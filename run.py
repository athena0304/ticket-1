# -*- coding: utf-8 -*-
import json
import urllib
import urllib2
from functools import wraps
import sys

from flask import Flask
from flask import render_template, session, redirect
from flask import request
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from tools.odbc import get_odbc_inst
from tools.global_conf import *

from tools.WRONG_CODE import *

reload(sys)
sys.setdefaultencoding("utf-8")

conf = WechatConf(
    token=token,
    appid=appid,
    appsecret=appsecret,
    encrypt_mode='mormal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    # encoding_aes_key='your_encoding_aes_key'  # 如果传入此值则必须保证同时传入 token, appid
)
wechat = WechatBasic(conf=conf)
app = Flask(__name__)


@app.route('/test')
def test():
    return 'hello gsteps'


@app.route('/check_signature')
def check_signature():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echostr = request.args.get('echostr', '')
    if wechat.check_signature(signature, timestamp, nonce):
        # return json.dumps({'echostr':echostr})
        return echostr
    else:
        return json.dumps({'echostr': ''})


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            session['target_union_id'] = request.args.get('union_id', '')
            print 'login_required   target_union_id:%s' % session['target_union_id']
            callback_url = urllib.quote_plus('%s/callback' % domain)
            urls = 'https://open.weixin.qq.com/connect/oauth2/authorize?' \
                   'appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect' % (
                       appid, callback_url)
            return redirect(urls)
        else:
            pass
        return f(*args, **kwargs)

    return decorated_function


def url_get(urls):
    # import requests
    # res = requests.post(urls).text
    # return json.loads(res)
    req = urllib2.Request(urls)
    response = urllib2.urlopen(req)
    return json.loads(response.read())


def get_user_info():
    urls = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (
        session['access_token'], session['open_id'])
    res = url_get(urls)
    user_info = {
        'open_id': res['openid'],
        'nickname': res['nickname'],
        'sex': res['sex'],
        'province': res['province'],
        'city': res['city'],
        'country': res['country'],
        'head_img_url': res['headimgurl'],
        'privilege': res['privilege'],
        'union_id': res['unionid'],
    }
    return user_info


@app.route('/callback', methods=['POST', 'GET'])
def callback():
    code = request.args.get('code', '')
    state = request.args.get('state')
    if code:
        code_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' \
                   'appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (appid, appsecret, code)
        res = url_get(code_url)
        session['access_token'] = res['access_token']
        session['open_id'] = res['openid']
        user_info = get_user_info()
        session['union_id'] = user_info['union_id']
        get_odbc_inst().register_user(user_info)
    return redirect('/?union_id=%s' % user_info['union_id'])


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    union_id = session.get('union_id', '')
    target_union_id = session.get('target_union_id', '')
    print request.url
    if not target_union_id:
        target_union_id = request.args.get('target_union_id', '')
    if not target_union_id:
        foo_union_id = request.args.get('union_id', '')
        if foo_union_id and foo_union_id != union_id:
            target_union_id = foo_union_id
    print 'index   target_union_id:%s' % session['target_union_id']
    if target_union_id and union_id != target_union_id:
        cheer_num = get_odbc_inst().get_cheer_num(target_union_id)
        print 'target_cheer_num:%s' % cheer_num
        session['target_union_id'] = ''
        return render_template('cheer.html', union_id=union_id, target_union_id=target_union_id, cheer_num=cheer_num)
    else:
        cheer_num = get_odbc_inst().get_cheer_num(union_id)
        return render_template('index.html', union_id=union_id, cheer_num=cheer_num)


@app.route('/cheer', methods=['POST', 'GET'])
@login_required
def cheer():
    return redirect('/?union_id=%s' % session['union_id'])


@app.route('/async_cheer', methods=['POST'])
@login_required
def async_cheer():
    union_id = request.form.get('union_id', '')
    target_union_id = request.form.get('target_union_id', '')
    code = RIGHT
    if not union_id:
        code = CHEER_UNION_ID_IS_NULL
    elif not target_union_id:
        code = CHEER_TARGET_UNION_ID_IS_NULL
    else:
        code = get_odbc_inst().cheer(union_id, target_union_id)
    if code == RIGHT:
        target_cheer_num = get_odbc_inst().get_cheer_num(target_union_id)
        return json.dumps({'code': code, 'target_cheer_num': target_cheer_num})
    else:
        return json.dumps({'code': code})


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'opends-client-secrets'
    app.run(host='0.0.0.0', port=80)

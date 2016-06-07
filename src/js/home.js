$(document).ready(function() {


    wx.config({
        debug: true, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
        appId: 'wx9e8843162b182d8f', // 必填，公众号的唯一标识
        timestamp: , // 必填，生成签名的时间戳
        nonceStr: '', // 必填，生成签名的随机串
        signature: '', // 必填，签名，见附录1
        jsApiList: [] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
    });

    wx.onMenuShareTimeline({
        title: '360G-STEPS街舞社公演入场券！开抢啦！', // 分享标题
        link: '', // 分享链接
        imgUrl: 'static/img/logo.png', // 分享图标
        success: function() {
            // 用户确认分享后执行的回调函数
        },
        cancel: function() {
            // 用户取消分享后执行的回调函数
        }
    });

    wx.onMenuShareAppMessage({
        title: '360G-STEPS街舞社公演入场券！开抢啦！', // 分享标题
        desc: '一个连程序猿都会Hip-Hop的街舞社团，来瞧瞧我们的另一面！', // 分享描述
        link: '', // 分享链接
        imgUrl: 'static/img/logo.png', // 分享图标
        type: '', // 分享类型,music、video或link，不填默认为link
        dataUrl: '', // 如果type是music或video，则要提供数据链接，默认为空
        success: function() {
            // 用户确认分享后执行的回调函数
        },
        cancel: function() {
            // 用户取消分享后执行的回调函数
        }
    });

    function loadQrcode() {
        layer.open({
            title: [
                '长按关注官方账号',
                'background-color:#182f52; color:#fff;'
            ],
            content: "<img src='/static/img/qrcode.png'></img><p>长按关注G-STEPS街舞社可随时咨询问题</p>",
        })
    }

    $(".info").on("click", function() {
        loadQrcode();
    })

    $(".footer a").on("click", function() {
        loadQrcode();
    })



});
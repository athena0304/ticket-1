# -*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors as cursors
from DBUtils.PooledDB import PooledDB
from tools.global_conf import *
from WRONG_CODE import *


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class ODBC():
    def __init__(self):
        connect_info = {
            'server': server,
            'uid': uid,
            'port': port,
            'pwd': pwd
        }
        self.connect_info = connect_info
        self.list_pool = self.create_pool(self.connect_info, 'list')
        self.dict_pool = self.create_pool(self.connect_info, 'dict')

    def create_pool(self, connect_info, cursor_type='list'):
        if cursor_type == 'dict':
            mysql_cursor = cursors.DictCursor
        else:
            mysql_cursor = cursors.SSCursor
        pool = PooledDB(MySQLdb,
                        host=connect_info['server'],
                        port=connect_info['port'],
                        user=connect_info.get('uid', ''),
                        passwd=connect_info.get('pwd', ''),
                        db=connect_info.get('database', ''),
                        cursorclass=mysql_cursor,
                        charset='utf8')
        return pool

    def get_cursor(self, cursor_type='list'):
        if cursor_type == 'dict':
            conn = self.dict_pool.connection()
            cursor = conn.cursor()
            return conn, cursor
        else:
            conn = self.list_pool.connection()
            cursor = conn.cursor()
            return conn, cursor

    def register_user(self, user_info):
        conn, cursor = self.get_cursor()
        sql = "select count(1) from `ticket`.`user` where `open_id`='%s' and `union_id`='%s' " % (
            (user_info['open_id'], user_info['union_id']))
        cursor.execute(sql)
        res = cursor.fetchall()
        if res[0][0] == 1:
            pass
        else:
            user_info_keys = [
                'open_id',
                'nickname',
                'sex',
                'province',
                'city',
                'country',
                'head_img_url',
                'privilege',
                'union_id'
            ]
            pre_compile = []
            infos = []
            for x in user_info_keys:
                pre_compile.append('%s')
                infos.append(str(user_info[x]))
            pre_compile = ','.join(pre_compile)
            keys = ','.join(user_info_keys)
            sql = u'insert into `ticket`.`user` (%s) values (%s)' % (keys, pre_compile)
            cursor.execute(sql, tuple(infos))

    def cheer(self, union_id, target_union_id):
        try:
            if self.has_cheer(union_id, target_union_id):
                return CHEER_REPEAT
            else:
                conn, cursor = self.get_cursor()
                sql = 'insert into `ticket`.`cheer` (`union_id`, `target_union_id`) values (%s, %s)'
                cursor.execute(sql, (union_id, target_union_id))
                return RIGHT
        except Exception, e:
            print e
            return CHEER_EXCEPT

    def has_cheer(self, union_id, target_union_id):
        try:
            conn, cursor = self.get_cursor()
            sql = "select count(1) from `ticket`.`cheer` where `union_id`='%s' and `target_union_id`='%s' " % (
                union_id, target_union_id)
            cursor.execute(sql)
            res = cursor.fetchall()
            if res[0][0] == 1:
                return True
            else:
                return False
        except Exception, e:
            print e
            return False

    def get_cheer_num(self, union_id):
        try:
            conn, cursor = self.get_cursor()
            sql = "select count(1) from `ticket`.`cheer` where `target_union_id`='%s' " % union_id
            cursor.execute(sql)
            res = cursor.fetchall()
            cheer_num = res[0][0]
            return cheer_num
        except Exception, e:
            print e
            return 0

    def is_user_exist(self, union_id):
        try:
            conn, cursor = self.get_cursor()
            sql = "select count(1) from `ticket`.`user` where `union_id`='%s' " % union_id
            cursor.execute(sql)
            res = cursor.fetchall()
            if res[0][0] == 0:
                return False
            else:
                return True
        except Exception, e:
            return False


def get_odbc_inst():
    return ODBC()

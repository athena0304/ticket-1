# -*- coding: utf-8 -*-
__author__ = 'guoguangchuan'


from tools.global_conf import satisfy_cheer_num


def get_remain_cheer_num(cheer_num):
    remain_cheer_num = satisfy_cheer_num - cheer_num
    if remain_cheer_num < 0:
        remain_cheer_num = 0
    return remain_cheer_num

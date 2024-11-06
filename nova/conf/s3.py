# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__project__ =  'openstack-nova'
__file__    =  's3.py'
__author__  =  'king'
__time__    =  '2024/9/5 16:50'


                              _ooOoo_
                             o8888888o
                             88" . "88
                             (| -_- |)
                             O\  =  /O
                          ____/`---'\____
                        .'  \\|     |//  `.
                       /  \\|||  :  |||//  \
                      /  _||||| -:- |||||-  \
                      |   | \\\  -  /// |   |
                      | \_|  ''\---/''  |   |
                      \  .-\__  `-`  ___/-. /
                    ___`. .'  /--.--\  `. . __
                 ."" '<  `.___\_<|>_/___.'  >'"".
                | | :  `- \`.;`\ _ /`;.`/ - ` : | |
                \  \ `-.   \_ __\ /__ _/   .-` /  /
           ======`-.____`-.___\_____/___.-`____.-'======
                              `=---='
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                       佛祖保佑        永无BUG
"""

from oslo_config import cfg

s3_opt_group = cfg.OptGroup("s3")

s3_opts = [
    cfg.BoolOpt("enabled", default=False, help="enable S3 storage"),
    cfg.StrOpt('bucket', default='screenshots'),
    cfg.StrOpt('endpoint', default=''),
    cfg.StrOpt('access_key', default=''),
    cfg.StrOpt('secret_key', default=''),
]


def register_opts(conf):
    conf.register_group(s3_opt_group)
    conf.register_opts(s3_opts, group=s3_opt_group)


def list_opts():
    return {s3_opt_group: s3_opts}

# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__project__ =  'openstack-nova'
__file__    =  'server_screenshots.py'
__author__  =  'king'
__time__    =  '2024/9/3 14:21'


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
from nova.api.validation import parameter_types

create = {
    'type': 'object',
    'properties': {
        'screenshot': {
            'type': 'object',
            'properties': {
                'name': parameter_types.name,
                'screen': parameter_types.non_negative_integer,
                'format': {
                    'type': 'string',
                    'enum': ['PNG', 'png', 'JPG', 'jpg'],
                },
            },
            'required': ['name'],
            'additionalProperties': False,
        },
    },
    'required': ['screenshot'],
    'additionalProperties': False,
}

update = {
    'type': 'object',
    'properties': {
        'screenshot': {
            'type': 'object',
            'properties': {
                'name': parameter_types.name,
            },
            'required': ['name'],
            'additionalProperties': False,
        },
    },
    'required': ['screenshot'],
    'additionalProperties': False,
}

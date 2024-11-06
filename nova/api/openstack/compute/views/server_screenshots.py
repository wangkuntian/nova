# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__project__ =  'openstack-nova'
__file__    =  'server_screenshots.py'
__author__  =  'king'
__time__    =  '2024/9/9 16:46'


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
from oslo_log import log
from nova.api.openstack import common

LOG = log.getLogger(__name__)


class ViewBuilder(common.ViewBuilder):

    @staticmethod
    def basic(request, screenshot):
        screenshot = {
            'id': screenshot.uuid,
            'name': screenshot.name,
            'size': screenshot.size,
            'format': screenshot.format,
            'height': screenshot.height,
            'width': screenshot.width,
            'screen': screenshot.screen,
            'path': screenshot.path,
            'remote': screenshot.remote,
            'created_at': screenshot.created_at,
            'updated_at': screenshot.updated_at,
        }
        return screenshot

    def show(self, request, screenshot):
        screenshot = self.basic(request, screenshot)
        return dict(screenshot=screenshot)

    def index(self, request, screenshots):
        screenshots = [
            self.basic(request, screenshot) for screenshot in screenshots
        ]
        return dict(screenshots=screenshots)

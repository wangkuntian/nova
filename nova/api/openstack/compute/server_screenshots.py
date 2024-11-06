# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__project__ =  'openstack-nova'
__file__    =  'server_screenshots.py'
__author__  =  'king'
__time__    =  '2024/9/3 13:50'


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
from webob import exc
from oslo_log import log

from nova import exception
from nova.api import validation
from nova.api.openstack import wsgi
from nova.api.openstack import common
from nova.api.openstack.compute.schemas import server_screenshots
from nova.api.openstack.compute.views import server_screenshots as views
from nova.compute import api as compute

LOG = log.getLogger(__name__)


class ServerScreenshotsController(wsgi.Controller):
    _view_builder_class = views.ViewBuilder

    def __init__(self, *args, **kwargs):
        super(ServerScreenshotsController, self).__init__()
        self.compute_api = compute.API()

    @wsgi.expected_errors((400, 404, 409))
    @validation.schema(server_screenshots.create)
    def create(self, req, server_id, body):
        context = req.environ["nova.context"]
        screenshot = body.get('screenshot')
        try:
            instance = self.compute_api.get(context, server_id)
            screenshot = self.compute_api.take_screenshot(
                context, instance, screenshot
            )
            response = self._view_builder.show(req, screenshot)
            return response
        except exception.InstanceNotFound as ex:
            raise exc.HTTPNotFound(explanation=ex.format_message())
        except exception.InstanceInvalidState as state_error:
            raise common.raise_http_conflict_for_instance_invalid_state(
                state_error, 'screenshot', server_id
            )

    @wsgi.expected_errors((400, 404))
    def index(self, req, server_id):
        context = req.environ["nova.context"]
        instance = common.get_instance(
            self.compute_api,
            context,
            server_id,
        )
        sort_key = req.params.get('sort_key', 'created_at')
        sort_dir = req.params.get('sort_dir', 'desc')
        limit, marker = common.get_limit_and_marker(req)
        screenshots = self.compute_api.get_screenshots(
            context, instance, sort_key, sort_dir, limit, marker
        )
        response = self._view_builder.index(req, screenshots)
        return response

    @wsgi.expected_errors((400, 404))
    @validation.schema(server_screenshots.update)
    def update(self, req, server_id, id, body):
        context = req.environ["nova.context"]
        updates = body['screenshot']
        try:
            _ = self.compute_api.get(context, server_id)
            screenshot = self.compute_api.update_screenshot(
                context, id, updates
            )
            response = self._view_builder.show(req, screenshot)
            return response
        except (
                exception.InstanceNotFound,
                exception.InstanceScreenshotNotFound,
        ) as ex:
            raise exc.HTTPNotFound(explanation=ex.format_message())

    @wsgi.expected_errors((400, 404, 409, 501))
    def show(self, req, server_id, id):
        context = req.environ["nova.context"]
        try:
            _ = self.compute_api.get(context, server_id)
            screenshot = self.compute_api.get_screenshot(context, id)
            response = self._view_builder.show(req, screenshot)
            return response
        except (
                exception.InstanceNotFound,
                exception.InstanceScreenshotNotFound,
        ) as ex:
            raise exc.HTTPNotFound(explanation=ex.format_message())

    @wsgi.response(204)
    @wsgi.expected_errors((400, 404))
    def delete(self, req, server_id, id):
        context = req.environ["nova.context"]
        try:
            instance = self.compute_api.get(context, server_id)
            self.compute_api.delete_screenshot(context, instance, id)
        except (
                exception.InstanceNotFound,
                exception.InstanceScreenshotNotFound,
        ) as ex:
            raise exc.HTTPNotFound(explanation=ex.format_message())

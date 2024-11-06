# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__project__ =  'openstack-nova'
__file__    =  'instance_screenshot.py'
__author__  =  'king'
__time__    =  '2024/9/3 17:12'


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
from oslo_utils import uuidutils
from oslo_serialization import jsonutils

from nova import exception
from nova.db import api as db
from nova.db.sqlalchemy import api as db_api
from nova.objects import base
from nova.objects import fields

LOG = log.getLogger(__name__)

_INSTANCE_SCREENSHOT_FIELDS = [
    'screen',
    'size',
    'width',
    'height',
    'path',
    'remote',
    'format',
]


@base.NovaObjectRegistry.register
class InstanceScreenshot(
    base.NovaPersistentObject,
    base.NovaEphemeralObject,
    base.NovaObjectDictCompat,
):
    # Version 1.0: Initial version
    VERSION = '1.0'

    fields = {
        'id': fields.IntegerField(),
        'uuid': fields.UUIDField(),
        'name': fields.StringField(),
        'instance_uuid': fields.UUIDField(),
        'screen': fields.IntegerField(default=0),
        'size': fields.IntegerField(default=0),
        'format': fields.StringField(default='png'),
        'height': fields.FloatField(default=0),
        'width': fields.FloatField(default=0),
        'path': fields.StringField(default=''),
        'remote': fields.StringField(default=''),
    }

    @staticmethod
    def _from_db_object(context, screenshot, db_screenshot):
        screenshot._context = context
        for field in screenshot.fields:
            if field not in _INSTANCE_SCREENSHOT_FIELDS:
                screenshot[field] = db_screenshot[field]
            else:
                extra = jsonutils.loads(db_screenshot['extra'])
                screenshot[field] = extra.get(field, None)
        screenshot.obj_reset_changes()
        return screenshot

    @base.remotable
    def create(self):
        if self.obj_attr_is_set('id'):
            raise exception.ObjectActionError(
                action='create', reason='already created'
            )
        updates = self.obj_get_changes()
        extra = dict()
        for field in updates.copy():
            if field in _INSTANCE_SCREENSHOT_FIELDS:
                update = updates.pop(field)
                extra[field] = update

        if 'uuid' not in updates:
            updates['uuid'] = uuidutils.generate_uuid()
            self.uuid = updates['uuid']

        updates['deleted'] = 0
        updates['extra'] = jsonutils.dumps(extra)
        db_screenshot = db.screenshot_create(self._context, updates)
        self._from_db_object(self._context, self, db_screenshot)

    @staticmethod
    @db_api.require_context
    @db_api.pick_context_manager_writer
    def _save(context, screenshot_id, updates):
        extra = updates.pop('extra')
        db_screenshot = db.screenshot_get_by_id(context, screenshot_id)
        db_extra = jsonutils.loads(db_screenshot.extra)
        db_extra.update(extra)
        updates['extra'] = jsonutils.dumps(db_extra)
        db_screenshot.update(updates)
        db_screenshot.save(context.session)
        return db_screenshot

    @base.remotable
    def save(self):
        updates = self.obj_get_changes()
        extra = dict()
        for field in updates.copy():
            if field in _INSTANCE_SCREENSHOT_FIELDS:
                update = updates.pop(field)
                extra[field] = update
        updates['extra'] = extra
        db_screenshot = self._save(self._context, self.id, updates)
        self._from_db_object(self._context, self, db_screenshot)

    def destroy(self):
        db.screenshot_destroy(self._context, self.id)

    @classmethod
    def get_by_id(cls, context, screenshot_id):
        db_screenshot = db.screenshot_get_by_id(context, screenshot_id)
        cls._from_db_object(context, cls(context), db_screenshot)

    @classmethod
    def get_by_uuid(cls, context, screenshot_uuid):
        db_service = db.screenshot_get_by_uuid(context, screenshot_uuid)
        return cls._from_db_object(context, cls(context), db_service)


@base.NovaObjectRegistry.register
class InstanceScreenshotList(base.ObjectListBase, base.NovaObject):
    # Version 1.0: Initial version
    VERSION = '1.0'

    fields = {
        'objects': fields.ListOfObjectsField('InstanceScreenshot'),
    }

    @staticmethod
    @db.select_db_reader_mode
    def _get_all_by_instance(
            context,
            instance_uuid,
            sort_key='created_at',
            sort_dir='desc',
            limit=None,
            marker=None,
    ):
        return db.screenshot_get_all_by_instance(
            context, instance_uuid, sort_key, sort_dir, limit, marker
        )

    @base.remotable_classmethod
    def get_by_instance_uuid(
            cls,
            context,
            instance_uuid,
            sort_key='created_at',
            sort_dir='desc',
            limit=None,
            marker=None,
    ):
        db_screenshots = cls._get_all_by_instance(
            context, instance_uuid, sort_key, sort_dir, limit, marker
        )
        return base.obj_make_list(
            context,
            cls(context),
            InstanceScreenshot,
            db_screenshots or [],
        )

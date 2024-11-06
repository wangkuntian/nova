# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__project__ =  'openstack-nova'
__file__    =  's3_utils.py'
__author__  =  'king'
__time__    =  '2024/9/4 13:35'


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
from oslo_config.cfg import CONF
from oslo_log import log as logging

try:
    import boto3
except ImportError:
    boto3 = None

CLIENT = None
LOG = logging.getLogger(__name__)


def get_client():
    global CLIENT
    if not CLIENT:
        CLIENT = RGWClient(
            endpoint=CONF.s3.endpoint,
            access_key=CONF.s3.access_key,
            secret_key=CONF.s3.secret_key,
            bucket=CONF.s3.bucket,
        )
    return CLIENT


class ACLS(object):
    PRIVATE = 'private'
    PUBLIC_READ = 'public-read'
    PUBLIC_READ_WRITE = 'public-read-write'
    AUTHENTICATED_READ = 'authenticated-read'


class RGWClient(object):
    def __init__(
            self, endpoint: str, access_key: str, secret_key: str, bucket: str
    ):
        self.endpoint = endpoint
        self._check_boto3_installed()
        self.client = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        if not self.head_bucket(bucket):
            self.create_bucket(bucket)

    @staticmethod
    def _check_boto3_installed():
        if boto3 is None:
            raise ImportError('boto3 is not installed')

    def head_bucket(self, bucket: str) -> bool:
        try:
            _ = self.client.head_bucket(Bucket=bucket)
        except Exception:
            return False
        else:
            return True

    def create_bucket(self, bucket: str, acl: str = ACLS.PUBLIC_READ):
        try:
            self.client.create_bucket(Bucket=bucket, ACL=acl)
        except Exception as ex:
            LOG.error(ex)

    def _remote(self, bucket: str, object_name: str):
        return f'{self.endpoint}/{bucket}/{object_name}'

    def upload(
            self,
            bucket: str,
            file_path: str,
            object_name: str,
            acl: str = ACLS.PUBLIC_READ,
    ) -> (bool, str):
        remote_path = self._remote(bucket, object_name)
        try:
            LOG.info(f'uploading file {file_path} to {remote_path}')
            self.client.upload_file(
                file_path, bucket, object_name, ExtraArgs={'ACL': acl}
            )
            success = True
        except boto3.exceptions.S3UploadFailedError as ex:
            success = False
            LOG.error(ex)
        return success, remote_path

    def delete_object(self, bucket: str, object_name: str):
        remote_path = self._remote(bucket, object_name)
        try:
            LOG.info(f'deleting object {remote_path}')
            self.client.delete_object(Bucket=bucket, Key=object_name)
        except Exception as ex:
            LOG.error(ex)

    def list_objects(self, bucket: str, prefix: str = ''):
        result = self.client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        for content in result['Contents']:
            LOG.debug(content)

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# This is a placeholder for backports.
# Do not use this number for new work.  New work starts after
# all the placeholders.
#
# See this for more information:
# http://lists.openstack.org/pipermail/openstack-dev/2013-March/006827.html

from sqlalchemy import Column, Index
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    meta.reflect()

    instance_screenshots = Table(
        'instance_screenshots',
        meta,
        Column('id', Integer, primary_key=True, nullable=False),
        Column('uuid', String(36), nullable=False),
        Index('screenshots_uuid_idx', 'uuid', unique=True),
        Column(
            'instance_uuid',
            String(length=36),
            ForeignKey(
                'instances.uuid', name='screenshots_instance_uuid_fkey'
            ),
            nullable=False,
        ),
        Column('name', String(length=255)),
        Column('extra', Text()),
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted', Integer),
        Column('deleted_at', DateTime),
        mysql_engine='InnoDB',
        mysql_charset='utf8',
    )
    instance_screenshots.create(migrate_engine)

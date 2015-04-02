# Copyright 2013 Mirantis Inc.
# Copyright 2014 Cloudbase Solutions Srl
#
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

from oslo.config import cfg
import yaml

from cloudbaseinit.openstack.common import log as logging
from cloudbaseinit.plugins.common.userdataplugins import base
from cloudbaseinit.plugins.common.userdataplugins.cloudconfigplugins import (
    factory
)


LOG = logging.getLogger(__name__)
OPTS = [
    cfg.StrOpt(
        'skyfrom_metadata_path',
        default='C:/cloudinit/metadata',
        help=(
            'The skyform metadata file location'
        ),
    )
]
CONF = cfg.CONF
CONF.register_opts(OPTS)
DEFAULT_ORDER_VALUE = 999

class SkyformConfigPlugin(base.BaseUserDataPlugin):

    def __init__(self):
        super(SkyformConfigPlugin, self).__init__("text/skyform-config")

    def process_non_multipart(self, part):
        """Process the given data"""
        
        import os, ConfigParser, json
        init_path = os.getenv('CLOUDINIT_PATH') or CONF.skyform_metadata_path
        try:
            part = part[len('#cloud-skyform'):]
            data = json.loads(part)
            config = ConfigParser.ConfigParser()
            config.add_section('DEFAULT')
            for k,v in data:
                config.set(k, v)

            with open(init_path, 'wb') as configfile:
                config.write(configfile)

        except Exception,e :
            LOG.debug('failed to generate the metadata file. due to %s' % e)
                
    def process(self, part):
        payload = part.get_payload()
        self.process_non_multipart(payload)

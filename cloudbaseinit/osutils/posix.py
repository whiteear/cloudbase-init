# Copyright 2012 Cloudbase Solutions Srl
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

import os

from cloudbaseinit.osutils import base


class PosixUtils(base.BaseOSUtils):

    def reboot(self):
        os.system('reboot')

    def get_dhcp_hosts_in_use(self):
        dhclientFile = '/var/lib/dhclient/dhclient-eth0.leases'
        dhfp = file(dhclientFile)
        content = dhfp.read()
        lineList = content.split('\n')
        dhfp.close()

        dhcpServer = []
        for line in lineList:
            if 'dhcp-server-identifier' in line:
                dhcpServer.append(line.strip().split(' '))

        if not dhcpServer:
            return None

        dhcpServer = dhcpServer[len(dhcpServer)-1][2][:-1]
        return [('', dhcpServer)]

    def set_config_value(self, name, value, section=None):
        pass

    def get_config_value(self, name, section=None):
        """
        PLUGIN_EXECUTION_DONE = 1
        PLUGIN_EXECUTE_ON_NEXT_BOOT = 2
        """ 
        return 2

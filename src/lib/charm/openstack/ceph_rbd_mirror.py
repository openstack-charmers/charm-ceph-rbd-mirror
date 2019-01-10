# Copyright 2018 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections

import charms_openstack.charm
import charms_openstack.adapters


class CephRBDMirrorCharm(charms_openstack.charm.OpenStackCharm):
    # Override source config key to be compatible with the other Ceph charms
    source_config_key = 'source'

    # We require Ceph 12.2 Luminous or later for HA support in the Ceph
    # rbd-mirror daemon.  Luminous appears in UCA at pike.
    release = 'pike'
    name = 'ceph-rbd-mirror'
    packages = ['rbd-mirror']
    python_version = 3
    required_relations = ['ceph-cluster']
    release_pkg = 'rbd-mirror'
    package_codenames = {
        'rbd-mirror': collections.OrderedDict([
            ('12', 'pike'),
            ('13', 'rocky'),
        ]),
    }

    def install(self):
        """We override install function to configure source before installing
        packages.

        The OpenStackAPICharm class already does this but we do not need nor
        want the other services it provides for Ceph charms."""
        self.configure_source()
        super().install()

# Copyright 2019 Intel, Inc.
# All Rights Reserved.
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

"""Version 2 of the Cyborg API"""

import pecan
from pecan import rest
from wsme import types as wtypes

from cyborg.api.controllers import base
from cyborg.api.controllers import link
from cyborg.api.controllers.v2 import api_version_request
from cyborg.api.controllers.v2 import arqs
from cyborg.api.controllers.v2 import device_profiles
from cyborg.api.controllers.v2 import devices
from cyborg.api import expose


class V2(base.APIBase):
    """The representation of the version 2 of the API."""

    id = wtypes.text
    """The ID of the version"""

    links = [link.Link]
    """Links to the accelerator resource"""

    max_version = wtypes.text
    """Highest microversion supported"""

    min_version = wtypes.text
    """Lowest microversion supported"""

    status = wtypes.text
    """Status"""

    @staticmethod
    def convert():
        v2 = V2()
        v2.id = 'v2.0'
        v2.max_version = api_version_request.max_api_version().get_string()
        v2.min_version = api_version_request.min_api_version().get_string()
        v2.status = 'CURRENT'
        v2.links = [
            link.Link.make_link('self', pecan.request.public_url,
                                '', ''),
            ]
        return v2


class Controller(rest.RestController):
    """Version 2 API controller root"""

    device_profiles = device_profiles.DeviceProfilesController()
    accelerator_requests = arqs.ARQsController()
    devices = devices.DevicesController()

    @expose.expose(V2)
    def get(self):
        return V2.convert()


__all__ = ('Controller',)

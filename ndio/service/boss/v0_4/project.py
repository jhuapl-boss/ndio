# Copyright 2016 The Johns Hopkins University Applied Physics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ndio.service.boss.service import Service
from .base import Base

class ProjectService_0_4(Base):
    def __init__(self):
        super().__init__()

    def list(self, resource, url_prefix, auth):
        return self.get_request(resource, 'GET', 'application/json', url_prefix, auth, list_req = True)

    def create(self, resource, url_prefix, auth):
        pass

    def get(self, resource, url_prefix, auth):
        pass

    def update(self, resource, url_prefix, auth):
        pass

    def delete(self, resource, url_prefix, auth):
        pass
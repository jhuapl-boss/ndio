﻿# Copyright 2016 The Johns Hopkins University Applied Physics Laboratory
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

"""
This example shows how to work with the Boss' groups.  Specifically, this
example demonstrates creating and deleting groups and managing the users that 
belong to a group.  The Remote class methods that begin with 'group_' perform
group operations.

Groups are collections of users.  Permissions are associated with groups
and resources.  The three combined determine what a user may do with a
particular resource.
"""

from ndio.remote.boss.remote import Remote, LATEST_VERSION
from ndio.ndresource.boss.resource import *
from requests import HTTPError

API_VER = LATEST_VERSION
rmt = Remote('example.cfg')
#rmt = Remote('test.cfg')
rmt.group_perm_api_version = API_VER

# Turn off SSL cert verification.  This is necessary for interacting with
# developer instances of the Boss.
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
rmt.project_service.session_send_opts = { 'verify': False }
rmt.metadata_service.session_send_opts = { 'verify': False }
rmt.volume_service.session_send_opts = { 'verify': False }

# Note spaces are not allowed in group names.
grp_name = 'my_group'

# Boss user names still in flux.
user_name = 'bossadmin'

print('Creating group . . .')
try:
    rmt.group_create(grp_name)
except HTTPError as h:
    # Assume group already exists if an exception raised.
    print(h.response.content)

print('Confirm group created . . .')
if rmt.group_get(grp_name):
    print('Confirmed')

print('Add user to group . . .')
rmt.group_add_user(grp_name, user_name)

print('Confirm user is member of group . . .')
if rmt.group_get(grp_name, user_name):
    print('Confirmed')
else:
    print('NOT a member of the group')

print('Remove user from group . . .')
rmt.group_delete(grp_name, user_name)

print('Confirm user is not a member of group . . .')
if rmt.group_get(grp_name, user_name):
    print('Still a member of the group; removal must have failed')
else:
    print('Confirmed')

print('Deleting group . . .')
rmt.group_delete(grp_name)

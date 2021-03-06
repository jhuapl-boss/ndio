﻿from ndio.remote.boss.remote import Remote, LATEST_VERSION
from ndio.ndresource.boss.resource import *
import sys
import numpy
from requests import HTTPError

rmt = Remote('example.cfg')
#rmt = Remote('test.cfg')
API_VER = LATEST_VERSION

# Turn off SSL cert verification.  This is necessary for interacting with
# developer instances of the Boss.
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
rmt.project_service.session_send_opts = { 'verify': False }
rmt.metadata_service.session_send_opts = { 'verify': False }
rmt.volume_service.session_send_opts = { 'verify': False }

COLL_NAME = 'gray'
EXP_NAME = 'alpha'
CHAN_NAME = 'ex_EM'

chan_setup = ChannelResource(
    CHAN_NAME, COLL_NAME, EXP_NAME, API_VER, 'Example channel.', datatype='uint16')
try:
    chan_actual = rmt.project_get(chan_setup)
except HTTPError:
    chan_actual = rmt.project_create(chan_setup)

print('Data model setup.')

# Ranges use the Python convention where the number after the : is the stop
# value.  Thus, x_rng specifies x values where: 0 <= x < 8.
x_rng = '0:8'
y_rng = '0:4'
z_rng = '0:5'

# Note that the numpy matrix is in Z, Y, X order.
data = numpy.random.randint(0, 3000, (5, 4, 8))
data = data.astype(numpy.uint16)

# Upload the cutout to the channel.
rmt.cutout_create(chan_actual, 0, x_rng, y_rng, z_rng, data)

# Verify that the cutout uploaded correctly.
cutout_data = rmt.cutout_get(chan_actual, 0, x_rng, y_rng, z_rng)
numpy.testing.assert_array_equal(data, cutout_data)

# Get only a small piece of the cutout.
small_cutout_data = rmt.cutout_get(chan_actual, 0, '0:1', '0:1', '0:5')
numpy.testing.assert_array_equal(data[0:5, 0:1, 0:1], small_cutout_data)

# For times series data, the matrix is in t, Z, Y, X order.
time_rng = '0:3'
time_data = numpy.random.randint(0, 3000, (3, 5, 4, 8), numpy.uint16)

rmt.cutout_create(chan_actual, 0, x_rng, y_rng, z_rng, time_data, time_rng)

time_cutout_data = rmt.cutout_get(chan_actual, 0, x_rng, y_rng, z_rng, time_rng)
numpy.testing.assert_array_equal(time_data, time_cutout_data)

# Clean up.
rmt.project_delete(chan_actual)

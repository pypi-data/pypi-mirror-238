import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
django.setup()

from django import http
from django.conf import settings
import dodi
from PIL import Image
import re
from .test_utils import *

# Test url_base()
assert 'DODI_BASE_URL' not in settings.__dict__
assert_equal(dodi.url_base(), '/dodi/')
settings.DODI_BASE_URL = 'http://my_site.com/'
assert_equal(dodi.url_base(), 'http://my_site.com/dodi/')

# Test url()
settings.DODI_BASE_URL = '/'
assert_equal(dodi.url('foo', 'f'), '/dodi/f?foo')
assert_equal(dodi.static_url('fake', 'f'), '/dodi/f?/static/fake')

# make sure we can find collected static, uncollected static, and media files
assert_equal(get_response(dodi.url('fake_image', 'width=5')).status_code, 404)
assert_equal(get_response(dodi.static_url('app_static_ace_truck_small.jpg', 'width=5')).status_code, 200)
assert_equal(get_response(dodi.static_url('static_root_ace_truck_small.jpg', 'width=5')).status_code, 200)
assert_equal(get_response(dodi.url('/media/media_root_ace_truck_small.jpg', 'width=5')).status_code, 200)

# make sure pre-cropping works
image = get_response_image(dodi.static_url('ace_truck_200_100.jpg', 'crop_left=10;crop_right=5;crop_top=4;crop_bottom=3'))
assert image.width == 185 and image.height == 93

# make sure cropping works, jpg works
image = get_response_image(dodi.static_url('app_static_ace_truck_small.jpg', 'width=20;height=10;mode=crop'))
assert image.width == 20
assert image.height == 10

# # make sure fitting works
image = get_response_image(dodi.static_url('ace_truck_200_100.jpg', 'width=100;height=100'))
assert image.width == 100
assert image.height == 50
image = get_response_image(dodi.static_url('ace_truck_200_100.jpg', 'width=100;height=25'))
assert image.width == 50
assert image.height == 25

# make sure scale-up works
# without scale-up, we ensure it comes back cropped to correct aspect ratio
image = get_response_image(dodi.static_url('ace_truck_200_100.jpg', 'width=200;height=200;mode=crop'))
assert image.width == 100
assert image.height == 100
# with scale-up, we scale up
image = get_response_image(dodi.static_url('ace_truck_200_100.jpg', 'width=200;height=200;mode=crop;scale_up'))
assert image.width == 200
assert image.height == 200

# make sure no-extension jpg is recognized as jpeg
assert_equal(get_response(dodi.static_url('ace_truck_small_jpg', 'width=10;height=10;mode=crop'))['content-type'], 'image/jpeg')

# make sure png works, transparency preserved
image = get_response_image(dodi.static_url('sun.png', 'width=10;height=10;mode=crop'))
assert image.width == 10
assert image.format == 'PNG'
assert image.mode == 'RGBA'

# Ensure non-images return reasonable error
r = get_response(dodi.static_url('a.txt', 'width=10'))
assert r.status_code == 400
assert r.content == b'File could not be interpereted as an image'

# Match_orientation (landscape supplied, portrait requested)
image = get_response_image(dodi.static_url('ace_truck_200_100.jpg', 'width=70;height=100;mode=crop;match_orientation'))
assert image.width == 100 and image.height == 70
image = get_response_image(dodi.static_url('ace_truck_200_100.jpg', 'width=70;height=100;mode=scale;match_orientation'))
assert image.width == 100 and image.height == 50
image = get_response_image(dodi.static_url('ace_truck_200_100.jpg', 'width=70;height=100;mode=stretch;match_orientation'))
assert image.width == 100 and image.height == 70
# Match_orientation (portrait supplied, landscape requested)
image = get_response_image(dodi.static_url('ace_truck_100_200.jpg', 'width=100;height=70;mode=crop;match_orientation'))
assert image.width == 70 and image.height == 100
image = get_response_image(dodi.static_url('ace_truck_100_200.jpg', 'width=100;height=70;mode=scale;match_orientation'))
assert image.width == 50 and image.height == 100
image = get_response_image(dodi.static_url('ace_truck_100_200.jpg', 'width=100;height=70;mode=stretch;match_orientation'))
assert image.width == 70 and image.height == 100

# Test caching headers
r = get_response(dodi.static_url('sun.png', 'width=10;height=10;mode=crop'))
etag = r['etag']
assert re.match(r'"[^"]+"', etag), 'etags must be quoted'
assert r['cache-control'] == 'public, max-age=31536000'
r2 = get_response(dodi.static_url('sun.png', 'width=10;height=10;mode=crop'), **{'HTTP_IF_NONE_MATCH': etag})
assert r2.status_code == 304
assert r2['etag'] == etag
assert r2['cache-control'] == r['cache-control']
# send multiple etags, one matching
r2 = get_response(dodi.static_url('sun.png', 'width=10;height=10;mode=crop'), **{'HTTP_IF_NONE_MATCH': f'{etag} "a"'})
assert r2.status_code == 304
assert r2['etag'] == etag
assert r2['cache-control'] == r['cache-control']
# send etag, not matching
r2 = get_response(dodi.static_url('sun.png', 'width=10;height=10;mode=crop'), **{'HTTP_IF_NONE_MATCH': '"a"'})
assert r2.status_code == 200
assert r2['etag'] == etag
assert r2['cache-control'] == r['cache-control']

# Rotate
image = get_response_image(dodi.static_url('ace_truck_200_100.jpg', 'rotate=90'))
assert image.width == 100 and image.height == 200
image = get_response_image(dodi.static_url('ace_truck_200_100.jpg', 'rotate=270'))
assert image.width == 100 and image.height == 200
image = get_response_image(dodi.static_url('ace_truck_200_100.jpg', 'rotate=180'))
assert image.width == 200 and image.height == 100

r = get_response(dodi.static_url('ace_truck_200_100.jpg', 'rotate=91'))
assert r.status_code == 400
assert r.content == b'Invalid rotation: 91. The only allowed rotations are 0, 90, 180, and 270'
r = get_response(dodi.static_url('ace_truck_200_100.jpg', 'rotate=a'))
assert r.status_code == 400
assert r.content == b'Invalid rotation: a. The only allowed rotations are 0, 90, 180, and 270'

# Overlay
r = get_response(dodi.static_url('ace_truck_200_100.jpg', 'overlay=fake'))
assert r.status_code == 400
assert r.content == b'OverlayColor must be specified as "color,alpha"'
r = get_response(dodi.static_url('ace_truck_200_100.jpg', 'overlay=#888,0.5'))
assert r.status_code == 200

for transform in [
    'color=-1',
    'color=2',
    'brightness=-1',
    'brightness=2',
    'contrast=-1',
    'contrast=2',
] :
    r = get_response(dodi.static_url('ace_truck_small_jpg', transform))
    assert r.status_code == 400
for transform in [
    'color=0.5',
    'brightness=0.5',
    'contrast=0.5',
] :
    i = get_response_image(dodi.static_url('ace_truck_200_100.jpg', transform))
    assert i.width == 200 and i.height == 100

# This particular image has an exif issue that breaks transformations with earlier versions of Pillow
import PIL
print(PIL.__version__)
r = get_response(dodi.static_url('broken_exif.png', 'width=200'))
assert r.status_code == 200

print('Tests passed ✔')
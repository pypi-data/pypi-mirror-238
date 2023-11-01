from contextlib import contextmanager
from django.test import Client
from io import BytesIO
from pathlib import Path
from PIL import Image
import shutil

client = Client(SERVER_NAME='localhost')

# Turn off django server console logging
import logging
logging.getLogger('django').setLevel('ERROR')

@contextmanager
def assert_raises(cls):
    try :
        yield
    except cls :
        pass
    else :
        raise AssertionError(f'{cls} not raised')
def assert_equal(result, expected):
    if result != expected :
        raise AssertionError(f'unexpected result: {result}; expected: {expected}')

def get_response(site_relative_url, **extra):
    return client.get(site_relative_url, **extra)

def get_response_image(site_relative_url, **extra):
    r = get_response(site_relative_url)
    if r.status_code != 200 :
        raise Exception(f'Unexpected response: {r.status_code}: {r.content}')
    return Image.open(BytesIO(r.content))


output_path = Path(__file__).parent / 'output' 
def clear_output_images():
    if output_path.exists() :
        shutil.rmtree(output_path)
def store_response_image(site_relative_url):
    name = site_relative_url.rsplit('/', 1)[-1]
    name, params = name.split('?')
    name, ext = name.rsplit('.', 1)

    target = Path(output_path, f'{name}.{params}.{ext}')
    target.parent.mkdir(exist_ok=True, parents=True)
    target.write_bytes(get_response(site_relative_url).content)

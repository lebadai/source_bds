import json
from datetime import date, datetime
from rest_framework import exceptions

import os
from django.core.files.storage import FileSystemStorage
from urllib.parse import urljoin
from django.conf import settings

def validate_exception(text=None, code=None): # noqa
        fail = {
            'success': False,
            'detail': text,

        }
        raise exceptions.ValidationError(fail)

def decode_to_json(data):
    return json.loads(data)


def today():
    return date.today()


def now():
    return datetime.now()


def datetime_to_string(_time, _format='%d/%m/%Y %H:%M:%S'):
    if _time:
        return _time.strftime(_format)
    return ''


def convert_string_to_day(string, default=None):
    try:
        return datetime.strptime(string, '%Y-%m-%d')
    except (ValueError, TypeError):
        return default

def string_to_time(_string, _format='%d/%m/%Y %H:%M:%S'):
    if not isinstance(_string, str):
        return None
    
    try:
        return datetime.strptime(_string, _format)
    except (ValueError, IndexError, AttributeError):
        return None

def check_progressive_percent(total):
    ret = 0.0
    if not total:
        return ret
    for i in total:
        ret += i
    if ret == 100:
        return ret
    else:
        return validate_exception('progressive percent must be 100%')

def save_upload_file(file, sub_folder):

    file_size = int(file.size / 1024)
    if file_size > 1000000:
        return self.validate_exception('File upload too larger')
    name = file.name
    file_name = os.path.splitext(name)[0] + "_" + str(datetime.now().strftime("%Y%m%d%H%M%S"))
    file_content_type = os.path.splitext(name)[1][1:]
    
    fs = FileSystemStorage(location='cdn/' + sub_folder,
                            base_url=urljoin(settings.MEDIA_URL, sub_folder))
    filename = fs.save(file_name + "." + file_content_type, file)
    file_url = urljoin('http://127.0.0.1:8000', fs.url(filename))
    return file_url, file_size, file_name, file_content_type

def check_body(body):
    if body:
        try:
            content = decode_to_json(body)
            return content
        except Exception as ex:
            return validate_exception('Parsing body to json error')
    else:
        return validate_exception('Missing body')
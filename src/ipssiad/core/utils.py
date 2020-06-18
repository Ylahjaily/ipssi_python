import os
import datetime
import hashlib
import shutil

from django.core.exceptions import ValidationError


def validate_file_extension(file):
    ext = os.path.splitext(file.name)[1]
    valid_extension = ['.jpg', '.png', '.gif']
    if not ext.lower() in valid_extension:
        raise ValidationError('Unsupported file extension.')

def media_path(obj, filename):
    now = datetime.datetime.now()
    secure_hash = hashlib.md5()
    secure_hash.update(
        f'{now}'.encode('utf-8')
    )
    path = secure_hash.hexdigest()
    return '/'.join(['tmp', path, filename])


def delete_file(file):
    if os.path.isfile(file):
        source = os.path.dirname(os.path.abspath(file))
        shutil.rmtree(source)

from django.conf import settings
from django.urls import re_path
from . import views


if settings.DEBUG:
    from django.utils.autoreload import file_changed
    file_changed.disconnect(dispatch_uid='template_loaders_file_changed')


prefix = getattr(settings, 'MADMIN', {}).get('upload_path_prefix', 'madmin')


madmin_urls = [
    re_path('^{}/upload/'.format(prefix), views.upload, name="upload"),
    re_path('^{}/check_upload/'.format(prefix), views.check_upload, name="check_upload"),
]

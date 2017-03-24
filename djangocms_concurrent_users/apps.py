# -*- coding: utf-8 -*-
from django.apps.config import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

BLOCKING_OFFSET_DEFAULT = 20
POLLING_INTERVAL_DEFAULT = 10
BLOCK_EDITING_DEFAULT = True


class ConcurrentUsersConfig(AppConfig):
    name = 'djangocms_concurrent_users'
    verbose_name = 'Django Concurrent Users'

    def ready(self):

        blocking_offset = getattr(settings, 'CONCURRENT_BLOCKING_OFFSET', BLOCKING_OFFSET_DEFAULT)
        polling_interval = getattr(settings, 'CONCURRENT_POLLING_INTERVAL', POLLING_INTERVAL_DEFAULT)

        if blocking_offset <= polling_interval:
            raise ImproperlyConfigured('CONCURRENT_BLOCKING_OFFSET is shorter than CONCURRENT_POLLING_INTERVAL')




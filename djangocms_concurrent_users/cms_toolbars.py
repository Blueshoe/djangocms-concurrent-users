# -*- coding: utf-8 -*-
from cms.constants import RIGHT
from cms.toolbar.items import LinkItem
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from django.conf import settings

from .apps import POLLING_INTERVAL_DEFAULT
from django.template import RequestContext


class ConcurrencyButton(LinkItem):
    template = 'djangocms_concurrent_users/concurrency_button.html'

    def __init__(self, request):
        self.request = request
        self.side = RIGHT

    def get_context(self):
        context = RequestContext(self.request)
        context.push({'check_time': getattr(settings, 'CONCURRENT_POLLING_INTERVAL', POLLING_INTERVAL_DEFAULT) * 1000})
        return context


@toolbar_pool.register
class ConcurrentEditingModifier(CMSToolbar):

    def populate(self):
        concurrency_btn = ConcurrencyButton(self.toolbar.request)
        # we need to register this button in order to get the code into the template
        self.toolbar.add_item(concurrency_btn)

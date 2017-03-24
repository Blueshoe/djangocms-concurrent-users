# -*- coding: utf-8 -*-
from django.conf.urls import url

from djangocms_concurrent_users.views import PageIndicatorStatusView

urlpatterns = [
    url(r'^update_page_indicator/$', view=PageIndicatorStatusView.as_view(), name='update-page-indicator'),
]

# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings


class PageIndicator(models.Model):
    # the page to lock
    page = models.ForeignKey('cms.Page')
    editor = models.ForeignKey(settings.AUTH_USER_MODEL)
    # this timestamp gets updated with every polling request
    edited_on = models.DateTimeField()
    # this is the lock's creation timestamps
    started_editing = models.DateTimeField(null=True)

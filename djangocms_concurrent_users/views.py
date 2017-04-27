# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.template.defaultfilters import date as _date
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from cms.models.pagemodel import Page

from .apps import BLOCKING_OFFSET_DEFAULT, BLOCK_EDITING_DEFAULT
from djangocms_concurrent_users.models import PageIndicator


class PageIndicatorStatusView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.now = timezone.now()
        self.time_past = self.now - timezone.timedelta(seconds=getattr(settings, 'CONCURRENT_BLOCKING_OFFSET',
                                                                       BLOCKING_OFFSET_DEFAULT))
        return super(PageIndicatorStatusView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        _page = get_object_or_404(Page, pk=request.GET.get('page_id'))

        # release page for all users which did not update during the last timeframe
        PageIndicator.objects.filter(edited_on__lte=self.time_past, page=_page).delete()

        page_indicators = PageIndicator.objects.filter(edited_on__gte=self.time_past, page=_page) \
            .exclude(editor=request.user)

        response = {}
        if page_indicators.exists():
            response['conflict'] = True
            editing_user = page_indicators.first()
            response['concurrent_user'] = [editing_user.editor.username]
            # default behavior for concurrent users is blocking
            response['block_editing'] = getattr(settings, 'CONCURRENT_BLOCK_EDITING', BLOCK_EDITING_DEFAULT)

            response['message'] = _(u'The page is currently edited by {user} since {time}.') \
                .format(user=editing_user.editor, time=_date(editing_user.started_editing, 'D, d. b, H:i'))
            response['buttons'] = {
                'published_page': {
                    'link': '{url}?edit_off'.format(url=_page.get_absolute_url()),
                    'link_text': _('View Published Page'),
                },
                'back': {
                    'link': '',
                    'link_text': _('Back'),
                }
            }
        else:
            response['conflict'] = False

        return JsonResponse(json.dumps(response), safe=False)

    def post(self, request, *args, **kwargs):
        _page = get_object_or_404(Page, pk=request.POST.get('page_id'))

        def update_indicator():
            indicator = PageIndicator.objects.get(editor=request.user, edited_on__gte=self.time_past, page=_page)
            indicator.edited_on = self.now
            indicator.save()

        # To avoid uncontrolled creation of PageIndicators delete any for this user/page combination which
        # is too old.
        PageIndicator.objects.filter(editor=request.user, edited_on__lte=self.time_past, page=_page).delete()

        try:
            update_indicator()
        except PageIndicator.DoesNotExist:
            PageIndicator.objects.create(editor=request.user, edited_on=self.now, started_editing=self.now, page=_page)

        return HttpResponse(status=200)

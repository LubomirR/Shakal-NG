# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import PollDetail, PollList, PollCreate, PollPost


class Patterns(object):
	def __init__(self):
		self.app_name = 'polls'
		self.name = 'polls'

	@property
	def urls(self):
		pat = patterns('polls.views',
			url(r'^detail/(?P<slug>[-\w]+)/$', PollDetail.as_view(), name="detail-by-slug"),
			url(r'^(?:(?P<page>\d+)/)?$', PollList.as_view(), name='list'),
			url(r'^post/(?P<pk>\d+)/$', PollPost.as_view(), name='post'),
			url(r'^vytvorit/$', login_required(PollCreate.as_view()), name='create'),
		)
		return (pat, self.app_name, self.name)

urlpatterns = Patterns().urls

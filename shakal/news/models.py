# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

class News(models.Model):
	subject = models.CharField(max_length = 255, verbose_name = _('subject'))
	text = models.TextField(verbose_name = _('text'))
	time = models.DateTimeField(default = datetime.now, verbose_name = _('time'))
	author = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True, verbose_name = _('user'))
	authors_name = models.CharField(max_length = 255, verbose_name = _('authors name'))
	approved = models.BooleanField(default = False, verbose_name = _('approved'))

	class Meta:
		verbose_name = _('news item')
		verbose_name_plural = _('news items')
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.contenttypes.generic import GenericStackedInline
from django.utils.translation import ugettext_lazy as _

from attachment.models import Attachment


class AttachmentInline(GenericStackedInline):
	model = Attachment
	verbose_name = _('attachment')
	verbose_name_plural = _('attachments')
	ct_field = 'content_type'
	ct_fk_field = 'object_id'
	exclude = ('size', )
	can_delete = True
	template = "admin/edit_inline/stacked_collapse.html"


class AttachmentAdmin(admin.ModelAdmin):
	exclude = ('size', )


admin.site.register(Attachment, AttachmentAdmin)

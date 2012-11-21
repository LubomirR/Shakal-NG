# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class AntispamInput(TextInput):
	def render(self, name, value, attrs = None):
		question = self.attrs.pop('question', "")
		answer = self.attrs.pop("answer", "")
		data = super(AntispamInput, self).render(name, value, attrs)
		self.attrs['question'] = question
		self.attrs['answer'] = answer
		return mark_safe(question + data)


class AntispamField(CharField):
	widget = AntispamInput
	def clean(self, value):
		value = super(CharField, self).clean(value)
		if value != self.widget.attrs.get('answer', ""):
			raise ValidationError(_("Bad answer"))
		return value
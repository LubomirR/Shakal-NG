# -*- coding: utf-8 -*-
import os

from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader, find_template_loader
from django_tools.middlewares.ThreadLocal import get_current_request

from template_dynamicloader.utils import get_template_settings


class Loader(BaseLoader):
	is_usable = True

	def __init__(self, loaders):
		self._loaders = loaders
		self._cached_loaders = []

	@property
	def loaders(self):
		if not self._cached_loaders:
			cached_loaders = []
			for loader in self._loaders:
				cached_loaders.append(find_template_loader(loader))
			self._cached_loaders = cached_loaders
		return self._cached_loaders

	def get_visitors_template_dir(self):
		request = get_current_request()
		(template_device, template_skin, css) = get_template_settings(request)
		return os.path.join(template_device, template_skin.split(',')[0])

	def get_visitors_template(self, template_name):
		return os.path.join(self.get_visitors_template_dir(), template_name)

	def load_template(self, template_name, template_dirs = None):
		try:
			return self.direct_load_template(self.get_visitors_template(template_name), template_dirs, 'load_template')
		except TemplateDoesNotExist:
			return self.direct_load_template(template_name, template_dirs, 'load_template')

	def load_template_source(self, template_name, template_dirs = None):
		try:
			return self.direct_load_template(self.get_visitors_template(template_name), template_dirs, 'load_template_source')
		except TemplateDoesNotExist:
			return self.direct_load_template(template_name, template_dirs, 'load_template_source')

	def direct_load_template(self, visitors_template, template_dirs, load_type):
		for template_loader in self.loaders:
			try:
				return getattr(template_loader, load_type)(visitors_template, template_dirs)
			except TemplateDoesNotExist:
				pass
			except NotImplementedError:
				pass
			except AttributeError:
				pass
		raise TemplateDoesNotExist(visitors_template)

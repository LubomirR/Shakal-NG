# -*- coding: utf-8 -*-

from django.views.generic import CreateView


class AddLoggedFormArgumentMixin(object):
	def get_form(self, form_class):
		return form_class(logged = self.request.user.is_authenticated(), **self.get_form_kwargs())


class PreviewCreateView(CreateView):
	def form_valid(self, form):
		item = form.save(commit = False)
		if not 'create' in self.request.POST:
			return self.render_to_response(self.get_context_data(form = form, item = item, valid = True))
		return super(PreviewCreateView, self).form_valid(form)
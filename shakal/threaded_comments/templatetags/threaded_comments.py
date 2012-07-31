# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.contrib.comments.templatetags.comments import BaseCommentNode
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from shakal import threaded_comments

register = template.Library()


class ThreadedCommentsBaseNode(BaseCommentNode):
	def __init__(self, *args, **kwargs):
		super(ThreadedCommentsBaseNode, self).__init__(*args, **kwargs)
		self.root_node = None
		self.comments_model = threaded_comments.get_model()

	def get_root_node(self, context):
		if self.root_node is None:
			ctype, object_pk = self.get_target_ctype_pk(context)
			self.root_node = self.comments_model.objects.get_root_comment(ctype, object_pk)
		return self.root_node

	def get_comments_query_set(self, context):
		ctype, object_pk = self.get_target_ctype_pk(context)
		if not object_pk:
			return self.comments_model.comment_objects.none()

		queryset = self.comments_model.comment_objects.filter(
			content_type = ctype,
			object_pk = object_pk,
			site__pk = settings.SITE_ID
		)
		queryset = queryset.order_by('lft').select_related('user')
		print(type(self.comments_model.comment_objects))
		return queryset

	def get_query_set(self, context):
		ctype, object_pk = self.get_target_ctype_pk(context)
		queryset = self.get_comments_query_set(context)
		if not queryset.has_root_item():
			self.comments_model.objects.get_root_comment(ctype, object_pk)
			queryset = self.get_comments_query_set(context)
		return queryset


class ThreadedCommentsListNode(ThreadedCommentsBaseNode):
	def render(self, context):
		query_set = self.get_query_set(context)
		context[self.as_varname] = query_set
		return ''


class ThreadedCommentsFormNode(ThreadedCommentsBaseNode):
	def get_form(self, context):
		ctype, object_pk = self.get_target_ctype_pk(context)
		if object_pk:
			return threaded_comments.get_form()(ctype.get_object_for_this_type(pk=object_pk), parent_comment=self.get_root_node(context))
		else:
			return None

	def render(self, context):
		context[self.as_varname] = self.get_form(context)
		return ''


@register.tag
def get_threaded_comments_list(parser, token):
	return ThreadedCommentsListNode.handle_token(parser, token)


@register.simple_tag(takes_context = True)
def render_threaded_comments_toplevel(context, target):
	model_class = target.__class__
	templates = [
		"comments/{0}_{1}_comments_toplevel.html".format(*str(model_class._meta).split('.')),
		"comments/{0}_comments_toplevel.html".format(model_class._meta.app_label),
		"comments/comments_toplevel.html".format(model_class._meta.app_label),
	]
	context.update({"target": target})
	return mark_safe(render_to_string(templates, context))

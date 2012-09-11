# -*- coding: utf-8 -*-

from antispam.fields import AntispamField
from django.forms import Form
import random

class AntispamFormMixin(Form):
	captcha = AntispamField(required = True)

	def generate_antispam(self):
		sign = random.choice(['+', '-', '/', '*'])
		num_1 = 0
		num_2 = 0
		if sign == "+" or sign == "*":
			num_1 = random.randrange(1, 10)
			num_2 = random.randrange(1, 10)
			if sign == "+":
				answer = num_1 + num_2
			if sign == "*":
				answer = num_1 * num_2
		if sign == "-":
			answer = random.randrange(1, 10)
			num_2 = random.randrange(1, 10)
			num_1 = num_2 + answer
		if sign == "/":
			answer = random.randrange(1, 10)
			num_2 = random.randrange(1, 10)
			num_1 = num_2 * answer
		return (u"{0} {1} {2} plus tisíc (číslom) ".format(num_1, sign, num_2), unicode(answer + 1000))

	def set_antispam(self, antispam):
		if 'captcha' in self.fields:
			self.fields['captcha'].widget.attrs['question'] = antispam[0]
			self.fields['captcha'].widget.attrs['answer'] = antispam[1]

	def process_antispam(self, request):
		if request.method == 'GET':
			request.session['antispam'] = self.generate_antispam()
		self.set_antispam(request.session['antispam'])

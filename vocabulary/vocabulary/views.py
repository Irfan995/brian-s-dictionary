from tempfile import template
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


class IndexView(TemplateView):
    template_name = 'index.html'


class AuthenticateView(TemplateView):
    template_name = 'authentication/authenticate.html'

    # def get(self, request):
    #     user = self.request.user
    #     print(user)
    #     if user.is_authenticated:
    #         return HttpResponseRedirect('manage_vocabulary:vocabulary-list')
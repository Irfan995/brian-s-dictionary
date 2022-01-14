from tempfile import template
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class AuthenticateView(TemplateView):
    template_name = 'authentication/authenticate.html'
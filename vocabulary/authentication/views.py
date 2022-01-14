from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class SignupView(TemplateView):
    template_name = 'authentication/signup.html'


class LoginView(TemplateView):
    template_name = 'authentication/login.html'
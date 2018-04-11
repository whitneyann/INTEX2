from django.contrib.auth import authenticate, logout
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from account import models as amod
import re


@view_function
def process_request(request):

    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/homepage/index')








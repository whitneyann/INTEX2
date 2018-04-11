from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from formlib import Formless
from django import forms
import stripe



@view_function
def process_request(request):

    context = {

    }

    return request.dmp.render('cart.html', context)

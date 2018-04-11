from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect, JsonResponse
from formlib import Formless
from django.contrib.auth import authenticate, login
from catalog import models as cmod
from decimal import Decimal
#from catalog.views.api import search
import requests
import math
#
@view_function
def process_request(request):
    myCatalogList = cmod.Category.objects.all()

    productList = cmod.Product.objects.all().filter(status='A').order_by('name')


    response = requests.get(c)

    context = {
        'categories': myCatalogList,
        # 'response':response,
    }
    return JsonResponse(response)


# go to request.get (dictionary of parameters)

# return something.json(dictionary)

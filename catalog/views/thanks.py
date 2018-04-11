from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from django import forms
from formlib.form import Formless
from django.http import HttpResponseRedirect


@view_function
def process_request(request):

    myCatalogList = cmod.Category.objects.all()

    count = request.last_five

    for p in count:
        print(request.last_five)
        if p.status == 'I':
            request.last_five.remove(p)



    # render the format
    context = {
        'categories': myCatalogList,

    }
    return request.dmp.render('thanks.html', context)

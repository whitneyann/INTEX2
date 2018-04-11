from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from catalog import models as cmod
from django.views.generic.edit import DeleteView


@view_function
def process_request(request):
    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])
    except cmod.Product.DoesNotExist:
        return HttpResponseRedirect('/')

    product.status = 'I'
    product.save()

    productList = cmod.Product.objects.filter(status='A')

    context={
            'productList': productList
    }

    return request.dmp.render('/catalog/templates/product.html',
        context
    )




from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from formlib import Formless
from django import forms
import stripe



@view_function
def process_request(request):
    if request.user.is_authenticated:
        pass
    else:
        return HttpResponseRedirect('/account/login/')

    print('oooooooooooooooo11111111')
    cart = cmod.Order.objects.get(user = request.user, status = 'cart')
    cart.recalculate()
    items = cart.active_items(include_tax_item=False)

    taxline = cmod.OrderItem.objects.filter(product__name = "Sales Tax", status = "active").first()
    # taxline = cmod.OrderItem.objects.filter(order = cart, product__name = "Sales Tax", status = "active").first()


    print('ppppppppppppppppppppppppppp', taxline)
    taxprice= taxline.price
    total = cart.total_price
    total = round(total,2)




    context = {
        'items': items,
        'taxline': taxline,
        'total': total,
        'taxprice': taxprice,
    }
        #Render the template
    return request.dmp.render('cart.html', context)

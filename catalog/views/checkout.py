from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from django import forms
from formlib.form import Formless
from django.http import HttpResponseRedirect


@view_function
def process_request(request, cart: cmod.Order = None):
    if request.user.is_authenticated:
        pass
    else:
        return HttpResponseRedirect('/account/login/')

    # Grab the cart
    cart = cmod.Order.objects.get(user=request.user, status='cart')
    cart.recalculate()

    cartTotal = cart.total_price
    cartTotal = round(cartTotal, 2)
    form = checkoutForm(request, cart = cart)
    form.submit_text = None

    cartTotal='{:,.2f}'.format(cartTotal)

    myCatalogList = cmod.Category.objects.all()

    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/catalog/thanks')

    # render the format
    context = {
        'form': form,
        'categories': myCatalogList,
        'totalPrice': cartTotal,
        'cart': cart,

    }
    return request.dmp.render('checkout.html', context)


class checkoutForm(Formless):
    def init(self):

        # INFORMATION FOR THE FORM
        self.fields['address'] = forms.CharField(label='Street Address', max_length=100)
        self.fields['city'] = forms.CharField(label='City', max_length=100)
        self.fields['state'] = forms.CharField(label='State', max_length=50)
        self.fields['zip'] = forms.IntegerField(label='ZIP Code')
        self.fields['phone'] = forms.IntegerField(label='Phone Number')
        self.fields['stripeToken']= forms.CharField(required=True,label="stripeToken", widget=forms.HiddenInput)

    def clean(self):

        try:
            self.cart.finalize(self.cleaned_data.get('stripeToken'))

        except Exception as E:
            raise forms.ValidationError(str(E))

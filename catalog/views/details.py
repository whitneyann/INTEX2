from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from formlib import Formless
from django import forms


@view_function
def process_request(request, product: cmod.Product):
    form = CartForm(request, product=product)
    if form.is_valid():
        print('form is valid')
        form.commit()
        return HttpResponseRedirect('/catalog/cart/')

    if product is None:
        return HttpResponseRedirect('/')

    categoryList = cmod.Category.objects.all()
    productList = cmod.Product.objects.all().filter(status='A')
    myPics = product.image_urls()

    for p in request.last_five:
        if p == product or p.status == 'I':
            request.last_five.remove(p)


    request.last_five.insert(0, product)



    if len(request.last_five) > 6:
        request.last_five.pop()



    # elif (request.last_five.status == 'I'):
    #     request.last_five.pop()

    context = {
        'product': product,
        'categoryList': categoryList,
        'productList': productList,
        'myPics': myPics,
        'form': form,
    }

    return request.dmp.render('details.html',
                              context,
                              )


class CartForm(Formless):
    def init(self):

        # if self.product.status == 'A':
        self.submit_text="Add to Cart"
        if self.request.user.is_authenticated:
            self.cart = self.request.user.get_shopping_cart()

        quanty = []
        for x in range(1, self.product.get_quantity() + 1):
            quanty.append([str(x), str(x)])

        if self.product.__class__.__name__ == 'BulkProduct':
            self.fields['quantity'] = forms.ChoiceField(choices=quanty)
        else:
            self.fields['quantity'] = forms.CharField(initial=1, widget=forms.HiddenInput)




    def clean(self):
        qtycheck = self.cleaned_data.get('quantity')
        qtycheck = int(qtycheck)

        item = self.cart.get_item(self.product, True)
        item.recalculate(0)

        if qtycheck is None:
            raise forms.ValidationError('Please enter a quantity')

        if item.quantity + qtycheck > self.product.get_quantity():
            if self.product.__class__.__name__ == 'BulkProduct':
                raise forms.ValidationError('You can only order ' + str(
                    self.product.get_quantity()) + ' ' + self.product.name + '. You currently have ' + str(item.quantity) + " in your cart.")
            else:
                raise forms.ValidationError('This item is already in your cart.')

        return self.cleaned_data


    def commit(self):

        item = self.cart.get_item(self.product, True)
        q = int(self.cleaned_data.get('quantity'))
        item.recalculate(q)

        # save the new order
        item.save()

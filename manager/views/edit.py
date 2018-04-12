from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from account.models import User
from django.contrib.auth import authenticate, login
from catalog import models as cmod
from django_mako_plus import view_function



@view_function
def process_request(request):
    try:
        product = cmod.Product.objects.get(id=request.dmp.urlparams[0])
    except cmod.Product.DoesNotExist:
        return HttpResponseRedirect('/')

    if product.TITLE == 'Individual':
        product = cmod.IndividualProduct.objects.get(id=request.dmp.urlparams[0])
        form = EditForm(initial={'name':product.name,
                                 'description':product.description,
                                 'price':product.price,
                                 'status':product.status,
                                 'category':product.category,
                                 'type':product.__class__.__name__,
                                 'pid':product.pid},
                        request=request)

    elif product.TITLE == 'Rental':
        product = cmod.RentalProduct.objects.get(id=request.dmp.urlparams[0])
        form = EditForm(initial={'name':product.name,
                                 'description':product.description,
                                 'price':product.price,
                                 'status':product.status,
                                 'category':product.category,
                                 'type':product.__class__.__name__,
                                 'max_rental_days':product.max_rental_days,
                                 'retire_date':product.retire_date},
                        request=request)
    else:
        product = cmod.BulkProduct.objects.get(id=request.dmp.urlparams[0])
        form = EditForm(initial={'name':product.name,
                                 'description':product.description,
                                 'price':product.price,
                                 'status':product.status,
                                 'category':product.category,
                                 'type':product.__class__.__name__,
                                 'quantity':product.quantity,
                                 'reorder_trigger':product.reorder_trigger,
                                 'reorder_quantity':product.reorder_quantity},
                        request=request)

    if form.is_valid():
        form.commit(request)
        return HttpResponseRedirect('/catalog/product/')

    context={
              'form': form,
              'product': product,
        }
    return request.dmp.render('edit.html', context)



class EditForm(Formless):

    def init(self):
       self.fields['type'] = forms.ChoiceField(label="Select Product Type", choices=cmod.Product.TYPE_CHOICES)
       self.fields['name'] = forms.CharField(label='Product Name')
       self.fields['description'] = forms.CharField(label='Product Description')
       self.fields['price'] = forms.DecimalField(label='Product Price',max_digits=7, decimal_places=2)
       self.fields['status'] = forms.ChoiceField(label="Select Product Status", choices=cmod.Product.STATUS_CHOICES)
       self.fields['category'] = forms.ModelChoiceField(label="Select Category", queryset=cmod.Category.objects.all())
       self.fields['quantity'] = forms.IntegerField(required=False)
       self.fields['reorder_trigger'] = forms.IntegerField(required=False)
       self.fields['reorder_quantity'] = forms.IntegerField(required=False)
       self.fields['max_rental_days'] = forms.IntegerField(required=False)
       self.fields['retire_date']=forms.DateField(required=False)
       self.fields['pid']=forms.CharField(required=False)

    def clean(self):

        if self.cleaned_data.get('type') == 'IndividualProduct':

            myPID=self.cleaned_data.get('pid')

            if myPID is None:
                raise forms.ValidationError('This product needs a Product ID')

        elif self.cleaned_data.get('type') == 'RentalProduct':

            maxRental = self.cleaned_data.get('max_rental_days')
            retire = self.cleaned_data.get('retire_date')

            if maxRental is None:
                raise forms.ValidationError('Must fill out the max rental field')
            if retire is None:
                raise forms.ValidationError('This product needs a retire date')

        else:

            quan = self.cleaned_data.get('quantity')
            retrig = self.cleaned_data.get('reorder_trigger')
            requan = self.cleaned_data.get('reorder_quantity')

            if quan is None:
                raise forms.ValidationError('Must fill out the quantity field')
            if retrig is None:
                raise forms.ValidationError('Must fill out the reorder trigger field')
            if requan is None:
                raise forms.ValidationError('Must fill out the reorder quantity field')
            if quan <= 1:
                raise forms.ValidationError('Please enter a quantity greater than 1 for bulk items ')

        return self.cleaned_data


#commit it LAST
    def commit(self, request):
        #self.cleaned_data.title

        if (self.cleaned_data.get('type') == 'IndividualProduct'):
            myProduct = cmod.IndividualProduct.objects.get(id=request.dmp.urlparams[0])
            myProduct.TITLE = self.cleaned_data.get('title')
            myProduct.status = self.cleaned_data.get('status')
            myProduct.name = self.cleaned_data.get('name')
            myProduct.description = self.cleaned_data.get('description')
            myProduct.category = self.cleaned_data.get('category')
            myProduct.price = self.cleaned_data.get('price')
            myProduct.pid = self.cleaned_data.get('pid')
            myProduct.save()

        elif (self.cleaned_data.get('type') == 'RentalProduct'):
            myProduct = cmod.RentalProduct.objects.get(id=request.dmp.urlparams[0])
            myProduct.TITLE = self.cleaned_data.get('title')
            myProduct.status = self.cleaned_data.get('status')
            myProduct.name = self.cleaned_data.get('name')
            myProduct.description = self.cleaned_data.get('description')
            myProduct.category = self.cleaned_data.get('category')
            myProduct.price = self.cleaned_data.get('price')
            myProduct.max_rental_days = self.cleaned_data.get('max_rental_days')
            myProduct.retire_date = self.cleaned_data.get('retire_date')
            myProduct.save()

        else:
            myProduct = cmod.BulkProduct.objects.get(id=request.dmp.urlparams[0])
            myProduct.TITLE = self.cleaned_data.get('title')
            myProduct.status = self.cleaned_data.get('status')
            myProduct.name = self.cleaned_data.get('name')
            myProduct.description = self.cleaned_data.get('description')
            myProduct.category = self.cleaned_data.get('category')
            myProduct.price = self.cleaned_data.get('price')
            myProduct.quantity = self.cleaned_data.get('quantity')
            myProduct.reorder_trigger = self.cleaned_data.get('reorder_trigger')
            myProduct.reorder_quantity = self.cleaned_data.get('reorder_quantity')
            myProduct.save()


        HttpResponseRedirect('/catalog/templates/product.html')

from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as cmod




@view_function
def process_request(request):

    #process the form
    form = CreateForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/catalog/product/')

    context={
              'form': form,
        }

    return request.dmp.render('create.html', context)



class CreateForm(Formless):


    def init(self):

       self.fields['type'] = forms.ChoiceField(label = "Product Type",choices = cmod.Product.TYPE_CHOICES)
       self.fields['category'] = forms.ModelChoiceField(label="Select Category", queryset=cmod.Category.objects.all())
       self.fields['name'] = forms.CharField(label='Product Name')
       self.fields['description'] = forms.CharField(label='Product Description')
       self.fields['price'] = forms.DecimalField(label='Product Price',max_digits=7, decimal_places=2)
       self.fields['status'] = forms.ChoiceField(label="Select Product Status", choices=cmod.Product.STATUS_CHOICES)
       self.fields['pid'] = forms.CharField(label='Product ID', required=False)
       self.fields['quantity'] = forms.IntegerField(label='Quantity', required=False)
       self.fields['reorder_trigger'] = forms.IntegerField(required=False)
       self.fields['reorder_quantity'] = forms.IntegerField(required=False)
       self.fields['max_rental_days'] = forms.IntegerField(required=False)
       self.fields['retire_date']=forms.DateField(required=False)


    # def clean_pid(self):
    #     #get the pid
    #     idcheck = self.cleaned_data.get('id')
    #
    #     # Check to see if any products already exist with this pid.
    #     if cmod.Product.objects.filter(id=idcheck).count() > 0:
    #         raise forms.ValidationError('This product ID is already in use.')
    #
    #     return idcheck

    def clean(self):

        if self.cleaned_data.get('type') == 'IndividualProduct':

            myPID=self.cleaned_data.get('pid')
            idcheck = self.cleaned_data.get('pid')

            if myPID is None:
                raise forms.ValidationError('This product needs a Product ID')
            if cmod.IndividualProduct.objects.filter(pid=idcheck).count() > 0:
                raise forms.ValidationError('This product ID is already in use.')

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
    def commit(self):
        #self.cleaned_data.title

        if (self.cleaned_data.get('type') == 'IndividualProduct'):
            myProduct = cmod.IndividualProduct()
            myProduct.TITLE = self.cleaned_data.get('title')
            myProduct.status = self.cleaned_data.get('status')
            myProduct.name = self.cleaned_data.get('name')
            myProduct.description = self.cleaned_data.get('description')
            myProduct.category = self.cleaned_data.get('category')
            myProduct.price = self.cleaned_data.get('price')
            myProduct.pid = self.cleaned_data.get('pid')
            myProduct.save()

        elif (self.cleaned_data.get('type') == 'RentalProduct'):
            myProduct = cmod.RentalProduct()
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
            myProduct = cmod.BulkProduct()
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

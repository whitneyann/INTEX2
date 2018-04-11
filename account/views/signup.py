from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from account.models import User
from django.contrib.auth import authenticate, login
import re



@view_function
def process_request(request):
    #process the form
    form = SignupForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/')


    return request.dmp.render('signup.html', {'form': form,})



class SignupForm(Formless):
    def init(self):
        self.fields['first_name'] = forms.CharField(label='First Name')
        self.fields['last_name'] = forms.CharField(label='Last Name')
        self.fields['email'] = forms.EmailField(label='Email')
        self.fields['password'] = forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput)
        self.fields['password2'] = forms.CharField(label='Password 2', widget=forms.PasswordInput)
        self.fields['birthdate'] = forms.DateField(label='Date of Birth')
        self.fields['address'] = forms.CharField(label='Address')
        self.fields['city'] = forms.CharField(label='City')
        self.fields['state'] = forms.CharField(label='State')
        self.fields['zipcode'] = forms.IntegerField(label='ZipCode')


    def clean_password(self):
        #get password
        Mypassword = self.cleaned_data.get('password')

        #check to ensure it has a #
        if re.search('\d', Mypassword) is None:
            raise forms.ValidationError('Your password must contain a number')

        return Mypassword


    def clean_email(self):
        #get the email
        emailcheck = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        if User.objects.filter(email=emailcheck).count() > 0:
            raise forms.ValidationError('This email address is already in use.')

        return emailcheck

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            # show an error message: no soup for you
            print('>>>>>Less than 18!')
        return age

    def clean(self):
        #for checking the entire form - usually two variables at once
        #password and password2 (are they matching?)
        pw1 = self.cleaned_data.get('password')
        pw2 = self.cleaned_data.get('password2')
        if pw1 != pw2:
            #yell at user!
            raise forms.ValidationError('Uh-oh! Passwords do not match!')
        return self.cleaned_data

    #commit it LAST
    def commit(self):

        #make the user
        myUser = User()

        #load up the user
        myUser.first_name = self.cleaned_data.get('first_name')
        myUser.last_name = self.cleaned_data.get('last_name')
        myUser.email = self.cleaned_data.get('email')
        myUser.birthdate = self.cleaned_data.get('birthdate')
        myUser.address = self.cleaned_data.get('address')
        myUser.city = self.cleaned_data.get('city')
        myUser.state = self.cleaned_data.get('state')
        myUser.zipcode = self.cleaned_data.get('zipcode')
        myUser.set_password(self.cleaned_data.get('password'))

        #save the new user
        myUser.save()

        user = authenticate(email = self.cleaned_data.get('email'), password = self.cleaned_data.get('password'))
        login(self.request, user)

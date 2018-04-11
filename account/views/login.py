from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms



@view_function
def process_request(request):

    #process the form
    form = loginForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/')

    #render the template
    return request.dmp.render('login.html', {
        'form': form,
    })

class loginForm(Formless):
    def init(self):
        '''Add fields to this form'''
        self.fields['email'] = forms.CharField(label='Email Address')
        self.fields['password'] = forms.CharField(label='Password', widget=forms.PasswordInput())
        self.user = None

    def clean(self):
        self.user = authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))
        if self.user is None:
            raise forms.ValidationError('Invalid email or password.')
        return self.cleaned_data

    def commit(self):
        '''Actually process the form'''
        login(self.request, self.user)

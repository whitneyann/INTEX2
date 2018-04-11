from django.db import models
from cuser.models import AbstractCUser
from catalog import models as cmod

# Create your models here.

class User(AbstractCUser):
        birthdate = models.DateField(blank=True, null=True)
        address = models.TextField(blank=True, null=True)
        city = models.TextField(blank=True, null=True)
        state = models.TextField(blank=True, null=True)
        zipcode = models.TextField(blank=True, null=True)

        def get_purchases(self):
                return ['Roku Ultimate 2000', 'USB Cable', 'Candy Bar']

        def get_shopping_cart(self):

                cart = cmod.Order.objects.filter(status='cart', user=self).first()

                if cart is None:
                        cart = cmod.Order()
                        cart.status = 'cart'
                        cart.user = self
                        cart.save()
                # else:
                #     cart = cmod.Order.objects.filter(status='cart', user=self).first()
                return cart

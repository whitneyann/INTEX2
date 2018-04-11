from polymorphic.models import PolymorphicModel
from django.conf import settings
from django.db import models, transaction
from django.conf import settings
from django.forms.models import model_to_dict
from polymorphic.models import PolymorphicModel
from decimal import Decimal
from django.http import HttpResponseRedirect
from datetime import datetime
import stripe
import yagmail



class Category(models.Model):
        create_date = models.DateTimeField(auto_now_add=True)
        last_modified = models.DateTimeField(auto_now=True)
        name = models.TextField(null=True, blank=True)
        description = models.TextField(null=True, blank=True)

        def __str__(self):
                return self.name


#######################################################################
###   Products


#pip3 install django-polymorphic
class Product(PolymorphicModel):
        '''a bulk, individual, or rental product'''
        TYPE_CHOICES = (
               ('BulkProduct', 'Bulk Product'),
               ('RentalProduct', 'Rental Product'),
               ('IndividualProduct', 'Individual Product'),
        )
        STATUS_CHOICES = (
                ('A', 'Active'),
                ('I', 'Inactive'),
        )

        create_date = models.DateTimeField(auto_now_add=True)
        last_modified = models.DateTimeField(auto_now=True)
        name = models.TextField()
        description = models.TextField()
        category = models.ForeignKey('Category', on_delete=models.CASCADE)
        price = models.DecimalField(max_digits=7, decimal_places=2)
        status = models.TextField(choices=STATUS_CHOICES, default='A')

        #this method is now in every subclass
        def get_quantity(self):
                return 1

        def image_url(self):
                '''Always returns one image'''
                pi = self.images.first()
                if pi is None:
                        return settings.STATIC_URL + 'catalog/media/products/notfound.jpg'
                else:
                        url=settings.STATIC_URL + 'catalog/media/products/' + pi.filename
                return url

        def image_urls(self):
                '''Returns a LIST of images'''
                pi = self.images.all()
                urls = []
                if pi is None:
                        urls.append(settings.STATIC_URL + 'catalog/media/products/notfound.jpg')
                else:
                        for m in pi:
                                urls.append(settings.STATIC_URL + "catalog/media/products/" + m.filename)
                return urls


class BulkProduct(Product):
        '''a bulk product'''
        TITLE = 'Bulk'
        quantity = models.IntegerField()
        reorder_trigger = models.IntegerField(default=0)
        reorder_quantity = models.IntegerField(default=0)

        def get_quantity(self):
                return self.quantity


class IndividualProduct(Product):
        '''an individual product'''
        TITLE = 'Individual'
        pid = models.TextField(default='NA')


class RentalProduct(Product):
        '''a rental product'''
        TITLE = 'Rental'
        max_rental_days = models.IntegerField(default=0)
        retire_date=models.DateField(null=True, blank=True)


class ProductImage(models.Model):
        filename = models.TextField()
        product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)






#######################################################################
###   Orders

class Order(models.Model):
    '''An order in the system'''
    STATUS_CHOICES = (
        ( 'cart', 'Shopping Cart' ),
        ( 'payment', 'Payment Processing' ),
        ( 'sold', 'Finalized Sale' ),
    )
    order_date = models.DateTimeField(auto_now_add=True)
    name = models.TextField(blank=True, default="Shopping Cart")
    status = models.TextField(choices=STATUS_CHOICES, default='cart', db_index=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99
    user = models.ForeignKey('account.User', related_name='orders',  on_delete=models.CASCADE)
    # shipping information
    ship_date = models.DateTimeField(null=True, blank=True)
    ship_tracking = models.TextField(null=True, blank=True)
    ship_name = models.TextField(null=True, blank=True)
    ship_address = models.TextField(null=True, blank=True)
    ship_city = models.TextField(null=True, blank=True)
    ship_state = models.TextField(null=True, blank=True)
    ship_zip_code = models.TextField(null=True, blank=True)

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'Order {}: {}: {}'.format(self.id, self.user.get_full_name(), self.total_price)

    def active_items(self, include_tax_item=True):
        '''Returns the active items on this order'''
        if include_tax_item:
            act = OrderItem.objects.filter(order = self, status = 'active')
        else:
            act = OrderItem.objects.filter(order=self, status = 'active').exclude(product__name ="Sales Tax")

        return act


    def get_item(self, product, create=False):
        '''Returns the OrderItem object for the given product'''
        item = OrderItem.objects.filter(order=self, product=product).first()
        if item is None and create:
            item = OrderItem.objects.create(order=self, product=product, price=product.price, quantity=0)
        elif create and item.status != 'active':
            item.status = 'active'
            item.quantity = 0
        if item is not None:
            item.recalculate()
        item.save()
        return item


    def num_items(self):
        '''Returns the number of items in the cart'''
        return sum(self.active_items(include_tax_item=False).values_list('quantity', flat=True))


    def recalculate(self):
        '''
        Recalculates the total price of the order,
        including recalculating the taxable amount.

        Saves this Order and all child OrderLine objects.
        '''
        # iterate the order items (not including tax item) and get the total price
        # call recalculate on each item
        subtotal = Decimal(0)
        for item in self.active_items():
            item.recalculate()
            subtotal = item.extended + subtotal

        # update/create the tax order item (calculate at 7% rate)
        taxitem = OrderItem.objects.filter(product__name='Sales Tax').first()
        print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj',taxitem)
        if taxitem is None:
            # taxitem = OrderItem()
            # taxitem.Order=self
            taxitem.product = self.get_item(Product.objects.filter(id=73).first(), True)
            taxitem.status='active'
        #
        # if taxitem is None:
        #     taxitem = self.get_item(Product.objects.filter(id=87).first(), True)
        taxitem.price = subtotal*(Decimal(0.07))
        taxitem.save()


        # update the total and save
        self.total_price = taxitem.price + subtotal
        self.save()

    def finalize(self, stripe_charge_token):
        '''Runs the payment and finalizes the sale'''
        with transaction.atomic():
            # recalculate just to be sure everything is updated
            self.recalculate()
            self.save()
            items_bought = ''
            # check that all products are available
            for x in self.active_items():
                if x.quantity > x.product.get_quantity():
                    raise ValueError('Sorry, we do not have enough ' + x.product.name + 'in stock.')

            # contact stripe and run the payment (using the stripe_charge_token)
            charge = stripe.Charge.create(
                amount = int(self.total_price * 100),
                currency = "usd",
                description = "sample charge",
                source = stripe_charge_token,
            )
            # finalize (or create) one or more payment objects
            payment, created = Payment.objects.get_or_create(order=self)
            payment.payment_date = datetime.now()
            payment.amount = self.total_price
            payment.validation_code = charge['id']
            payment.save()

            # set order status to sold and save the order
            self.status = 'sold'
            self.save()
            literallykillme = 0
            tax_total=0
            # update product quantities for BulkProducts
            for x in self.active_items():
                if x.product.TITLE =='Bulk':
                    x.product.quantity -= x.quantity
                    if x.product.quantity == 0:
                        x.product.status ='I'

            # update status for IndividualProducts
                else:
                    x.product.status='I'

                x.product.save()
                x.save()

                literallykillme = literallykillme + 1

                if len(self.active_items()) == 1:
                    items_bought = str(x.product.name)
                elif literallykillme == len(self.active_items()):
                    items_bought = items_bought + 'and ' + str(x.product.name)
                else:
                    items_bought = items_bought + str(x.product.name) + ', '

                # items_bought = items_bought + ', ' + x.product.name # fix beginning comma
            tax_total= (self.total_price/107)*7
            yag = yagmail.SMTP('shopfomo.me@gmail.com', 'POOPonast1ck')
            # contents = 'Thank you for placing an order with FOMO today! Your Order Number is %s and contains %s. Your order has been placed on %s for a total of $%s including $%s sales tax.' % str(self.id), items_bought, str(self.order_date), str(self.total_price),
            contents = 'Thank you for placing an order with FOMO today! Your cost is $%.2f and contains %s. Your Sales Tax was $%.2f. You ordered it on %s. Your Order is being shipped. Please allow 2-5 business days for arrival.' % ((self.total_price), str(items_bought), (tax_total), (self.order_date.strftime('%m/%d/%y')))
            subject = 'Order %s Confirmation' % self.id
            recipient = self.user.email
            yag.send(recipient, subject, contents)

class OrderItem(models.Model):
    '''A line item on an order'''
    STATUS_CHOICES = (
        ( 'active', 'Active' ),
        ( 'deleted', 'Deleted' ),
    )
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    status = models.TextField(choices=STATUS_CHOICES, default='active', db_index=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99
    quantity = models.IntegerField(default=0)
    extended = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'OrderItem {}: {}: {}'.format(self.id, self.product.name, self.extended)


    def recalculate(self, qty=0):
        '''Updates the order item's price, quantity, extended'''
        # update the price if it isn't already set and we have a product
        if self.price is None:
            self.price = 100

        if self.product.name != 'Sales Tax':
            self.price = self.product.price

        # default the quantity to 1 if we don't have a quantity set
        if self.quantity is None:
            self.quantity = 1
        self.quantity = self.quantity + qty

        # calculate the extended (price * quantity)
        self.extended = self.price * self.quantity

        # save the changes
        self.save()

class Payment(models.Model):
    '''A payment on a sale'''
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2) # max number is 999,999.99
    validation_code = models.TextField(null=True, blank=True)

from django.contrib import admin
from .models import Category, Product, BulkProduct, IndividualProduct, RentalProduct, Order, OrderItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(BulkProduct)
admin.site.register(IndividualProduct)
admin.site.register(RentalProduct)
admin.site.register(Order)
admin.site.register(OrderItem)




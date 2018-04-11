from django.db import models

# Create your models here.
class Category(models.Model):
        create_date = models.DateTimeField(auto_now_add=True)
        last_modified = models.DateTimeField(auto_now=True)

from django.core import serializers
from django.db import models

# Create your models here.
class Customer(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField()

    updated_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.TextField()

    name = models.CharField(max_length=400,blank=False, default='')
    phone = models.TextField(blank=False, default='')
    email=models.TextField(blank=False, default='')

    deleted = models.BooleanField(default=False)

    ##########################################################################
    def toJSON(self):
        return serializers.serialize("json", self)    
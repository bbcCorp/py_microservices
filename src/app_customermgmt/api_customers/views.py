import logging

from rest_framework import generics
from api_customers.models import Customer
from api_customers.serializers import SimpleCustomerSerializer



# Create your views here.

class CustomerList(generics.ListCreateAPIView):
    """
    List all code customers, or create a new customer.
    Supports GET and POST
    """
    queryset = Customer.objects.all()
    serializer_class = SimpleCustomerSerializer
      
class CustomerDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a code customer.
    Supports GET (by id), PUT and DELETE
    """
    queryset = Customer.objects.all()
    serializer_class = SimpleCustomerSerializer
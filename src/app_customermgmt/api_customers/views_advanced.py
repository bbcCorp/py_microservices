import os
import sys
import copy
import json
from datetime import datetime

from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_customers.models import Customer
from api_customers.serializers import CustomerSerializer

import api_customers.settings as SETTINGS

## Import external libraries outside the Django project
curpath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join (curpath, "../../")))
from app_messaging_utils import SimpleKafkaProducer
from app_models import AppEventType, AppEventArgs

kafka_config= SETTINGS.message_producer
kafkaProducer = SimpleKafkaProducer()
kafkaProducer.configure(config=kafka_config) 

# This allows fine grained control over the API views

###############################################################################
class CustomerList(APIView):
    """
        List all code customers, or create a new customer.
    """
    ###########################################################################
    def get(self, request, format=None):
        '''
            get all records
        '''
        # customers = Customer.objects.all()
        customers = Customer.objects.filter(deleted=False)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    ###########################################################################
    def post(self, request, format=None):
        '''
            create record. generate INSERT event once successful.

        '''
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Push message to event queue
            event = AppEventArgs(
                app_event_type=AppEventType.Insert,
                after_change=serializer.data)
            kafkaProducer.produce(topic=SETTINGS.message_topic,message=event.toJSON())
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

############################# End of CustomerList #############################


###############################################################################
class CustomerDetails(APIView):
    """
    Retrieve, update or delete a code customer.

    This class also generates update/delete events

    """
    def get_object(self, pk):        
        try:
            return Customer.objects.get(pk=pk,deleted = False)
        except Customer.DoesNotExist:
            raise Http404

    ###########################################################################
    def get(self, request, pk, format=None):
        '''
            get record by id
        '''
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    ###########################################################################
    def put(self, request, pk, format=None):
        '''
            update record by id. generate UPDATE event once successful.
        '''
        customer = self.get_object(pk)

        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Push message to event queue
            event = AppEventArgs(
                app_event_type=AppEventType.Update,
                after_change=serializer.data)
            kafkaProducer.produce(topic=SETTINGS.message_topic,message= event.toJSON())

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ###########################################################################
    def delete(self, request, pk, format=None):
        '''
            delete record by id. generate DELETE event once successful.
        '''
        customer = self.get_object(pk)

        before_update = copy.deepcopy(customer)
        # customer.delete()
        customer.deleted = True
        customer.updated_on = datetime.utcnow()
        customer.save()

        # Push message to event queue
        event = AppEventArgs(
                app_event_type=AppEventType.Delete,
                before_change=CustomerSerializer(before_update).data,
                after_change=CustomerSerializer(customer).data)
        
        kafkaProducer.produce(topic=SETTINGS.message_topic,message=event.toJSON())

        return Response(status=status.HTTP_204_NO_CONTENT)       

########################## End of CustomerDetails #############################
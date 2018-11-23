import pytest
from rest_framework.test import APIRequestFactory
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

class TestCustomer:
    def test_model(self):
        factory = APIRequestFactory()
        
        request = factory.post('/api/customers', { 
            "name":"test2", 
            "phone":"1-800-test2", 
            "email":"test2@email.com" }, format='json')

        
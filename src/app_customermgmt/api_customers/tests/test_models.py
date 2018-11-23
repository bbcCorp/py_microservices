import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

class TestCustomer:
    def test_model(self):
        obj = mixer.blend('api_customers.models.Customer')
        assert obj.pk == 1, 'Should create a customer instance'
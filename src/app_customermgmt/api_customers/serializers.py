from datetime import datetime
from rest_framework import serializers
from api_customers.models import Customer

class SimpleCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'phone', 'email')

class CustomerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    name = serializers.CharField(required=True, allow_blank=False, max_length=400)
    phone = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True)

    deleted = serializers.BooleanField(read_only=True)
    created_on = serializers.DateTimeField(read_only=True)
    created_by = serializers.CharField(read_only=True)
    updated_on = serializers.DateTimeField(read_only=True)
    updated_by = serializers.CharField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Customer` instance, given the validated data.
        """
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Customer` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.updated_on = datetime.utcnow()

        instance.save()
        return instance    
from api.models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = "__all__"
        partial = True

class PoSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    delivery_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    acknowledgement_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required = False)
    issue_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required = False)
    class Meta:
        model = PurchaseOrder
        fields = "__all__"

    def error_response(self, errors):
        return {
            'errors': errors
        }

    def validate(self, data):
        data = super().validate(data)
        delivery_date = data.get('delivery_date')
        order_date = data.get('order_date')

        if not order_date:  
            order_date = self.instance.order_date
        if not delivery_date:  
            delivery_date = self.instance.delivery_date

        if delivery_date < order_date:
            raise serializers.ValidationError({"error": "delivery_date date cannot date before order_date."})
        
        return data
    
class MetricsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vendor
        exclude = ["contact_details", "address", "name"]

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user
    
class HistorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = History
        fields = "__all__"
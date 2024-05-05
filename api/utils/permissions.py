from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from api.models import PurchaseOrder

class DenyManualMetrics(permissions.BasePermission):
    message = "Metrics fields cannot be set manually"

    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH']:
            disallowed_fields = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fullfillment_rate']
            data = request.data
            for field in disallowed_fields:
                if field in data:
                    raise PermissionDenied(detail=self.message)
        return True
    
class AttributePermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        attrs = ["issue_date", "acknowledgement_date"]
        for attr in attrs:
            if attr in request.data :
                raise PermissionDenied(detail=f"{attr} cannot be set manually")
            
        return True
    
    def has_object_permission(self, request, view, obj):
        attrs = ["order_date", "delivery_date"]
        if obj.status == 'completed':
            for attr in attrs:
                if attr in request.data :
                    raise PermissionDenied(detail=f"{attr} cannot be edited for a completed order. Retry after changing status to pending.")
            
        return True
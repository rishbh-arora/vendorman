from rest_framework import permissions, authentication, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, History

from django.utils import timezone
from .utils.serializers import VendorSerializer, PoSerializer, HistorySerializer
from .utils.permissions import DenyManualMetrics, AttributePermissions

from .utils.filter import PurchaseOrderFilter
from django_filters.rest_framework import DjangoFilterBackend

class PurchaseViewset(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PoSerializer
    permission_classes = [permissions.IsAdminUser, AttributePermissions]
    authentication_classes = [authentication.TokenAuthentication]
    lookup_field = "po_number"
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vendor']

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, po_number=None):
        purchase_order = self.get_object()
        if purchase_order.acknowledgement_date:
            return Response({"message": "Purchase order already acknowledged"}, status=status.HTTP_400_BAD_REQUEST)
        purchase_order.acknowledgement_date = timezone.now()
        purchase_order.save()
        
        vendor = purchase_order.vendor
        vendor.update_response_time()
        vendor.save()
        return Response({"message": "Purchase order acknowledged successfully."})
    
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


    
class VendorViewset(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAdminUser, DenyManualMetrics]
    authentication_classes = [authentication.TokenAuthentication]
    lookup_field = "vendor_code"

    @action(detail=True, methods=['get'])
    def performance(self, request, vcode):
        vendor = self.get_object()
        serializer = self.get_serializer(vendor, many=False)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

class HistoryViewset(viewsets.ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.TokenAuthentication]
    lookup_field = "vendor_code"
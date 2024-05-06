from rest_framework import permissions, authentication, viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone
from .models import Vendor, PurchaseOrder, History
from django.contrib.auth.models import User
from .utils.serializers import *
from .utils.permissions import DenyManualMetrics, AttributePermissions
from .utils.filters import HistoryFilter, PurchaseOrderFilter

from django_filters.rest_framework import DjangoFilterBackend

class PurchaseViewset(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PoSerializer
    permission_classes = [permissions.IsAuthenticated, AttributePermissions]
    authentication_classes = [authentication.TokenAuthentication]
    lookup_field = "po_number"
    filter_backends = [DjangoFilterBackend]
    filterset_class = PurchaseOrderFilter

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
    permission_classes = [permissions.IsAuthenticated, DenyManualMetrics]
    authentication_classes = [authentication.TokenAuthentication]
    lookup_field = "vendor_code"

    @action(detail=True, methods=['get'])
    def performance(self, request, vendor_code=None):
        print("vendor_code")
        if vendor_code:
            vendor = self.get_object()
            serializer = MetricsSerializer(vendor, many=False)
            return Response(serializer.data)
        
        data = self.get_queryset()
        serializer = MetricsSerializer(data, many=True)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

class HistoryViewset(viewsets.ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HistoryFilter

class UserViewset(CreateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    lookup_field = 'username'

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, username, *args, **kwargs):
        user = self.get_object()
        if user.is_staff:
            return Response({"message": "Cannot destroy admin user"}, status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)
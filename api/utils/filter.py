import django_filters
from api.models import PurchaseOrder

class PurchaseOrderFilter(django_filters.FilterSet):
    vendor_id = django_filters.CharFilter(field_name='vendor__id')

    class Meta:
        model = PurchaseOrder
        fields = ['vendor_id']
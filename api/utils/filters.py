import django_filters
from api.models import History, PurchaseOrder

class HistoryFilter(django_filters.FilterSet):
    vendor = django_filters.NumberFilter(field_name='vendor__vendor_code')

    class Meta:
        model = History
        fields = ['vendor']

class PurchaseOrderFilter(django_filters.FilterSet):
    vendor = django_filters.CharFilter(field_name='vendor__vendor_code')

    class Meta:
        model = PurchaseOrder
        fields = ['vendor']

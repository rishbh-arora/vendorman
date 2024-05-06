from django.db import models
from django.utils import timezone
from django.db.models import Avg, JSONField, F
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator


class History(models.Model):
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name='fk_history_vendor')
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_rate = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.vendor.name

class PurchaseOrder(models.Model):

    status_levels = [
        ('pending', 'pending'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled'),
    ]

    po_number = models.CharField(max_length=10, primary_key = True)
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name="fk_po_vendor", to_field='vendor_code')
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = JSONField()
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(choices=status_levels, default="pending", max_length=9)
    quality_rating = models.FloatField(null = True)
    issue_date = models.DateTimeField(auto_now_add = True)
    acknowledgement_date = models.DateTimeField(null=True)
    on_time = models.BooleanField(null=True)
    old_status = None
    complete_without_acknowledge = None


    def snapshot(self, vendor):
        History.objects.create(
                            vendor = vendor,
                            on_time_delivery_rate = vendor.on_time_delivery_rate,
                            quality_rating_rate = vendor.quality_rating_avg,
                            average_response_time = vendor.average_response_time,
                            fulfillment_rate = vendor.fullfillment_rate
                        )
    def __str__(self) -> str:
        return self.po_number

class Vendor(models.Model):
    name = models.CharField(max_length=30)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=10, primary_key=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fullfillment_rate = models.FloatField(default=0)

    def update_delivery_rate(self, on_time_delivery=False, delete=False):
        orders = PurchaseOrder.objects.filter(status = 'completed', vendor = self)
        on_time = orders.filter(on_time = True).count()
        total = orders.count()
        if not delete:
            total += 1
            if on_time_delivery:
                on_time += 1
        elif not total:
            self.on_time_delivery_rate = 0
            return
        self.on_time_delivery_rate = (on_time / total) * 100

    def update_quality_rate(self):
        quality_rating_avg = PurchaseOrder.objects.filter(vendor=self).aggregate(avg_qr=Avg('quality_rating'))['avg_qr']
        if not quality_rating_avg:
            self.quality_rating_avg = 0
            return
        
        self.quality_rating_avg = quality_rating_avg


    def update_response_time(self):
        orders = PurchaseOrder.objects.filter(
            acknowledgement_date__isnull=False,
            vendor=self
        )
        t = orders.aggregate(avg_res_time=Avg(F('acknowledgement_date') - F('issue_date')))['avg_res_time']
        if not t:
            self.average_response_time = 0
            return
        
        t = t.total_seconds()
        self.average_response_time = t / (24 * 3600)

    def update_fullfilment_rate(self):
        all_orders = PurchaseOrder.objects.filter(vendor = self)
        fulfilled = all_orders.filter(status = 'completed')
        if not all_orders.count():
            self.fullfillment_rate = 0
            return
        
        self.fullfillment_rate = (fulfilled.count() / all_orders.count())

    def __str__(self) -> str:
        return self.name



@receiver(pre_save, sender=PurchaseOrder)
def pre_updates(sender, instance: PurchaseOrder, **kwargs):
    try:
        old_status = PurchaseOrder.objects.get(pk = instance.pk)
        instance.old_status = old_status

        if old_status != instance.status and instance.status == "completed":
            vendor = instance.vendor
            if not instance.acknowledgement_date:
                instance.acknowledgement_date = timezone.now()
                instance.complete_without_acknowledge = True
            
            instance.on_time = timezone.now() <= instance.delivery_date
            vendor.update_delivery_rate(instance.on_time, False)
            instance.delivery_date = timezone.now()
            
            vendor.save()
    except:
        pass


@receiver(post_save, sender=PurchaseOrder)
def post_updates(sender, instance: PurchaseOrder, created,  **kwargs):
    vendor = instance.vendor
    vendor.update_fullfilment_rate()
    if not created:
        if instance.old_status != instance.status:
            if instance.status == 'completed':
                if instance.quality_rating:
                    vendor.update_quality_rate()
                if instance.complete_without_acknowledge:
                    vendor.update_response_time()
                vendor.save()
            instance.snapshot(vendor)

@receiver(post_delete, sender=PurchaseOrder)
def delete(sender, instance: PurchaseOrder,  **kwargs):
    vendor = instance.vendor
    vendor.update_fullfilment_rate()
    vendor.update_response_time()
    vendor.update_quality_rate()
    vendor.update_delivery_rate(delete = True)
    vendor.save()
    

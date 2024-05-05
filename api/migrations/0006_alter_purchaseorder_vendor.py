# Generated by Django 5.0.4 on 2024-05-05 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_purchaseorder_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_po_vendor', to='api.vendor'),
        ),
    ]

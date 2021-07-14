# Generated by Django 2.2.8 on 2021-07-14 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_order_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='amount',
            field=models.FloatField(default=10),
        ),
        migrations.AddField(
            model_name='coupon',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]

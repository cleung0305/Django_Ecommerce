# Generated by Django 2.2.8 on 2021-07-19 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20210719_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='description',
            field=models.CharField(default='New Promo!', max_length=100),
        ),
    ]
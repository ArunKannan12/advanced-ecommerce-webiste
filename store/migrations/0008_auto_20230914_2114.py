# Generated by Django 3.2.20 on 2023-09-14 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20230912_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='new_price',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.IntegerField(null=True),
        ),
    ]
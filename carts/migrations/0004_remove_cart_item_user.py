# Generated by Django 3.2.20 on 2023-09-05 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_cart_item_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart_item',
            name='user',
        ),
    ]
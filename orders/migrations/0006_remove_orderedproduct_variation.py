# Generated by Django 3.2.20 on 2023-09-12 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20230907_1012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderedproduct',
            name='variation',
        ),
    ]

# Generated by Django 3.2.5 on 2021-08-13 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0023_auto_20210812_1933'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='trasaction_id',
            new_name='transaction_id',
        ),
    ]

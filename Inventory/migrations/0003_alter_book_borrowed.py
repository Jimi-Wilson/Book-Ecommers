# Generated by Django 3.2.5 on 2021-07-21 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0002_auto_20210721_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='borrowed',
            field=models.BooleanField(default=False, null=True),
        ),
    ]

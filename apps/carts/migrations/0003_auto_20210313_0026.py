# Generated by Django 3.1.7 on 2021-03-12 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_auto_20210228_1901'),
        ('carts', '0002_auto_20210307_1937'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('item', 'cart')},
        ),
    ]

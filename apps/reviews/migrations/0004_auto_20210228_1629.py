# Generated by Django 3.1.7 on 2021-02-28 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20210228_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='published_at',
            field=models.DateTimeField(blank=True, default=''),
        ),
    ]
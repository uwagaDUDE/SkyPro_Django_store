# Generated by Django 4.2.2 on 2023-07-02 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='productversion',
            name='version',
            field=models.IntegerField(default=1),
        ),
    ]

# Generated by Django 5.1.6 on 2025-02-15 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0002_alter_user_phone_number_productimage_producttype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(blank=True, null=True, related_name='product', to='Api.productimage'),
        ),
    ]

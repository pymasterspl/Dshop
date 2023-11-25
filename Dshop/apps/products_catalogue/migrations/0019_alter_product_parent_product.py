# Generated by Django 4.2.7 on 2023-11-15 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products_catalogue', '0018_product_parent_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='parent_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products_catalogue.product'),
        ),
    ]
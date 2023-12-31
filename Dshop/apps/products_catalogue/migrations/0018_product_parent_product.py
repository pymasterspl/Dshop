# Generated by Django 4.2.7 on 2023-11-11 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("products_catalogue", "0017_merge_20231106_1241"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="parent_product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="products_catalogue.product",
            ),
        ),
    ]

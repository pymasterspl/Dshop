# Generated by Django 4.2.5 on 2023-10-05 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products_catalogue", "0012_pricechangehistory"),
    ]

    operations = [
        migrations.AddField(
            model_name="pricechangehistory",
            name="disabled_at",
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-16 15:14

from django.db import migrations


def delete_all_ceneocategories(apps, schema_editor):
    CC = apps.get_model("products_catalogue", "CeneoCategory")
    CC.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("products_catalogue", "0020_productattribute"),
    ]

    operations = [
        migrations.RunPython(delete_all_ceneocategories, delete_all_ceneocategories),
    ]

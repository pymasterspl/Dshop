# Generated by Django 4.2.3 on 2023-08-07 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products_catalogue', '0003_remove_category_sort_category_parent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products_catalogue.category'),
        ),
    ]
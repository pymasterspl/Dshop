# Generated by Django 4.2.7 on 2024-02-12 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_catalogue', '0002_alter_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cart_total',
            field=models.DecimalField(decimal_places=2, default=None, editable=False, max_digits=10),
        ),
    ]

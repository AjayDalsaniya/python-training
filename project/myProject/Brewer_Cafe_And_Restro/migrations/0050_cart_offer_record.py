# Generated by Django 4.1.3 on 2023-01-28 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brewer_Cafe_And_Restro', '0049_remove_cart_offer_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='offer_record',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
# Generated by Django 4.1.3 on 2022-12-20 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brewer_Cafe_And_Restro', '0027_itemcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcategory',
            name='item_category_description',
            field=models.CharField(max_length=1000),
        ),
    ]

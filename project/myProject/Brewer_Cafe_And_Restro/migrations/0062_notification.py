# Generated by Django 4.1.3 on 2023-01-31 14:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brewer_Cafe_And_Restro', '0061_delete_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('idnotification', models.AutoField(primary_key=True, serialize=False)),
                ('notification_description', models.TextField(blank=True, max_length=500)),
                ('notificationDate', models.DateField(null=True, verbose_name=datetime.date.today)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_iduser', models.ForeignKey(db_column='user_iduser', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Brewer_Cafe_And_Restro.user')),
            ],
            options={
                'db_table': 'notification',
                'managed': True,
            },
        ),
    ]

# Generated by Django 2.2.4 on 2020-10-15 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(default='1900-01-01'),
        ),
    ]

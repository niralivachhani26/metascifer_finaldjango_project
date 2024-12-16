# Generated by Django 5.1.4 on 2024-12-12 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_customuser_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='usertype',
            field=models.CharField(choices=[('artist', 'Artist'), ('customer', 'Customer')], default='customer', max_length=20),
        ),
    ]

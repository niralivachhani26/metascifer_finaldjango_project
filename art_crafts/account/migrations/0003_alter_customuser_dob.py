# Generated by Django 5.1.4 on 2024-12-11 09:18

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_customuser_city_alter_customuser_contact_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='dob',
            field=models.DateField(blank=True, null=True, validators=[account.models.MinAgeValidator(18)], verbose_name='Date of Birth'),
        ),
    ]

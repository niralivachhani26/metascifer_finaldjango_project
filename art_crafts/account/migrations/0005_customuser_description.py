# Generated by Django 5.1.4 on 2024-12-13 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_customuser_usertype'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.1.4 on 2024-12-13 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='arts',
            name='art_image',
            field=models.ImageField(blank=True, upload_to='static/images/arts/'),
        ),
    ]

# Generated by Django 4.1.2 on 2023-02-05 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.CharField(default='static/images/default.jpg', max_length=100),
        ),
    ]

# Generated by Django 4.1.2 on 2023-02-07 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_alter_course_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructor',
            name='total_learners',
        ),
    ]
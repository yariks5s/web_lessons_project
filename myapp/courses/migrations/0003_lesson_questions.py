# Generated by Django 4.1.6 on 2023-03-07 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_lesson_lessonslearnerrelations'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='questions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.questmodel'),
        ),
    ]

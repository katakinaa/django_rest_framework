# Generated by Django 5.1.1 on 2024-10-01 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0002_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='duration',
            field=models.TextField(null=True),
        ),
    ]

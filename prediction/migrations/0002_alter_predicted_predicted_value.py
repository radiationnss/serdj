# Generated by Django 4.2.7 on 2024-01-16 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predicted',
            name='predicted_value',
            field=models.CharField(max_length=255),
        ),
    ]

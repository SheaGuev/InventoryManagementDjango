# Generated by Django 5.0.4 on 2024-05-03 01:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("InventoryManagement", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]

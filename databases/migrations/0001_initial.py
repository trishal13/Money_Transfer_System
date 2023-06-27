# Generated by Django 4.2.1 on 2023-05-23 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Users",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.CharField(max_length=100)),
                ("Aadhar", models.CharField(max_length=12)),
                ("Mobile", models.CharField(max_length=10)),
                ("Email", models.EmailField(max_length=255)),
                ("Date_Of_Birth", models.DateField()),
                ("Account_Number", models.CharField(max_length=20)),
                ("IFSC", models.CharField(max_length=12)),
                ("Bank_Name", models.CharField(max_length=100)),
                ("User_ID", models.CharField(max_length=100)),
                ("Password", models.CharField(max_length=100)),
                ("MPIN", models.CharField(max_length=6)),
                ("Status", models.CharField(max_length=20)),
                ("Balance", models.IntegerField()),
            ],
        ),
    ]
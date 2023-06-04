# Generated by Django 4.1.7 on 2023-04-16 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="application2010e_part1",
            name="consent_Date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="application2010e_part1",
            name="location_Kept",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="application2010e_part1",
            name="supportive_type",
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name="application2010e_part1",
            name="verified_By",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
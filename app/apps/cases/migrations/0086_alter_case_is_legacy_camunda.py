# Generated by Django 3.2.7 on 2021-10-06 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0085_case_is_legacy_camunda"),
    ]

    operations = [
        migrations.AlterField(
            model_name="case",
            name="is_legacy_camunda",
            field=models.BooleanField(default=False),
        ),
    ]

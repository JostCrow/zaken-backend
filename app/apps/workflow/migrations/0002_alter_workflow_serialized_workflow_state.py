# Generated by Django 3.2.5 on 2021-08-26 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workflow", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workflow",
            name="serialized_workflow_state",
            field=models.JSONField(null=True),
        ),
    ]

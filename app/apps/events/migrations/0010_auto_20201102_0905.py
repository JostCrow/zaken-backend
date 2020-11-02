# Generated by Django 3.1.2 on 2020-11-02 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0009_auto_20201102_0808"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="type",
            field=models.CharField(
                choices=[
                    ("DEBRIEFING", "DEBRIEFING"),
                    ("VISIT", "VISIT"),
                    ("CASE", "CASE"),
                ],
                max_length=250,
            ),
        ),
    ]

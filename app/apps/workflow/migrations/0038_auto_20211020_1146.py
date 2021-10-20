# Generated by Django 3.2.7 on 2021-10-20 09:46

from django.db import migrations


def change_case_event_content_type(apps, schema_editor):
    CaseEvent = apps.get_model("events", "CaseEvent")
    ContentType = apps.get_model(app_label="contenttypes", model_name="ContentType")

    old_generic_completed_task_contenttype = ContentType.objects.filter(
        app_label="camunda", model="genericcompletedtask"
    ).first()
    new_generic_completed_task_contenttype = ContentType.objects.filter(
        app_label="workflow", model="genericcompletedtask"
    ).first()

    print(old_generic_completed_task_contenttype)
    print(new_generic_completed_task_contenttype)

    if (
        old_generic_completed_task_contenttype
        and new_generic_completed_task_contenttype
    ):
        case_events = CaseEvent.objects.filter(
            emitter_type_id=old_generic_completed_task_contenttype.id
        )
        print(case_events)
        case_events.update(emitter_type_id=new_generic_completed_task_contenttype.id)


def reverse_change_case_event_content_type(apps, schema_editor):
    CaseEvent = apps.get_model("events", "CaseEvent")
    ContentType = apps.get_model(app_label="contenttypes", model_name="ContentType")

    old_generic_completed_task_contenttype = ContentType.objects.filter(
        app_label="workflow", model="genericcompletedtask"
    ).first()
    new_generic_completed_task_contenttype = ContentType.objects.filter(
        app_label="camunda", model="genericcompletedtask"
    ).first()

    if (
        old_generic_completed_task_contenttype
        and new_generic_completed_task_contenttype
    ):
        case_events = CaseEvent.objects.filter(
            emitter_type_id=old_generic_completed_task_contenttype.id
        )
        case_events.update(emitter_type_id=new_generic_completed_task_contenttype.id)


class Migration(migrations.Migration):

    dependencies = [
        ("workflow", "0037_auto_20211019_1544"),
    ]

    operations = [
        migrations.RunPython(
            change_case_event_content_type,
            reverse_change_case_event_content_type,
        ),
    ]

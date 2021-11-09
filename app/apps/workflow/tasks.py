import copy
import logging

import celery
from apps.debriefings.models import Debriefing
from apps.visits.models import Visit
from celery import shared_task
from django.conf import settings
from django.db import transaction

DEFAULT_RETRY_DELAY = 2
logger = logging.getLogger(__name__)


class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception,)
    max_retries = 3
    default_retry_delay = DEFAULT_RETRY_DELAY


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_update_workflows(self):
    from apps.workflow.models import CaseWorkflow

    for workflow in CaseWorkflow.objects.filter(completed=False):
        if workflow.has_a_timer_event_fired():
            task_update_workflow.delay(workflow.id)
    return "task_update_workflows complete"


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_update_workflow(self, workflow_id):
    from apps.workflow.models import CaseWorkflow

    workflow = CaseWorkflow.objects.get(id=workflow_id)
    with transaction.atomic():
        workflow.update_workflow()

    return (
        f"task_update_workflow: update for workflow with id '{workflow_id}', complete"
    )


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_accept_message_for_workflow(self, workflow_id, message, extra_data):
    from apps.workflow.models import CaseWorkflow

    workflow = CaseWorkflow.objects.get(id=workflow_id)
    with transaction.atomic():
        workflow.accept_message(message, extra_data)

    return f"task_accept_message_for_workflow: message '{message}' for workflow with id {workflow_id}, accepted"


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_start_subworkflow(self, subworkflow_name, parent_workflow_id):
    from apps.workflow.models import CaseWorkflow

    parent_workflow = CaseWorkflow.objects.get(id=parent_workflow_id)
    with transaction.atomic():
        data = copy.deepcopy(parent_workflow.get_data())

        subworkflow = CaseWorkflow.objects.create(
            case=parent_workflow.case,
            parent_workflow=parent_workflow,
            workflow_type=subworkflow_name,
            data=data,
        )

    return f"task_start_subworkflow:  subworkflow id '{subworkflow.id}', for parent workflow with id '{parent_workflow_id}', created"


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_create_main_worflow_for_case(self, case_id):
    from apps.cases.models import Case
    from apps.workflow.models import CaseWorkflow

    case = Case.objects.get(id=case_id)
    with transaction.atomic():
        workflow_instance = CaseWorkflow.objects.create(
            case=case,
            workflow_type=settings.DEFAULT_WORKFLOW_TYPE,
            main_workflow=True,
            workflow_message_name="main_process",
        )

    return f"task_start_main_worflow_for_case: workflow id '{workflow_instance.id}', for case with id '{case_id}', created"


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_start_worflow(self, worklow_id):
    from apps.workflow.models import CaseWorkflow

    case_workflow = CaseWorkflow.objects.get(id=worklow_id)
    with transaction.atomic():
        case_workflow.start()

    return f"task_start_worflow: workflow id '{worklow_id}', started"


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_wait_for_workflows_and_send_message(self, workflow_id, message):
    import time

    from apps.workflow.models import CaseWorkflow

    time.sleep(2)

    logger.info(f"wait_for_workflows_and_send_message: {message}")
    logger.info(f"workflow id: {workflow_id}")

    workflow_instance = CaseWorkflow.objects.get(id=workflow_id)
    # tell the other workfows that this one is waiting
    workflow_instance.data.update(
        {
            message: "done",
        }
    )
    workflow_instance.save(update_fields=["data"])
    all_workflows = CaseWorkflow.objects.filter(
        case=workflow_instance.case,
        workflow_type=CaseWorkflow.WORKFLOW_TYPE_DIRECTOR,
    )

    workflows_completed = [
        a
        for a in all_workflows.values_list("data", flat=True)
        if a.get(message) == "done"
    ]
    main_workflow = all_workflows.filter(main_workflow=True).first()

    """
    Tests if all workflows reached thit point,
    so the last waiting worklfow kan tell the main workflow to accept the message after all, so only the main workflow can resume
    """
    if len(workflows_completed) == all_workflows.count() and main_workflow:

        # pick up all summons and pass them on to the main workflow
        all_summons = [
            d.get("summon_id")
            for d in all_workflows.values_list("data", flat=True)
            if d.get("summon_id")
        ]
        extra_data = {
            "all_summons": all_summons,
        }

        # sends the accept message to a task, because we have to wait until this current tasks, we are in, is completed
        task_accept_message_for_workflow.delay(main_workflow.id, message, extra_data)

        # TODO: cleanup(delete others), but the message is not send yet, so below should wait
        # other_workflows = all_workflows.exclude(id=main_workflow.id)
        # other_workflows.delete()


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_complete_worflow(self, worklow_id, data):
    from apps.workflow.models import CaseWorkflow

    case_workflow = CaseWorkflow.objects.get(id=worklow_id)
    with transaction.atomic():
        if (
            case_workflow.parent_workflow
            and case_workflow.parent_workflow.workflow_type
            == CaseWorkflow.WORKFLOW_TYPE_DIRECTOR
        ):
            case_workflow.parent_workflow.accept_message(
                f"resume_after_{case_workflow.workflow_type}",
                data,
            )

    return f"task_complete_worflow: workflow id '{worklow_id}', completed"


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_complete_user_task_and_create_new_user_tasks(self, id, data={}):
    from apps.workflow.models import CaseUserTask

    task = CaseUserTask.objects.get(id=id, completed=False)
    task.workflow.complete_user_task_and_create_new_user_tasks(task.task_id, data)

    return f"task_complete_user_task_and_create_new_user_tasks: task with id '{id}', created"


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_task_create_schedule(self, case_id):
    from apps.workflow.models import CaseUserTask, CaseWorkflow

    task_create_schedule = CaseUserTask.objects.filter(
        case__id=case_id, completed=False
    ).first()
    if (
        task_create_schedule
        and task_create_schedule.task_name == "task_create_schedule"
    ):
        CaseWorkflow.complete_user_task(task_create_schedule.id, {})
    else:
        return f"task_task_create_schedule: case id '{case_id}', task 'task_create_schedule' not found"

    return f"task_task_create_schedule: case with id '{case_id}', created"


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_task_create_visit(self, case_id):
    from apps.workflow.models import CaseUserTask, CaseWorkflow

    task_create_visit = CaseUserTask.objects.filter(
        case__id=case_id, completed=False
    ).first()
    if task_create_visit and task_create_visit.task_name == "task_create_visit":
        visit = Visit.objects.filter(case__id=case_id).first()
        if visit:
            CaseWorkflow.complete_user_task(
                task_create_visit.id,
                {
                    "situation": {"value": visit.situation},
                    "can_next_visit_go_ahead": {"value": visit.can_next_visit_go_ahead},
                },
            )
        else:
            return f"task_task_create_visit: case id '{case_id}', visit not found"
    else:
        return f"task_task_create_visit: case id '{case_id}', task 'task_create_visit' not found"

    return f"task_task_create_visit: case with id '{case_id}', created"


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_task_create_debrief(self, case_id):
    from apps.workflow.models import CaseUserTask, CaseWorkflow

    task_create_debrief = CaseUserTask.objects.filter(
        case__id=case_id, completed=False
    ).first()
    if task_create_debrief and task_create_debrief.task_name == "task_create_debrief":
        debriefing = Debriefing.objects.filter(case__id=case_id).first()
        if debriefing:
            CaseWorkflow.complete_user_task(
                task_create_debrief.id,
                {
                    "violation": {
                        "value": debriefing.violation,
                    }
                },
            )
        else:
            return f"task_task_create_debrief: case id '{case_id}', debrief not found"
    else:
        return f"task_task_create_debrief: case id '{case_id}', task 'task_create_debrief' not found"

    return f"task_task_create_debrief: case with id '{case_id}', created"

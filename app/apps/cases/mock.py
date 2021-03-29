import datetime

from apps.addresses.models import Address
from apps.cases.models import Case, CaseReason, CaseTeam
from apps.schedules.models import Action, DaySegment, Priority, Schedule, WeekSegment
from django.conf import settings
from django.contrib.auth import get_user_model
from model_bakery import baker


def mock():
    cases = mock_cases()
    mock_schedules(cases)


def mock_cases():
    print("Mocking cases")
    team = CaseTeam.objects.get(name=settings.DEFAULT_TEAM)
    reason = CaseReason.objects.get(name=settings.DEFAULT_REASON)

    user_model = get_user_model()
    user, _ = user_model.objects.get_or_create(
        email="jake.gyllenhaal@example.com",
        first_name="Jake",
        last_name="Gyllenhaal",
    )

    bag_ids = [
        "0363200012145295",
        "0363010000746755",
        "0363010000944728",
        "0363010012143319",
        "0363010000995710",
        "0363010000994527",
        "0363010012061588",
        "0363010001021020",
        "0363010012083877",
        "0363010001025436",
    ]

    cases = []

    for bag_id in bag_ids:
        address = Address.get(bag_id)
        case = baker.make(
            Case,
            author=user,
            reason=reason,
            team=team,
            start_date=datetime.date.today(),
            address=address,
            description="Melding gedaan door de buren",
        )
        cases.append(case)

    return cases


def mock_schedules(cases):
    for case in cases:
        action = Action.objects.get(name=settings.DEFAULT_SCHEDULE_ACTIONS[0])
        week_segment = WeekSegment.objects.get(
            name=settings.DEFAULT_SCHEDULE_WEEK_SEGMENTS[0]
        )
        day_segment = DaySegment.objects.get(
            name=settings.DEFAULT_SCHEDULE_DAY_SEGMENTS[0]
        )
        priority = Priority.objects.get(name=settings.DEFAULT_SCHEDULE_NORMAL_PRIORITY)

        Schedule.objects.create(
            case=case,
            action=action,
            week_segment=week_segment,
            day_segment=day_segment,
            priority=priority,
        )

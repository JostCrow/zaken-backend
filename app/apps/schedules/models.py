from apps.cases.models import Case, CaseTheme
from apps.events.models import CaseEvent, TaskModelEventEmitter
from django.db import models


class Action(models.Model):
    name = models.CharField(max_length=255)
    theme = models.ForeignKey(
        to=CaseTheme, on_delete=models.CASCADE, related_name="actions"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        unique_together = ["name", "theme"]


class WeekSegment(models.Model):
    name = models.CharField(max_length=255)
    theme = models.ForeignKey(
        to=CaseTheme, on_delete=models.CASCADE, related_name="week_segments"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        unique_together = ["name", "theme"]


class DaySegment(models.Model):
    name = models.CharField(max_length=255)
    theme = models.ForeignKey(
        to=CaseTheme, on_delete=models.CASCADE, related_name="day_segments"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        unique_together = ["name", "theme"]


class Priority(models.Model):
    name = models.CharField(max_length=255)
    theme = models.ForeignKey(
        to=CaseTheme, on_delete=models.CASCADE, related_name="priorities"
    )
    weight = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["weight"]
        unique_together = ["name", "theme"]


class Schedule(TaskModelEventEmitter):
    EVENT_TYPE = CaseEvent.TYPE_SCHEDULE

    action = models.ForeignKey(to=Action, on_delete=models.CASCADE)
    week_segment = models.ForeignKey(to=WeekSegment, on_delete=models.CASCADE)
    day_segment = models.ForeignKey(to=DaySegment, on_delete=models.CASCADE)
    priority = models.ForeignKey(to=Priority, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    case = models.ForeignKey(
        to=Case, related_name="schedules", on_delete=models.CASCADE
    )
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __get_event_values__(self):
        return {
            "date_added": self.date_added,
            "action": self.action.name,
            "week_segment": self.week_segment.name,
            "day_segment": self.day_segment.name,
            "priority": self.priority.name,
            "description": self.description,
        }

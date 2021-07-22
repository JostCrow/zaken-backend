import logging

from apps.schedules.models import Schedule
from apps.schedules.serializers import ScheduleCreateSerializer
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

logger = logging.getLogger(__name__)


class ScheduleViewSet(GenericViewSet, CreateModelMixin):
    # permission_classes = [IsInAuthorizedRealm | TopKeyAuth]
    serializer_class = ScheduleCreateSerializer
    queryset = Schedule.objects.all()

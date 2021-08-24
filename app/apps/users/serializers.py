from django.contrib.auth.models import Group
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import User
from .permissions import custom_permissions


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    @extend_schema_field(serializers.MultipleChoiceField(choices=custom_permissions))
    def get_permissions(self, object):
        return object.permissions.values_list("codename", flat=True)

    class Meta:
        model = Group
        exclude = [
            "id",
        ]


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    full_name = serializers.CharField(required=False)


class UserDetailSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    full_name = serializers.CharField(required=False)
    groups = GroupSerializer(required=False, many=True)

    class Meta:
        model = User
        exclude = [
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "user_permissions",
        ]


class OIDCAuthenticateSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)

from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer
from ..models import *

__all__ = [
    'NestedSystemGroupSerializer',
    'NestedSubsystemSerializer',
    'NestedSystemSerializer',
]


@extend_schema_serializer(
    exclude_fields=('system_count',),
)
class NestedSystemGroupSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_subsystems-api:systemgroup-detail')
    system_count = serializers.IntegerField(read_only=True)
    _depth = serializers.IntegerField(source='level', read_only=True)

    class Meta:
        model = SystemGroup
        fields = ['id', 'url', 'display', 'name', 'slug', 'system_count', '_depth']


@extend_schema_serializer(
    exclude_fields=('subsystem_count',),
)
class NestedSystemSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_subsystems-api:system-detail')
    subsystem_count = serializers.IntegerField(read_only=True)
    _depth = serializers.IntegerField(source='level', read_only=True)

    class Meta:
        model = System
        fields = ['id', 'url', 'display', 'name', 'slug', 'subsystem_count', '_depth']


class NestedSubsystemSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_subsystems-api:subsystem-detail')

    class Meta:
        model = Subsystem
        fields = ['id', 'url', 'display', 'name', 'slug']




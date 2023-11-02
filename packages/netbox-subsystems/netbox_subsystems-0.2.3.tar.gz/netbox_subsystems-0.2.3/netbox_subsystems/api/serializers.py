from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer, NestedGroupModelSerializer
from tenancy.api.nested_serializers import NestedTenantSerializer
from .nested_serializers import NestedSystemSerializer, NestedSystemGroupSerializer, NestedSubsystemSerializer
from ..models import Subsystem, System, SystemGroup, SYSTEM_FIELDS, SYSTEM_CHOICES_FIELD


class SystemGroupSerializer(NestedGroupModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_subsystems-api:systemgroup-detail')
    parent = NestedSystemGroupSerializer(required=False, allow_null=True)
    tenant_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = SystemGroup
        fields = [
            'id', 'url', 'display', 'name', 'slug', 'parent', 'description', 'tags', 'custom_fields', 'created',
            'last_updated', 'tenant_count', '_depth',
        ]


class SystemSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_subsystems-api:system-detail')
    group = NestedSystemGroupSerializer(required=False, allow_null=True)
    tenant = NestedTenantSerializer(required=False)
    parent = NestedSystemSerializer(required=False, allow_null=True)

    class Meta:
        model = System
        fields = (
            'id', 'url', 'display', 'name', 'slug', 'group', 'tenant', 'parent', 'description', 'comments', 'tags',
            'custom_fields', 'created', 'last_updated', 'security_id',
            # 'circuit_count', 'device_count', 'ipaddress_count', 'rack_count',
            # 'site_count', 'virtualmachine_count', 'vlan_count', 'vrf_count', 'cluster_count', 'prefix_count',
        ) + tuple(SYSTEM_FIELDS) + tuple(SYSTEM_CHOICES_FIELD)


class SubsystemSerializer(NestedGroupModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_subsystems-api:subsystem-detail'
    )
    system = NestedSystemSerializer(required=False)
    parent = NestedSubsystemSerializer(required=False)

    class Meta:
        model = Subsystem
        fields = (
            'id', 'url', 'display', 'name', 'parent', 'security_id', 'system',
            'comments', 'tags', 'custom_fields', 'created', 'last_updated'
        ) + tuple(SYSTEM_FIELDS) + tuple(SYSTEM_CHOICES_FIELD)


# class SystemConfLevelSerializer(NestedGroupModelSerializer):
#     url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_subsystems-api:system_config_level-detail')
#
#     class Meta:
#         model = SystemConfLevel
#         fields = [
#             'id', 'url', 'display', 'name', 'slug', 'description', 'tags', 'custom_fields', 'created',
#             'last_updated',
#         ]

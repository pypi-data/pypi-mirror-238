from rest_framework.routers import APIRootView
from netbox.api.viewsets import NetBoxModelViewSet
from utilities.utils import count_related

from circuits.models import Circuit
from dcim.models import Device, Rack, Site
from ipam.models import IPAddress, Prefix, VLAN, VRF
from tenancy.models import Tenant
from tenancy.api.serializers import TenantSerializer
from tenancy.filtersets import TenantFilterSet
from utilities.utils import count_related
from virtualization.models import VirtualMachine, Cluster
# from tenancy.api.views import *

from .. import models, filtersets
from . import serializers


class SubsystemsRootView(APIRootView):
    """
    Subsystems API root view
    """
    def get_view_name(self):
        return 'Subsystems'


class SystemGroupViewSet(NetBoxModelViewSet):
    queryset = models.SystemGroup.objects.add_related_count(
        models.SystemGroup.objects.all(),
        models.System,
        'group',
        'system_count',
        cumulative=True
    ).prefetch_related('tags')
    serializer_class = serializers.SystemGroupSerializer
    filterset_class = filtersets.SystemGroupFilterSet


class SystemViewSet(NetBoxModelViewSet):
    queryset = models.System.objects.prefetch_related(
        'group', 'tags'
    )
    # .annotate(
    #     circuit_count=count_related(Circuit, 'system'),
    #     device_count=count_related(Device, 'system'),
    #     ipaddress_count=count_related(IPAddress, 'system'),
    #     prefix_count=count_related(Prefix, 'system'),
    #     rack_count=count_related(Rack, 'system'),
    #     site_count=count_related(Site, 'system'),
    #     virtualmachine_count=count_related(VirtualMachine, 'system'),
    #     vlan_count=count_related(VLAN, 'system'),
    #     vrf_count=count_related(VRF, 'system'),
    #     cluster_count=count_related(Cluster, 'system')
    # )
    # )
    serializer_class = serializers.SystemSerializer
    filterset_class = filtersets.SystemFilterSet


class SubsystemViewSet(NetBoxModelViewSet):
    # queryset = models.Subsystems.objects.add_related_count(
    #     models.Subsystems,
    #     'parent',
    #     'subsystems_count',
    #     cumulative=True
    # ).prefetch_related('tags')

    queryset = models.Subsystem.objects.prefetch_related('system', 'tags')
    serializer_class = serializers.SubsystemSerializer
    filterset_class = filtersets.SubsystemFilterSet


# class SystemConfLevelViewSet(NetBoxModelViewSet):
#     queryset = models.SystemConfLevel.objects.all()
#     serializer_class = serializers.SystemConfLevelSerializer
#     filterset_class = filtersets.SystemConfLevelFilterSet

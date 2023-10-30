from django.contrib.auth.mixins import PermissionRequiredMixin
from netbox.views import generic
from utilities.views import register_model_view
from circuits.models import Circuit
from dcim.models import Cable, Device, Location, Rack, RackReservation, Site, VirtualDeviceContext
from ipam.models import Aggregate, ASN, IPAddress, IPRange, L2VPN, Prefix, VLAN, VRF
from virtualization.models import VirtualMachine, Cluster
from wireless.models import WirelessLAN, WirelessLink
from .models import System, SystemGroup, Subsystem
from . import forms, tables, filtersets


class SystemGroupListView(generic.ObjectListView):
    queryset = SystemGroup.objects.add_related_count(
        SystemGroup.objects.all(),
        System,
        'group',
        'system_count',
        cumulative=True
    )
    filterset = filtersets.SystemGroupFilterSet
    filterset_form = forms.SystemGroupFilterForm
    table = tables.SystemGroupTable
    permission_required = ('dcim.view_site', 'dcim.view_device')


@register_model_view(SystemGroup)
class SystemGroupView(generic.ObjectView):
    queryset = SystemGroup.objects.all()
    permission_required = ('dcim.view_site', 'dcim.view_device')

    def get_extra_context(self, request, instance):
        groups = instance.get_descendants(include_self=True)
        related_models = (
            (System.objects.restrict(request.user, 'view').filter(group__in=groups), 'group_id'),
        )

        return {
            'related_models': related_models,
        }


@register_model_view(SystemGroup, 'edit')
class SystemGroupEditView(generic.ObjectEditView):
    queryset = SystemGroup.objects.all()
    form = forms.SystemGroupForm
    permission_required = ('dcim.view_site', 'dcim.view_device')


@register_model_view(SystemGroup, 'delete')
class SystemGroupDeleteView(generic.ObjectDeleteView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = SystemGroup.objects.all()


# class SystemGroupBulkImportView(generic.BulkImportView):
#     queryset = SystemGroup.objects.all()
#     model_form = forms.SystemGroupImportForm
#
#
# class SystemGroupBulkEditView(generic.BulkEditView):
#     queryset = SystemGroup.objects.add_related_count(
#         SystemGroup.objects.all(),
#         System,
#         'group',
#         'tenant_count',
#         cumulative=True
#     )
#     filterset = filtersets.SystemGroupFilterSet
#     table = tables.SystemGroupTable
#     form = forms.SystemGroupBulkEditForm


class SystemGroupBulkDeleteView(generic.BulkDeleteView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = SystemGroup.objects.add_related_count(
        SystemGroup.objects.all(),
        System,
        'group',
        'System_count',
        cumulative=True
    )
    filterset = filtersets.SystemGroupFilterSet
    table = tables.SystemGroupTable


class SystemListView(generic.ObjectListView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = System.objects.all()
    filterset = filtersets.SystemFilterSet
    filterset_form = forms.SystemFilterForm
    table = tables.SystemTable


@register_model_view(System)
class SystemView(generic.ObjectView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = System.objects.all()

    def get_extra_context(self, request, instance):

        parents = instance.get_descendants(include_self=True)
        related_models = (
            (System.objects.restrict(request.user, 'view').filter(parent__in=parents), 'parent_id'),
        )

        return {
            'related_models': related_models,
        }


# @register_model_view(System, 'edit')
class SystemEditView(generic.ObjectEditView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = System.objects.all()
    form = forms.SystemForm
    template_name = 'netbox_subsystems/system_edit.html'


@register_model_view(System, 'delete')
class SystemDeleteView(generic.ObjectDeleteView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = System.objects.all()


# class SystemBulkImportView(generic.BulkImportView):
#     queryset = System.objects.all()
#     model_form = forms.SystemImportForm
#
#
# class SystemBulkEditView(generic.BulkEditView):
#     queryset = System.objects.all()
#     filterset = filtersets.SystemFilterSet
#     table = tables.SystemTable
#     form = forms.SystemBulkEditForm


# class SystemBulkDeleteView(generic.BulkDeleteView):
#     queryset = System.objects.all()
#     filterset = filtersets.SystemFilterSet
#     table = tables.SystemTable


class SubsystemView(PermissionRequiredMixin, generic.ObjectView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = Subsystem.objects.all()

    def get_extra_context(self, request, instance):
        parents = instance.get_descendants(include_self=True)
        related_models = (
            (Subsystem.objects.restrict(request.user, 'view').filter(parent__in=parents), 'parent_id'),
        )

        return {
            'related_models': related_models,
        }


class SubsystemListView(PermissionRequiredMixin, generic.ObjectListView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = Subsystem.objects.all()
    # queryset = Subsystem.objects.add_related_count(
        # Subsystem,
        # 'parent',
        # 'Subsystem_count',
        # cumulative=True
    # )
    table = tables.SubsystemTable
    filterset = filtersets.SubsystemFilterSet
    filterset_form = forms.SubsystemFilterForm


class SubsystemEditView(PermissionRequiredMixin, generic.ObjectEditView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = Subsystem.objects.all()
    form = forms.SubsystemForm
    template_name = 'netbox_subsystems/subsystem_edit.html'


class SubsystemDeleteView(PermissionRequiredMixin, generic.ObjectDeleteView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = Subsystem.objects.all()

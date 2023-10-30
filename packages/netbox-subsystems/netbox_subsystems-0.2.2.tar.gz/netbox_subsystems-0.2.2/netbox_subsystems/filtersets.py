import django_filters
from django.utils.translation import gettext as _
from netbox.filtersets import NetBoxModelFilterSet, OrganizationalModelFilterSet
from utilities.filters import TreeNodeMultipleChoiceFilter
from tenancy.filtersets import ContactModelFilterSet
from .models import Subsystem, SystemGroup, System, SYSTEM_FIELDS, SYSTEM_CHOICES_FIELD
from django.db.models import Q


class SystemGroupFilterSet(OrganizationalModelFilterSet):
    parent_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SystemGroup.objects.all(),
        label=_('Группа систем (ID)'),
    )
    parent = django_filters.ModelMultipleChoiceFilter(
        field_name='parent__slug',
        queryset=SystemGroup.objects.all(),
        to_field_name='slug',
        label=_('Группа систем (slug)'),
    )

    class Meta:
        model = SystemGroup
        fields = ['id', 'name', 'slug', 'description']


class SystemFilterSet(NetBoxModelFilterSet, ContactModelFilterSet):
    group_id = TreeNodeMultipleChoiceFilter(
        queryset=SystemGroup.objects.all(),
        field_name='group',
        lookup_expr='in',
        label=_('АС (ID)'),
    )
    group = TreeNodeMultipleChoiceFilter(
        queryset=SystemGroup.objects.all(),
        field_name='group',
        lookup_expr='in',
        to_field_name='slug',
        label=_('АС (slug)'),
    )
    parent_id = django_filters.ModelMultipleChoiceFilter(
        queryset=System.objects.all(),
        label=_('Система (ID)'),
    )
    parent = django_filters.ModelMultipleChoiceFilter(
        field_name='parent__slug',
        queryset=System.objects.all(),
        to_field_name='slug',
        label=_('Система (slug)'),
    )

    class Meta:
        model = System
        fields = ['id', 'name', 'slug', 'description'] + SYSTEM_FIELDS + SYSTEM_CHOICES_FIELD

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(slug__icontains=value) |
            Q(description__icontains=value) |
            Q(comments__icontains=value)
        )


class SubsystemFilterSet(NetBoxModelFilterSet, ContactModelFilterSet):
    system_id = TreeNodeMultipleChoiceFilter(
        queryset=System.objects.all(),
        field_name='system',
        lookup_expr='in',
        label=_('System (ID)'),
    )
    system = TreeNodeMultipleChoiceFilter(
        queryset=System.objects.all(),
        field_name='system',
        lookup_expr='in',
        to_field_name='slug',
        label=_('System (slug)'),
    )
    parent_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Subsystem.objects.all(),
        label=_('SubСистема (ID)'),
    )
    parent = django_filters.ModelMultipleChoiceFilter(
        field_name='parent__slug',
        queryset=Subsystem.objects.all(),
        to_field_name='slug',
        label=_('SubСистема (slug)'),
    )

    class Meta:
        model = Subsystem
        fields = ['id', 'name', 'slug', 'description'] + SYSTEM_FIELDS + SYSTEM_CHOICES_FIELD

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(slug__icontains=value) |
            Q(description__icontains=value) |
            Q(comments__icontains=value)
        )

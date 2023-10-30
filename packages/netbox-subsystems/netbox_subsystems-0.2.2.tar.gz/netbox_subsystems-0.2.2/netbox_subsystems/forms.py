from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from tenancy.models import Tenant
from .models import Subsystem, System, SystemGroup, SYSTEM_FIELDS, SYSTEM_CHOICES_FIELD, SystemLevelChoices, \
    SystemPersDataLevelChoices, SystemConfLevelChoices

from django.conf import settings
from packaging import version

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)
if NETBOX_CURRENT_VERSION >= version.parse("3.5"):
    from utilities.forms.fields import TagFilterField, CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField, SlugField
else:
    from utilities.forms import TagFilterField, CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField, SlugField


class SystemGroupForm(NetBoxModelForm):
    parent = DynamicModelChoiceField(
        queryset=SystemGroup.objects.all(),
        required=False
    )
    slug = SlugField()
    fieldsets = (
        ('Группа Системы', (
            'parent', 'name', 'slug', 'description', 'tags',
        )),
    )

    class Meta:
        model = SystemGroup
        fields = [
            'parent', 'name', 'slug', 'description', 'tags',
        ]


class SystemForm(NetBoxModelForm):
    group = DynamicModelChoiceField(label='Группа', queryset=SystemGroup.objects.all(), required=False)
    tenant = DynamicModelChoiceField(label='Учреждение', queryset=Tenant.objects.all())
    parent = DynamicModelChoiceField(queryset=System.objects.all(), required=False, null_option='NONE',
                                     label='В составе')
    comments = CommentField()
    slug = SlugField()

    class Meta:
        model = System
        fields = (
            'name', 'slug', 'group', 'parent', 'tenant', 'security_id', 'comments', 'description', 'tags'
        ) + tuple(SYSTEM_FIELDS) + tuple(SYSTEM_CHOICES_FIELD)


class SubsystemForm(NetBoxModelForm):
    system = DynamicModelChoiceField(label='Система', queryset=System.objects.all())
    parent = DynamicModelChoiceField(
        queryset=Subsystem.objects.all(),
        required=False,
        null_option='None',
        label='В составе'
    )
    comments = CommentField()
    slug = SlugField()

    class Meta:
        model = Subsystem
        fields = (
            'name', 'slug', 'parent', 'system', 'security_id', 'comments', 'description', 'tags'
        ) + tuple(SYSTEM_FIELDS) + tuple(SYSTEM_CHOICES_FIELD)


class SystemGroupFilterForm(NetBoxModelFilterSetForm):
    model = SystemGroup

    name = forms.CharField(
        label='Название',
        required=False
    )
    parent_id = DynamicModelChoiceField(
        queryset=SystemGroup.objects.all(),
        required=False,
        null_option='None',
        label='В составе'
    )

    tag = TagFilterField(model)


class SystemCommonFilterForm(NetBoxModelFilterSetForm):
    name = forms.CharField(
        label='Название',
        required=False
    )
    security_id = forms.CharField(
        label='SSID',
        required=False
    )
    critical_level = forms.MultipleChoiceField(
        label='Уровень критичности ИС',
        choices=SystemLevelChoices,
        required=False
    )
    pers_data_category = forms.MultipleChoiceField(
        label='Уровень критичности ИС (из тенантов',
        choices=SystemPersDataLevelChoices,
        required=False
    )
    confidential_info = forms.MultipleChoiceField(
        label='Перечень конфиденциальной информации',
        choices=SystemConfLevelChoices,
        required=False
    )


class SystemFilterForm(SystemCommonFilterForm):
    model = System
    tag = TagFilterField(model)
    parent_id = DynamicModelMultipleChoiceField(
        queryset=System.objects.all(),
        required=False,
        null_option='None',
        label='В составе'
    )
    system_group_id = DynamicModelMultipleChoiceField(
        queryset=SystemGroup.objects.all(),
        required=False,
        null_option='None',
        label='Группа'
    )
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'group_id': '$tenant_group_id'
        },
        label='Учреждение'
    )


class SubsystemFilterForm(SystemCommonFilterForm):
    model = Subsystem
    tag = TagFilterField(model)
    parent_id = DynamicModelMultipleChoiceField(
        queryset=Subsystem.objects.all(),
        required=False,
        null_option='None',
        label='В составе'
    )
    system_id = forms.ModelMultipleChoiceField(
        label='Система',
        queryset=System.objects.all(),
        required=False
    )


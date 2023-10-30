import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import Subsystem, System, SystemGroup, SYSTEM_FIELDS, SYSTEM_CHOICES_FIELD

TENANT_SUBSYSTEM_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_subsystems:subsystem' pk=record.pk %}">Подсистема {% firstof record.name %}</a>
{% endif %}
"""
TENANT_SYSTEM_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_subsystems:system' pk=record.pk %}">Система {% firstof record.name %}</a>
{% endif %}
"""
TENANT_SYSTEMGROUP_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_subsystems:systemgroup' pk=record.pk %}">Группа {% firstof record.name %}</a>
{% endif %}
"""


class SystemGroupTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=TENANT_SYSTEMGROUP_LINK)
    system_count = columns.LinkedCountColumn(
        viewname='plugins:netbox_subsystems:system_list',
        url_params={'group_id': 'pk'},
        verbose_name='Системы'
    )

    tags = columns.TagColumn(
        url_name='plugins:netbox_subsystems:subsystems_list'
    )

    class Meta(NetBoxTable.Meta):
        model = SystemGroup
        fields = (
            'pk', 'id', 'name', 'system_count', 'description', 'slug', 'tags', 'created', 'last_updated', 'actions',
        )
        default_columns = ('pk', 'name', 'system_count', 'description')


class SystemTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=TENANT_SYSTEM_LINK)
    group = tables.Column(verbose_name="Группа", linkify=True)
    tenant = tables.Column(verbose_name="Учреждение", linkify=True)
    parent = tables.Column(verbose_name="Входит в ", linkify=True)
    critical_level = columns.ChoiceFieldColumn()
    pers_data_category = columns.ChoiceFieldColumn()
    confidential_info = columns.ChoiceFieldColumn()
    tags = columns.TagColumn(url_name='plugins:netbox_subsystems:system_list')
    comments = columns.MarkdownColumn()

    class Meta(NetBoxTable.Meta):
        model = System
        fields = (
            'pk', 'id', 'name', 'slug', 'group', 'tenant', 'parent', 'description', 'comments', 'contacts', 'tags',
            'created', 'last_updated',
        ) + tuple(SYSTEM_FIELDS) + tuple(SYSTEM_CHOICES_FIELD)
        default_columns = ('pk', 'name', 'group', 'tenant')


class SubsystemTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=TENANT_SUBSYSTEM_LINK)
    system = tables.Column(verbose_name="Система", linkify=True)
    parent = tables.Column(verbose_name="Входит в ", linkify=True)
    critical_level = columns.ChoiceFieldColumn()
    pers_data_category = columns.ChoiceFieldColumn()
    confidential_info = columns.ChoiceFieldColumn()
    tags = columns.TagColumn(url_name='plugins:netbox_subsystems:subsystem_list')
    comments = columns.MarkdownColumn()

    class Meta(NetBoxTable.Meta):
        model = Subsystem
        fields = (
            'pk', 'id', 'name', 'slug', 'system', 'parent', 'description', 'comments', 'contacts', 'tags', 'created',
            'last_updated',
        ) + tuple(SYSTEM_FIELDS) + tuple(SYSTEM_CHOICES_FIELD)
        default_columns = ('pk', 'name', 'system', 'description')

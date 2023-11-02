from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify
from django.core.validators import ValidationError
from mptt.models import MPTTModel
from dcim.models import Device
from virtualization.models import VirtualMachine, Cluster
from ipam.models import L2VPN, ASN, IPAddress, IPRange, Prefix, VLAN

from netbox.models import NestedGroupModel, PrimaryModel, NetBoxModel
from utilities.choices import ChoiceSet


class SystemLevelChoices(ChoiceSet):
    key = 'SystemLevel'
    CHOICES = [
        ('bc', 'BC', 'green'),
        ('mc', 'MC', 'purple'),
        ('bo', 'BO', 'orange'),
        ('op', 'OP', 'yellow'),
    ]


class SystemPersDataLevelChoices(ChoiceSet):
    key = 'SystemPersDataLevel'
    CHOICES = [
        ('corporate', 'Работники компании', 'green'),
        ('partners', 'Клиенты или партнёры компании', 'purple'),
        ('biometric', 'Биометрические данные', 'orange'),
        ('special', 'Данные специальных категорий', 'yellow'),
        ('other', 'Иные данные', 'indigo'),
    ]


class SystemConfLevelChoices(ChoiceSet):
    key = 'SystemConfLevel'
    CHOICES = [
        ('bank', 'Банковская тайна', 'indigo'),
        ('commercial', 'Коммерческая тайна', 'purple'),
        ('other', 'Иная конфиденциальная инф-ия (КИ)', 'orange'),
        ('personal', 'Персональные данные', 'yellow'),
    ]


SYSTEM_FIELDS = ['security_id', 'gitlab', 'wiki', 'comm_date', 'com_order', 'is_box_solution',
                 'is_otsrc_sys', 'is_otsrc_sup', 'is_otsrc_adm', 'technologies', 'dev_technologies', 'is_internet',
                 'is_able_eirjs', 'is_able_api', 'is_api_internet', 'is_cont_access', 'is_conf_info']
SYSTEM_CHOICES_FIELD = ['confidential_info', 'critical_level', 'pers_data_category']  # get_document_type_display


# class SystemConfLevel(NetBoxModel):
#     name = models.CharField(
#         verbose_name="Название АС",
#         max_length=100
#     )
#     description = models.CharField(
#         verbose_name="Описание",
#         max_length=250,
#         blank=True
#     )
#     slug = models.SlugField(
#         verbose_name="короткий URL",
#         max_length=100
#     )
#
#     class Meta:
#         verbose_name = "Тип конфиденциальной информации"
#         verbose_name_plural = "Типы конфиденциальной информации"
#         ordering = ['name']
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('plugins:netbox_subsystems:system_config_level', args=[self.pk])


class SystemCommon(PrimaryModel, MPTTModel):
    name = models.CharField(
        verbose_name="Название АС",
        max_length=100
    )
    slug = models.SlugField(
        verbose_name="короткий URL",
        max_length=100
    )
    parent = models.ForeignKey(
        verbose_name='Входит в',
        to='self',
        on_delete=models.SET_NULL,
        related_name='child',
        blank=True,
        null=True,
        default=None
    )
    security_id = models.CharField(
        verbose_name="security_id",
        max_length=50
    )
    gitlab = models.URLField(
        verbose_name="Gitlab",
        max_length=200,
        blank=True,
        null=True
    )
    wiki = models.URLField(
        verbose_name="Wiki",
        max_length=200,
        blank=True,
        null=True
    )
    critical_level = models.CharField(  # BC,MC,BO,OP
        verbose_name="Уровень критичности ИС",
        max_length=2,
        choices=SystemLevelChoices,
        default='bc'
    )
    pers_data_category = models.CharField(
        verbose_name="Категория персональных данных",
        max_length=15,
        choices=SystemPersDataLevelChoices,
        default='corporate'
    )
    confidential_info = models.CharField(
        verbose_name="Перечень конфиденциальной информации",
        max_length=150,
        choices=SystemConfLevelChoices,
        default='personal'
    )
    # confidential_info = models.ManyToManyField(
    #     SystemConfLevel,
    #     verbose_name="Перечень конфиденциальной информации",
    # )
    comm_date = models.DateField(
        verbose_name="Дата ввода в эксплуатацию",
        blank=True,
        null=True
    )
    com_order = models.CharField(
        verbose_name="Приказ ввода в эксплуатацию",
        max_length=50,
        blank=True,
        null=True
    )
    technologies = models.CharField(
        verbose_name="Технологии",
        max_length=150,
        blank=True,
        null=True
    )
    dev_technologies = models.CharField(
        verbose_name="Технологии развертывания",
        max_length=150,
        blank=True,
        null=True
    )
    is_box_solution = models.BooleanField(
        verbose_name="Коробочное решение",
        default=False
    )
    is_otsrc_sys = models.BooleanField(
        verbose_name="Система на аутсорсе",
        default=False
    )
    is_otsrc_sup = models.BooleanField(
        verbose_name="Поддержка системы на аутсорсе",
        default=False
    )
    is_otsrc_adm = models.BooleanField(
        verbose_name="Администрирование системы на аутсорсе",
        default=False
    )
    is_internet = models.BooleanField(
        verbose_name="Решение доступно из сети Интернет",
        default=False
    )
    is_able_eirjs = models.BooleanField(
        verbose_name="Доступ из сети других организаций ЕИРЖС",
        default=False
    )
    is_able_api = models.BooleanField(
        verbose_name="Есть API",
        default=False
    )
    is_api_internet = models.BooleanField(
        verbose_name="Нужен API доступ из сети Интернет",
        default=False
    )
    is_cont_access = models.BooleanField(
        verbose_name="Доступ из сети подрядчика, контрагента",
        default=False
    )
    is_conf_info = models.BooleanField(
        verbose_name="Обрабатывается конфиденциальная информация",
        default=False
    )
    # Generic relations
    contacts = GenericRelation(
        to='tenancy.ContactAssignment'
    )
    """
        Для контактов:
            Владелец от бизнеса
            Руководитель проекта
            Архитектор
            DevOps
    """
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def get_child(self):
        return self.child.all()


    def clean(self):
        super().clean()

        # An MPTT model cannot be its own parent
        if self.pk and self.parent and self.parent in self.get_descendants(include_self=True):
            raise ValidationError({
                "parent": f"Cannot assign self or child {self._meta.verbose_name} as parent."
            })


class SystemGroup(NestedGroupModel):
    name = models.CharField(
        verbose_name="название",
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        verbose_name="короткий URL",
        max_length=100,
        unique=True
    )
    description = models.CharField(
        verbose_name="Описание",
        max_length=200,
        blank=True
    )

    class Meta:
        verbose_name = "Группа систем"
        verbose_name_plural = "Группы систем"
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('plugins:netbox_subsystems:systemgroup', args=[self.pk])


class System(SystemCommon):
    """
    A Systems represents an organization served by the NetBox owner. This is typically a customer or an internal
    department.
    """
    group = models.ForeignKey(
        verbose_name="Группа систем",
        to=SystemGroup,
        on_delete=models.SET_NULL,
        related_name='systems',
        blank=True,
        null=True
    )
    tenant = models.ForeignKey(
        verbose_name="Учреждения",
        to='tenancy.Tenant',
        on_delete=models.CASCADE,
        related_name='systems'
    )
    clone_fields = (
        'group', 'description',
    )

    class Meta:
        verbose_name = "Система"
        verbose_name_plural = "Системы"
        ordering = ['name']

    def get_related_objects(self):
        data = {
            Device._meta.verbose_name_plural: {
                'count': Device.objects.filter(custom_field_data__system=self.id).count(),
                'model': self.get_model_name(Device)
            },
            VirtualMachine._meta.verbose_name_plural: {
                'count': VirtualMachine.objects.filter(custom_field_data__system=self.id).count(),
                'model': self.get_model_name(VirtualMachine)
            },
            Cluster._meta.verbose_name_plural: {
                'count': Cluster.objects.filter(custom_field_data__system=self.id).count(),
                'model': self.get_model_name(Cluster)
            },
            ASN._meta.verbose_name_plural: {
                'count': ASN.objects.filter(custom_field_data__system=self.id).count(),
                'model': self.get_model_name(ASN)
            },
            L2VPN._meta.verbose_name_plural: {
                'count': L2VPN.objects.filter(custom_field_data__system=self.id).count(),
                'model': self.get_model_name(L2VPN)
            },
            IPRange._meta.verbose_name_plural: {
                'count': IPRange.objects.filter(custom_field_data__system=self.id).count(),
                'model': self.get_model_name(IPRange)
            },
            IPAddress._meta.verbose_name_plural: {
                'count': IPAddress.objects.filter(custom_field_data__system=self.id).count(),
                'model': self.get_model_name(IPAddress)
            },
            Prefix._meta.verbose_name_plural: {
                'count': Prefix.objects.filter(custom_field_data__system=self.id).count(),
                'model': self.get_model_name(Prefix)
            },
            VLAN._meta.verbose_name_plural: {
                'count': VLAN.objects.filter(custom_field_data__system=self.id).count(),
                'model': self.get_model_name(VLAN)
            },
        }
        return data

    @staticmethod
    def get_model_name(obj):
        obj_url = str(obj.__module__).split(".")[-1] + ':' + str(obj).split("'")[-2].split('.')[-1].lower() + '_list'
        link = "{% url '" + obj_url + "' %}?{{ filter_param }}={{ object.pk }}"
        model = str(obj).split("'")[-2].split('.')[-1].lower()
        return model

    def get_subsystems(self):
        return self.subsystems.all()


    def get_absolute_url(self):
        return reverse('plugins:netbox_subsystems:system', args=[self.pk])


class Subsystem(SystemCommon):
    """
    A Subsystems represents an organization served by the NetBox owner. This is typically a customer or an internal
    department.
    """
    system = models.ForeignKey(
        verbose_name="В составе системы",
        to=System,
        on_delete=models.CASCADE,
        related_name='subsystems'
    )

    parent = models.ForeignKey(
        verbose_name='Входит в подсистему',
        to='self',
        on_delete=models.CASCADE,
        related_name='child',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Подсистема"
        verbose_name_plural = "Подсистемы"
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('plugins:netbox_subsystems:subsystem', args=[self.pk])

    def get_related_objects(self):
        data = {
            Device._meta.verbose_name_plural: {
                'count': Device.objects.filter(custom_field_data__subsystem=self.id).count(),
                'model': self.get_model_name(Device)
            },
            VirtualMachine._meta.verbose_name_plural: {
                'count': VirtualMachine.objects.filter(custom_field_data__subsystem=self.id).count(),
                'model': self.get_model_name(VirtualMachine)
            },
            Cluster._meta.verbose_name_plural: {
                'count': Cluster.objects.filter(custom_field_data__subsystem=self.id).count(),
                'model': self.get_model_name(Cluster)
            },
            ASN._meta.verbose_name_plural: {
                'count': ASN.objects.filter(custom_field_data__subsystem=self.id).count(),
                'model': self.get_model_name(ASN)
            },
            L2VPN._meta.verbose_name_plural: {
                'count': L2VPN.objects.filter(custom_field_data__subsystem=self.id).count(),
                'model': self.get_model_name(L2VPN)
            },
            IPRange._meta.verbose_name_plural: {
                'count': IPRange.objects.filter(custom_field_data__subsystem=self.id).count(),
                'model': self.get_model_name(IPRange)
            },
            IPAddress._meta.verbose_name_plural: {
                'count': IPAddress.objects.filter(custom_field_data__subsystem=self.id).count(),
                'model': self.get_model_name(IPAddress)
            },
            Prefix._meta.verbose_name_plural: {
                'count': Prefix.objects.filter(custom_field_data__subsystem=self.id).count(),
                'model': self.get_model_name(Prefix)
            },
            VLAN._meta.verbose_name_plural: {
                'count': VLAN.objects.filter(custom_field_data__subsystem=self.id).count(),
                'model': self.get_model_name(VLAN)
            },
        }
        return data

    @staticmethod
    def get_model_name(obj):
        obj_url = str(obj.__module__).split(".")[-1] + ':' + str(obj).split("'")[-2].split('.')[-1].lower() + '_list'
        link = "{% url '" + obj_url + "' %}?{{ filter_param }}={{ object.pk }}"
        model = str(obj).split("'")[-2].split('.')[-1].lower()
        return model

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.tenant = self.system.tenant if self.system else None
        super().save(*args, **kwargs)

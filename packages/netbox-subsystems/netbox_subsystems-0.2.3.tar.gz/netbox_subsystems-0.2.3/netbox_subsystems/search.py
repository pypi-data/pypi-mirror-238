from netbox.search import SearchIndex
from .models import Subsystem, System, SystemGroup
from django.conf import settings

# If we run NB 3.4+ register search indexes 
if settings.VERSION >= '3.4.0':
    class SystemGroupIndex(SearchIndex):
        model = SystemGroup
        fields = (
            ('name', 100),
            ('slug', 110),
            ('description', 500),
        )

    # class SystemConfLevelIndex(SearchIndex):
    #     model = SystemConfLevel
    #     fields = (
    #         ('name', 100),
    #         ('slug', 110),
    #         ('description', 500),
    #     )

    class SystemIndex(SearchIndex):
        model = System
        fields = (
            ('name', 100),
            ('slug', 110),
            ('gitlab', 120),
            ('wiki', 130),
            ('com_order', 140),
            ('technologies', 150),
            ('dev_technologies', 160),
            ('description', 500),
            ('comments', 5000),
        )

    class SubsystemIndex(SearchIndex):
        model = Subsystem
        fields = (
            ('name', 100),
            ('slug', 110),
            ('gitlab', 120),
            ('wiki', 130),
            ('com_order', 140),
            ('technologies', 150),
            ('dev_technologies', 160),
            ('description', 500),
            ('comments', 5000),
        )

    # Register indexes
    indexes = [SystemGroupIndex, SystemIndex, SubsystemIndex]

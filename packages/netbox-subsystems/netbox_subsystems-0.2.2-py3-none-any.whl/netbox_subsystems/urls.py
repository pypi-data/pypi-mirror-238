from django.urls import path
from .models import Subsystem
from .views import *
from netbox.views.generic import ObjectChangeLogView

urlpatterns = (
    # Systems
    path('system/', SystemListView.as_view(), name='system_list'),
    path('system/add/', SystemEditView.as_view(), name='system_add'),
    path('system/<int:pk>/', SystemView.as_view(), name='system'),
    path('system/<int:pk>/edit/', SystemEditView.as_view(), name='system_edit'),
    path('system/<int:pk>/delete/', SystemDeleteView.as_view(), name='system_delete'),
    path('system/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='system_changelog', kwargs={
        'model': System
    }),
    # system-groups
    path('system-groups/', SystemGroupListView.as_view(), name='systemgroup_list'),
    path('system-groups/add/', SystemGroupEditView.as_view(), name='systemgroup_add'),
    path('system-groups/<int:pk>/', SystemGroupView.as_view(), name='systemgroup'),
    path('system-groups/<int:pk>/edit/', SystemGroupEditView.as_view(), name='systemgroup_edit'),
    path('system-groups/<int:pk>/delete/', SystemGroupDeleteView.as_view(), name='systemgroup_delete'),
    path('system-groups/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='systemgroup_changelog', kwargs={
        'model': SystemGroup
    }),
    # subsystems
    path('subsystem/', SubsystemListView.as_view(), name='subsystem_list'),
    path('subsystem/add/', SubsystemEditView.as_view(), name='subsystem_add'),
    path('subsystem/<int:pk>/', SubsystemView.as_view(), name='subsystem'),
    path('subsystem/<int:pk>/edit/', SubsystemEditView.as_view(), name='subsystem_edit'),
    path('subsystem/<int:pk>/delete/', SubsystemDeleteView.as_view(), name='subsystem_delete'),
    path('subsystem/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='subsystem_changelog', kwargs={
        'model': Subsystem
    }),
)

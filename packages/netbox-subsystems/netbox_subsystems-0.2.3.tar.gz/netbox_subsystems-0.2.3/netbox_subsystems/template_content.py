from extras.plugins import PluginTemplateExtension
from django.conf import settings
from .models import Subsystem, System, SystemGroup

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_subsystems', {})


class SubsystemsList(PluginTemplateExtension):
    model = 'tenancy.tenant'

    def get_context(self):
        systems = System.objects.filter(tenant=self.context['object'])
        systemgroups = SystemGroup.objects.filter(systems__in=systems)
        subsystems = Subsystem.objects.filter(system__in=systems)
        return {
            'systems': systems,
            'systems_count': len(list(systems)),
            'systemgroups': systemgroups,
            'systemgroups_count': len(list(systemgroups)),
            'subsystems': subsystems,
            'subsystems_count': len(list(subsystems))
        }

    def left_page(self):
        if plugin_settings.get('enable_subsystems') and plugin_settings.get('subsystems_location') == 'left':

            return self.render('netbox_subsystems/system_include.html', extra_context=self.get_context())
        else:
            return ""

    def right_page(self):
        if plugin_settings.get('enable_subsystems') and plugin_settings.get('subsystems_location') == 'right':

            return self.render('netbox_subsystems/subsystems_objects.html', extra_context=self.get_context())
        else:
            return ""

    def full_width_page(self):
        if plugin_settings.get('enable_subsystems') and plugin_settings.get('subsystems_location') == 'full_width_page':
            return self.render('netbox_subsystems/system_include.html', extra_context=self.get_context())
        else:
            return ""

    def buttons(self):
        if plugin_settings.get('enable_subsystems') and plugin_settings.get('subsystems_location') == 'buttons':
            return self.render('netbox_subsystems/system_include.html', extra_context=self.get_context())
        else:
            return ""

    def list_buttons(self):
        if plugin_settings.get('enable_subsystems') and plugin_settings.get('subsystems_location') == 'list_buttons':
            return self.render('netbox_subsystems/system_include.html', extra_context=self.get_context())
        else:
            return ""



template_extensions = [SubsystemsList]

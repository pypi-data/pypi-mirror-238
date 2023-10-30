from netbox.api.routers import NetBoxRouter
from .views import SubsystemViewSet, SystemViewSet, SystemGroupViewSet

app_name = 'netbox_subsystems'

router = NetBoxRouter()
router.register('subsystem', SubsystemViewSet)
router.register('system', SystemViewSet)
router.register('systemgroup', SystemGroupViewSet)

urlpatterns = router.urls

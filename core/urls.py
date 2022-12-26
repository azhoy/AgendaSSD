from django.urls import path, include
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('events', viewset=views.EventViewSet)
router.register('member', viewset=views.MemberViewSet)

events_router = routers.NestedDefaultRouter(router, 'events', lookup='event')
events_router.register('participants', viewset=views.EventParticipantsViewSet, basename='event-participants')

# URLConf
urlpatterns = router.urls + events_router.urls

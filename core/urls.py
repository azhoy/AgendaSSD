from django.urls import path, include
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('events', viewset=views.EventViewSet, basename='events')
router.register('member', viewset=views.MemberViewSet)

events_router = routers.NestedDefaultRouter(router, 'events', lookup='event')
events_router.register('invitations', viewset=views.InvitationViewSet, basename='event-invitations')

# URLConf
urlpatterns = router.urls + events_router.urls

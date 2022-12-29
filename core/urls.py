from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('events', viewset=views.EventViewSet, basename='events')
router.register('member', viewset=views.MemberViewSet)

events_router = routers.NestedDefaultRouter(router, 'events', lookup='event')
events_router.register('invitations', viewset=views.InvitationViewSet, basename='event-invitations')

# URLConf
urlpatterns = [
    path('agenda/', include(router.urls)),
    path('agenda/', include(events_router.urls)),
    path('', TemplateView.as_view(template_name='core/index.html'))
]

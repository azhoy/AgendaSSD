from django.views.generic import TemplateView
from django.urls import path, include, re_path

from rest_framework_nested import routers
from rest_framework_simplejwt import views as jwtviews

from . import views

# /agenda/events
event_router = routers.DefaultRouter()
event_router.register('events', viewset=views.EventViewSet, basename='events')

# /agenda/events/<event_uuid>/invitations
# /agenda/events/<event_uuid>/invitations/<invitation_uuid>
invitation_router = routers.NestedDefaultRouter(event_router, 'events', lookup='event')
invitation_router.register('invitations', viewset=views.InvitationViewSet, basename='event-invitations')

# /agenda/users/
# /agenda/users/me
# /agenda/users/set_email/
# /agenda/users/set_password/
user_router = routers.DefaultRouter()
user_router.register('users', viewset=views.CustomUserViewSet, basename='users')

# /agenda/contacts
contact_router = routers.DefaultRouter()
contact_router.register('contacts', viewset=views.ContactViewSet, basename='contacts')


app_name = 'core'
# URLConf
urlpatterns = [
    path('agenda/', include(event_router.urls)),
    path('agenda/', include(invitation_router.urls)),
    path('agenda/', include(user_router.urls)),
    path('agenda/', include(contact_router.urls)),
    re_path(r"^jwt/create/?", jwtviews.TokenObtainPairView.as_view(), name="jwt-create"),
    re_path(r"^jwt/refresh/?", jwtviews.TokenRefreshView.as_view(), name="jwt-refresh"),
    re_path(r"^jwt/verify/?", jwtviews.TokenVerifyView.as_view(), name="jwt-verify"),
    path('', TemplateView.as_view(template_name='core/index.html'))
]

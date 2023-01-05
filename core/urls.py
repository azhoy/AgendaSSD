from django.views.generic import TemplateView
from django.urls import path, include, re_path

from rest_framework_nested import routers
from rest_framework_simplejwt import views as jwtviews

from . import views

# /agenda/events/
event_router = routers.DefaultRouter()
event_router.register('events', viewset=views.EventViewSet, basename='events')

# /events/<event_uuid>/invitations/
# /agenda/events/<event_uuid>/invitations/
invitation_router = routers.NestedDefaultRouter(event_router, 'events', lookup='event')
invitation_router.register('invitations', viewset=views.InvitationViewSet, basename='event-invitations')

# /users/
# /users/me/
# /users/set_email/
# /users/set_password/
user_router = routers.DefaultRouter()
user_router.register('users', viewset=views.CustomUserViewSet, basename='users')

# /contacts/all/
contact_router = routers.DefaultRouter()
contact_router.register('all', viewset=views.ContactViewSet, basename='all')

# /requests/
contact_accept_requests_router = routers.DefaultRouter()
contact_accept_requests_router.register('requests', viewset=views.ContactAcceptViewSet, basename='requests')

# /agenda/requests/
contact_decline_request_router = routers.DefaultRouter()
contact_decline_request_router.register('decline_request', viewset=views.ContactDeclineViewSet, basename='decline_request')

# /agenda/delete_contact/
contact_delete_router = routers.DefaultRouter()
contact_delete_router.register('delete_contact', viewset=views.ContactDeleteViewSet, basename='delete_contact')

app_name = 'core'
# URLConf
urlpatterns = [
    path('', include(event_router.urls)),
    path('', include(invitation_router.urls)),
    path('', include(user_router.urls)),
    path('contacts/', include(contact_router.urls)),
    path('contacts/', include(contact_accept_requests_router.urls)),
    path('contacts/', include(contact_decline_request_router.urls)),
    path('contacts/', include(contact_delete_router.urls)),
    re_path(r"^jwt/create/?", jwtviews.TokenObtainPairView.as_view(), name="jwt-create"),
    re_path(r"^jwt/refresh/?", jwtviews.TokenRefreshView.as_view(), name="jwt-refresh"),
]

from django.views.generic import TemplateView
from django.urls import path, include, re_path

from rest_framework_nested import routers
from rest_framework_simplejwt import views as jwtviews

from . import views

# /events/
event_router = routers.DefaultRouter()
event_router.register('events', viewset=views.EventViewSet, basename='events')

# /events/<event_uuid>/invitations/
invitation_router = routers.NestedDefaultRouter(event_router, 'events', lookup='event')
invitation_router.register('invitations', viewset=views.InvitationViewSet, basename='event-invitations')

# /create_events/
create_event_router = routers.DefaultRouter()
create_event_router.register('create_events', viewset=views.CreateEventViewSet, basename='create_events')

# /users/
# /users/me/
# /users/set_email/
# /users/set_password/
user_router = routers.DefaultRouter()
user_router.register('users', viewset=views.CustomUserViewSet, basename='users')

# /contacts/all/
contact_router = routers.DefaultRouter()
contact_router.register('all', viewset=views.ContactViewSet, basename='all')

# /contacts/send_contact_request/
send_contact_request_router = routers.DefaultRouter()
send_contact_request_router.register('send_contact_request', viewset=views.AddContactRequestViewSet, basename='send_contact_request')

# /contacts/contact_requests/
contact_requests_router = routers.DefaultRouter()
contact_requests_router.register('my_contact_requests', viewset=views.SeeContactRequestViewSet, basename='my_contact_requests')


# /contacts/accept_contact_requests/
accept_contact_requests_router = routers.DefaultRouter()
accept_contact_requests_router.register('accept_contact_requests', viewset=views.AcceptContactRequestViewSet, basename='accept_contact_requests')

# /contacts/decline_contact_requests/
decline_contact_requests_router = routers.DefaultRouter()
decline_contact_requests_router.register('decline_contact_requests', viewset=views.DeclineContactRequestViewSet, basename='decline_contact_requests')

# /contacts/delete_contact/
delete_contact_router = routers.DefaultRouter()
delete_contact_router.register('delete_contact', viewset=views.DeleteContactViewSet, basename='delete_contact')

app_name = 'core'
# URLConf
urlpatterns = [
    path('', include(event_router.urls)),
    path('', include(invitation_router.urls)),
    path('', include(create_event_router.urls)),
    path('', include(user_router.urls)),
    path('contacts/', include(contact_router.urls)),
    path('contacts/', include(send_contact_request_router.urls)),
    path('contacts/', include(contact_requests_router.urls)),
    path('contacts/', include(accept_contact_requests_router.urls)),
    path('contacts/', include(decline_contact_requests_router.urls)),
    path('contacts/', include(delete_contact_router.urls)),
    re_path(r"^jwt/create/?", jwtviews.TokenObtainPairView.as_view(), name="jwt-create"),
    re_path(r"^jwt/refresh/?", jwtviews.TokenRefreshView.as_view(), name="jwt-refresh"),
    path('accounts/activate/<uid>/<token>', views.ActivateUser.as_view({'get': 'activation'}), name='activation')
]

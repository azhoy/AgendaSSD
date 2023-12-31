import re

from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMessage
from djoser.views import UserViewSet
from djoser.conf import settings as djoser_settings
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin,
    DestroyModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet

from .serializers import logger
from .models import Event, User, Invitation, ContactList, ContactRequest
from .serializers import (
    ContactSerializer, AddContactRequestSerializer, ContactRequestSerializer, HideContactSerializer,
    AcceptContactSerializer, DeclineContactSerializer, DeleteContactSerializer, HideUserSerializer,
    MyCreatedEventsSerializer, EventSerializer, UpdateEventSerializer, AddEventSerializer, HideEventsSerializers,
    InvitationsSerializer, AddInvitationsSerializer, HideInvitationsSerializer, LogoutSerializer)

# ####################################################################################################@
# Regex configuration
# ####################################################################################################@

# Client side encrypted data pattern
pattern = "\d\.(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)\|(?:[A-Za-z0-9+/]{4})*|(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)"


# ####################################################################################################@
# User Viewsets
# ####################################################################################################@


class CustomUserViewSet(UserViewSet):
    def permission_denied(self, request, **kwargs):
        raise NotFound()

    def get_queryset(self):
        user = self.request.user
        active_user = User.objects.get(id=user.id)
        # Only return the active users and is contact
        queryset = User.objects.filter(Q(id=active_user.id) | Q(friends__user_id=active_user.id))
        return queryset

    def get_serializer_context(self):
        return {
            'request': self.request,
            'username': self.request.user.username,
        }

    # Overriding default create method to remove extra information at Response
    def create(self, request, *args, **kwargs):
        protected_private_key = self.request.data['protected_private_key']
        protected_symmetric_key = self.request.data['protected_symmetric_key']

        # Checking the data received through the POST method before saving it on the server
        protected_private_key_encrypted = re.match(pattern, protected_private_key)
        protected_symmetric_key = re.match(pattern, protected_symmetric_key)

        if not protected_private_key_encrypted or not protected_symmetric_key:
            logger.warning(
                "A user a found a way to send unencrypted data to the server while registering"
            )
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(data={"message": "ok"}, status=status.HTTP_201_CREATED, headers=headers)

    # Override the '/users/me/' endpoint to prevent un-checked modifications
    # Only allowing GET method for the authenticated user
    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)

    # Deactivating methods allowing to modify credentials without email

    @action(["get"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["get"], detail=False)
    def reset_username(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["get"], detail=False)
    def reset_username_confirm(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["get"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["get"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        # this line is the only change from the base implementation.
        kwargs['data'] = {"uid": self.kwargs['uid'], "token": self.kwargs['token']}

        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(data={"message": "Account successfully activated"}, status=status.HTTP_204_NO_CONTENT)

# ####################################################################################################@
# Contacts Viewset
# ####################################################################################################@

class ContactViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    # Get => See my contact list
    def get_queryset(self):
        active_username = self.request.user.username,
        try:
            contact_list = ContactList.objects.filter(user__username=active_username[0])
            return contact_list
        except Exception as e:
            print(e)

    @action(detail=False, methods=['GET'])
    def my_contacts(self, request):
        member = User.objects.get(id=request.user.id)
        try:
            contact_list = ContactList.objects.filter(user__username=member.username)
            contacts = []
            for contact in contact_list.all():
                contact_dict = {}
                for elem in contact.get_contact_info():
                    contact_dict[f"user_id"] = elem['id']
                    contact_dict[f"username"] = elem['username']
                    contacts.append(contact_dict)
                    contact_dict = {}
            return Response(contacts)
        except Exception as e:
            print(e)


    def get_serializer_context(self):
        return {
            'request': self.request,
            'username': self.request.user.username,
        }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ContactSerializer
        return HideContactSerializer


class AddContactRequestViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    # Get => See my contact list
    def get_queryset(self):
        active_username = self.request.user.username,
        try:
            contact_list = ContactList.objects.filter(user__username=active_username[0])
            return contact_list
        except Exception as e:
            print(e)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'username': self.request.user.username,
            'username_to_add': self.request.data['username_to_add']
        }

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddContactRequestSerializer
        return HideContactSerializer

    # Overriding default create method to remove extra information
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data={"message": "ok"}, status=status.HTTP_201_CREATED, headers=headers)


class SeeContactRequestViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    # Get => See my contact list
    def get_queryset(self):
        user = self.request.user
        contact_requests = ContactRequest.objects.filter(receiver=user, is_active=True)
        return contact_requests

    def get_serializer_context(self):
        return {
            'request': self.request,
            'username': self.request.user.username,
        }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ContactRequestSerializer
        return HideContactSerializer


class AcceptContactRequestViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    # Overriding default create method to remove extra information
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data={"message": "ok"}, status=status.HTTP_201_CREATED, headers=headers)

    # Get => See my contact list
    def get_queryset(self):
        user = self.request.user
        contact_requests = ContactRequest.objects.filter(receiver=user, is_active=True)
        return contact_requests

    def get_serializer_context(self):
        return {
            'request': self.request,
            'username': self.request.user.username,
            'username_to_accept': self.request.data['username_to_accept']
        }

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AcceptContactSerializer
        return HideContactSerializer


class DeclineContactRequestViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    # Get => See my contact list
    def get_queryset(self):
        user = self.request.user
        contact_requests = ContactRequest.objects.filter(receiver=user, is_active=True)
        return contact_requests

    def get_serializer_context(self):
        return {
            'request': self.request,
            'username': self.request.user.username,
            'username_to_decline': self.request.data['username_to_decline']
        }

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DeclineContactSerializer
        return HideContactSerializer

    # Overriding default create method to remove extra information
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data={"message": "ok"}, status=status.HTTP_201_CREATED, headers=headers)


class DeleteContactViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    # Overriding default create method to remove extra information
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data={"message": "ok"}, status=status.HTTP_201_CREATED, headers=headers)

    # Get => See my contact list
    def get_queryset(self):
        user = self.request.user
        contact_requests = ContactRequest.objects.filter(receiver=user, is_active=True)
        return contact_requests

    def get_serializer_context(self):
        return {
            'request': self.request,
            'username': self.request.user.username,
            'username_to_delete': self.request.data['username_to_delete']
        }

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DeleteContactSerializer
        return HideContactSerializer


# ####################################################################################################@
# Invitation Viewset
# ####################################################################################################@

class InvitationViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddInvitationsSerializer
        return HideInvitationsSerializer

    # Overriding default create method to remove extra information
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data={"message": "ok"}, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'event_id': self.kwargs['event_pk'],
            'username': self.request.user.username,
            'username_to_invite': self.request.data['username_to_invite'],
            'protected_event_id': self.request.data['protected_event_id'],
            'protected_event_key': self.request.data['protected_event_key'],
            'protected_participants_list': self.request.data['protected_participants_list']
        }


# ####################################################################################################@
# Event Viewsets
# ####################################################################################################@

class CreateEventViewSet(
    CreateModelMixin,
    GenericViewSet
):
    queryset = Event.objects.prefetch_related('creator').all()
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddEventSerializer
        else:
            # Serializer to hide events details in the endpoint for non-related user
            return HideEventsSerializers

    def get_serializer_context(self):
        return {
            'request': self.request,
            'username': self.request.user.username,
            'protected_event_key': self.request.data['protected_event_key'],
            'title': self.request.data['title'],
            'start_date': self.request.data['start_date'],
            'end_date': self.request.data['end_date'],
            'description': self.request.data['description'],
            'location': self.request.data['location']
        }

    # Overriding default create method to remove extra information
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data={"message": "ok"}, status=status.HTTP_201_CREATED, headers=headers)


class EventViewSet(
    # ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    # queryset = Event.objects.prefetch_related('creator').all()
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Event.objects.prefetch_related('creator').all()

        active_user = User.objects.get(id=user.id)
        queryset = Event.objects.prefetch_related('creator').filter(
            creator_id=active_user.id
        )
        return queryset

    def get_serializer_context(self):
        return {
            'request': self.request,
            'username': self.request.user.username,
            'data': self.request.data
        }

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UpdateEventSerializer
        elif self.request.method == 'POST':
            return AddEventSerializer
        elif self.request.method == 'GET' and self.action == 'my_invitations':
            return InvitationsSerializer
        else:
            # Serializer to hide events details in the endpoint for non-related user
            return EventSerializer

    @action(detail=False, methods=['GET'])
    def my_invitations(self, request):
        active_user = User.objects.get(id=request.user.id)
        invitations = Invitation.objects.filter(user_invited__id=active_user.id)
        invitation_list = []
        for invitation in invitations:
            serializer = InvitationsSerializer(invitation)
            invitation_list.append(serializer.data)
        return Response(invitation_list)

    @action(detail=False, methods=['GET'])
    def my_events(self, request):
        active_user = User.objects.get(id=request.user.id)
        events = Event.objects.prefetch_related('creator').filter(creator_id=active_user.id)
        event_list = []
        for event in events:
            serializer = MyCreatedEventsSerializer(event)
            event_list.append(serializer.data)
        return Response(event_list)

    def update(self, request, *args, **kwargs):
        member = User.objects.get(id=request.user.id)
        event = Event.objects.prefetch_related('creator').get(id=kwargs['pk'])
        if getattr(event, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            event._prefetched_objects_cache = {}

        # Check if the data is encrypted
        suspect = False
        # Getting all the data sent
        for (key, value) in self.request.data.items():
            if not re.match(pattern, value):
                suspect = True
                logger.warning(
                    f"{member.username} sent unencrypted data to the server to the server while updating an event."
                    f" Locking the account"
                )
        if suspect:
            # Mail to admin
            alert_email = EmailMessage(
                'Warning alert - Django server',
                f"The user {member.username} managed to send unencrypted data"
                f"to the server to the server while updating an event. Locking out its account.",
                settings.EMAIL_HOST_USER,
                [f'{settings.ADMIN_EMAIL_ALERT}']
            )
            alert_email.send()
            # Mail to user
            info_email = EmailMessage(
                'Locking your account !',
                f"Due to suspicious activities your account was locked."
                f" Wait for administrator investigation please.",
                settings.EMAIL_HOST_USER,
                [f'{member.email}']
            )
            info_email.send()
            # Locking out the account
            member.lock_user()
        else:
            # Only the creator of the event can update this event
            if member.id == event.creator.id:
                serializer = self.get_serializer(event, data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(status=status.HTTP_200_OK)
            else:
                logger.warning(f"{member.username} tried to modify an event that's not its")
                return Response(status=status.HTTP_404_NOT_FOUND)

    # Overriding the delete method
    def destroy(self, request, *args, **kwargs):
        member = User.objects.get(id=request.user.id)
        event = Event.objects.prefetch_related('creator').get(id=kwargs['pk'])
        # Only the creator of an event can delete this event
        if member.id == event.creator.id:
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            logger.warning(f"{member.username} tried to delete an event that's not its")
            return Response(status=status.HTTP_404_NOT_FOUND)

class MyContactsEventViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):
    # queryset = Event.objects.prefetch_related('creator').all()
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users
    serializer_class = EventSerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Event.objects.prefetch_related('creator').all()

        active_user = User.objects.get(id=user.id)
        # Only fetch friends events
        queryset = Event.objects.prefetch_related('creator').filter(
            creator__friends__user_id=active_user.id
        )
        return queryset

# ####################################################################################################@
# Logout Viewsets
# ####################################################################################################@

class LogOutViewSet(
    CreateModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticated]  # All actions in this class are not available to unauthenticated users
    serializer_class = LogoutSerializer
    
    # Overriding default create method to remove extra information
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response(data={"message": "Log out."}, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'username': self.request.user.username,
            'refresh': self.request.data['refresh']
        }

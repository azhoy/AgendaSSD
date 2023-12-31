from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# ####################################################################################################@
# User model
# ####################################################################################################@

class User(AbstractUser):
    """The user model is the default authentication backend used by Django.
       Username and password are the only field required by default"""

    # A random uuid generated for each user (32 chars)
    id = models.UUIDField(primary_key=True, default=uuid4)

    # email field is used in the authentication process instead of username
    email = models.EmailField(unique=True, blank=False, null=False)

    # The public_key of the user is used to invite this user to an event
    # => The invited user public key is used to encrypt an event private key
    # => The resulting  protected_event_private_key is stored in the invitation model which is linked to an invited user
    public_key = models.TextField()

    # The protected_private_key is encrypted/decrypted on the client side with the user symmetric key
    # => Once decrypted on the client side, it's used to decrypt the protected_event_key to access event details
    protected_private_key = models.TextField()

    # The protected_symmetric_key is decrypted on the client sites with the strechted master key
    # The resulting symmetric key is used to decrypt the user data as well as the keys
    protected_symmetric_key = models.TextField()

    # An event_created field is generated from the Foreign Key 'creator' of the Event model
    # => event_created by default is a list of event id

    # The field used in the authentication system inherited from the AbstractUser model
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "public_key",
        "protected_private_key",
        "protected_symmetric_key"]

    def __str__(self):
        return self.username

    def lock_user(self):
        self.is_active = False
        self.save()

    def activate_user(self):
        self.is_active = True
        self.save()


# ####################################################################################################@
# Contact model
# ####################################################################################################@

class ContactList(models.Model):
    """List of contact of a user
    """

    # User object of the owner of the contact list
    # One contact list per users
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='user'

    )
    contacts = models.ManyToManyField(
        User,
        blank=True,
        related_name='friends'
    )

    def get_contact_info(self):
        all_contact_info = []
        contact_info = {}
        for contact in self.contacts.all():
            contact_info[f'id'] = contact.id
            contact_info[f'username'] = contact.username
            all_contact_info.append(contact_info)
            contact_info = {}
        return all_contact_info

    def add_contact(self, username_to_add):
        """
        Add a contact
        :param username_to_add: username of the user to add the contact list
        """
        if username_to_add not in self.contacts.all():
            self.contacts.add(username_to_add)
            self.save()

    def remove_contact(self, username_to_remove):
        """
        Remove a contact
        :param username_to_remove:username of the user to remove from the contact list
        """
        if username_to_remove in self.contacts.all():
            self.contacts.remove(username_to_remove)

    def unfriend(self, removee):
        """
        Initiate the action of removing a user from the contact list
        :param removee: User being removed from the contact list
        """
        remover_contact_list = self  # Person terminating the 'friendship'

        # Remove contact from the remover contact list
        remover_contact_list.remove_contact(removee)

        # Remove contact from the removee contact list
        contact_list = ContactList.objects.get(user=removee)
        contact_list.remove_contact(self.user)

    def is_mutual_contact(self, contact):
        """
        Is this a contact ?
        :param contact: Contact to check if it's a mutual
        :return (bool)
        """
        if contact in self.contacts.all():
            return True
        return False


class ContactRequest(models.Model):
    """
     A contact request is divided in 2 parts
     1. SENDER: Person initiating the contact request
     2. RECEIVER: Person receiving the contact request
    """
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sender"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="receiver"
    )
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """
        Accept a contact request
        Update both SENDER and RECEIVER contact list
        """
        (receiver_contact_list, created) = ContactList.objects.get_or_create(user=self.receiver)
        # If it exists
        if receiver_contact_list:
            receiver_contact_list.add_contact(self.sender)
            (sender_contact_list, created) = ContactList.objects.get_or_create(user=self.sender)
            if sender_contact_list:
                sender_contact_list.add_contact(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        """
        Decline a Contact request
        It is declined by setting 'is_active' field to False
        """
        self.is_active = False
        self.save()

    # Not implemented
    def cancel(self):
        """
        Cancel == Decline from the perspective of the sender of the contact request
        It is cancelled by setting 'is_active' field to False
        The difference is in the notification sent
        """
        self.is_active = False
        self.save()


# ####################################################################################################@
# Event model
# ####################################################################################################@

class Event(models.Model):
    # A random uuid generated for each user (32 chars)
    id = models.UUIDField(primary_key=True, default=uuid4)

    # The protected_event_key is encrypted/decrypted on the client side with the owner symmetric key
    # The resulting event key allows the owner to decrypt the details of its event with the event key

    # If an owner wants to invite a user to its event, he decrypts the protected_event_key on the client side with its
    # symmetric key (decrypted protected_symmetric_key using the stretched master key), then he encrypts the resulting
    # event key with the user's public key and store it in the invitation table.

    # When the invited user wants to read the details of an event he was invited to, he first decrypts its
    # protected_symmetric_key on the client with its stretched master key and get a symmetric key,
    # Then, he uses this symmetric key to decrypt its protected_private_key. Once he has his the private key,
    # He can decrypt the field 'protected_event_key' on its invitation. He is now able to read the event.
    protected_event_key = models.TextField()

    # User object of the owner of the contact list, the only field in clear in the event table
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_created'
    )
    # Event details fields encrypted the event key
    # The creator can directly decipher the protected_event_key to read them
    # Invited users need to use the protected_event_key from their invitation
    title = models.TextField()
    start_date = models.TextField()
    end_date = models.TextField(blank=True)
    description = models.TextField(blank=True)
    location = models.TextField(blank=True)
    participants = models.TextField(blank=True)

    # Methods used when an invitation is created
    # The list of participants is updated
    def update_participants(self, new_participants):
        self.participants = new_participants
        self.save()


# ####################################################################################################@
# Event Invitation model
# ####################################################################################################@

class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)

    user_invited = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_invited_to')

    protected_event_key = models.TextField()

    # Decipher this field with 'the unprotected invited_member_event_key'
    protected_event_id = models.TextField()

    # acceptedStatus = models.BooleanField(default=False)

    class Meta:
        unique_together = [['protected_event_id', 'user_invited']]

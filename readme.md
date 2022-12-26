# AgendaSSD

## Models 

- Member ( Inherits all django user models attributes (username, pwd...) ) 
  - id (PK, Auto generated, type=uuid)
  - contacts (Text)
  - created_events (List of Text, Auto generated from the creator FK of Events model)
  - invited_events (List of Text, Auto generated from the invited_member FK of EventParticipants model)

- Event
  - id (PK, Auto generated, type=uuid)
  - creator (FK => Member)
  - title (Text, Not null)
  - start_date (Text, Not null)
  - end_date (Text)
  - description (Text)
  - location (Text)
  - participants (List of Text, Auto generated from the event FK of EventParticipant model) 

- EventParticipant
  - id (PK, Auto generated, type=uuid)
  - event (FK => Event)
  - invited_member (FK => Member) 
  - acceptedStatus (Boolean) 

  - *Remark : unique constraint between event -  invited_member pairs*

## API

### Login (Create a JSON Web Token Authentication)
- request: POST 
- endpoint: /auth/jwt/create/
- send: 
{
    "username": "",
    "password": ""
}

- returned: 
  - If failed HTTP 401 Unauthorized
  - If success HTTP 200 OK 
    - an access token used to connect (5 minutes)
    - a refresh token used to get a new access token when expired (1 hour)

**CLI**
```Shell
curl -X POST http://127.0.0.1:8000/auth/jwt/create/ --data 'username=&password='
```

### Refresh a token
- request: POST 
- endpoint: /auth/users
- send: 
{
    "refresh": "",
    
}
- returned: HTTP 200 Created + a new access token 


### Register
- request: POST 
- endpoint: /auth/users
- send: 
{
    "username": "",
    "password": ""
}

- returned: HTTP 201 Created + the id and username

**CLI**
````Shell
curl -X POST http://127.0.0.1:8000/auth/users/ --data 'username=&password='
````

### Change credentials
TODO
### Get the current user
- request: HEAD 
- endpoint: /auth/user/me
- returned: HTTP 200 OK 

**CLI**
````shell
curl -LX GET http://127.0.0.1:8100/auth/users/me/ -H 'Authorization: JWT <token>'
````

### Get the current profile 
- request: HEAD 
- endpoint: /agenda/member/me
- returned: HTTP 200 OK 

**CLI**
````shell
curl -LX GET http://127.0.0.1:8100/agenda/member/me/ -H 'Authorization: JWT <token>'
````
### Create a Member profile (todo directly after registration) => Enable to link a contact list and a username
- request: POST 
- endpoint: /agenda/member/
- send: 
{
    "user_id": null,
    "contacts": ""
}
- *Remark*: 
  - A contact text fields can be added directly at profile creation or later
  - user_id is the id of a user account previously created with the /aut/users endpoints
- returned: HTTP 201 Created + the id (uuid) the user_id (int) and the contact list


### Change the contact fields from the member profile
- request: PUT 
- endpoint: /agenda/member/me
- send: 
  - Credentials: {Auth token, Key, Cred...}
  - {
    "contacts": ""
   }
- returned: HTTP 200 OK + the modified member objects (allowed)


### Display Agenda (All events)
- request: GET
- endpoint: /agenda/events/
- send: {Auth token, Key, Cred...}
- returned: HTTP 200 OK + A list of all the object (allowed view)

### Display an  event
- request: GET
- endpoint: /agenda/events/<event_uuid>
- send: {Auth token, Key, Cred...}
- returned: HTTP 200 OK + A list the event object fields (allowed view)

### Create an event
- request: POST 
- endpoint: /agenda/events/
- send: 
  - Credentials: {Auth token, Key, Cred...}
  - Event object: {
    "creator": null,
    "title": "",
    "start_date": "",
    "end_date": "",
    "description": "",
    "location": ""
  }
  - Remark: 
    - Creator must exist (uuid of a member object previously created)
    - Creator, Title and start_date fields are not null
- returned: HTTP 201 Created + A list of all the event objects (allowed view)

### Update an event 
- request: PUT 
- endpoint: /agenda/events/<event_uuid>
- send: 
  - Credentials: {Auth token, Key, Cred...}
  - Event object with modification: {
    "title": "",
    "start_date": "",
    "end_date": "",
    "description": "",
    "location": ""
  }
- returned: HTTP 200 OK + the modified event objects (allowed)

### Delete an event
- request: DELETE 
- endpoint: /agenda/events/<event_uuid>
- send: 
  - Credentials: {Auth token, Key, Cred...}
- returned: HTTP 204 No Content

### Add an invitation to a participant
- request: POST 
- endpoint: /agenda/events/<event_uuid>
- send: 
  - Credentials: {Auth token, Key, Cred...}
  - {
    "event": null,
    "invited_member": null,
    "acceptedStatus": false
   }
  - Remark: 
    - Event and invited_member are the uuid of the event and member already created
    - Event and invited_member fields are not null
    - AcceptedStatus is set to False by default
- returned: HTTP 201 Created + A list of all the invitation objects (allowed view)

### Update an invitation status 
- request: PUT 
- endpoint: /agenda/events/<event_uuid>/participants/<invitation_uuid>
- send: 
  - Credentials: {Auth token, Key, Cred...}
  - Event object with modification: {
    "acceptedStatus": true
  }
- returned: HTTP 200 OK + the modified invitation objects (allowed)


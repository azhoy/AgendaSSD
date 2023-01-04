# SSD - Agenda
## 1. Models

## 2. Features

### A) User registration, authentication and revocation
#### Register 
- **URL**: /agenda/users/
- **Method**: POST
- **Request**:
  - email
  - username
  - password
  - public_key
  - protected_private_key
  - protected_symmetric_key
- **Response**
  - HTTP_201_CREATED
    - email
    - id
    - username
    - public_key
    - protected_private_key
    - protected_symmetric_key
  - HTTP_400_BAD_REQUEST
      - email
      - id
      - username
      - public_key
      - protected_private_key
      - protected_symmetric_key
      - password
  
#### Change email
(TODO: Send confirmation link to email + SET_USERNAME_RETYPE = True)
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /users/set_email/
- **Method**: POST
- **Request**:
  - new_email
  - current_password
- Response
  - HTTP_204_NO_CONTENT
  - HTTP_400_BAD_REQUEST
    - new_email
    - current_password
    
#### Change password 
(TODO: Send confirmation link to email + SET_PASSWORD_RETYPE = True)
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /users/set_password/
- **Method**: POST
- **Request**:
  - new_password
  - re_new_password
  - current_password
- Response
  - HTTP_204_NO_CONTENT
  - HTTP_400_BAD_REQUEST
    - new_password
    - re_new_password
    - current_password
  
#### Generate JSON Web Token
- **URL**: /jwt/create/
- **Method**: POST
- **Request**:
  - email
  - password 
- Response
  - HTTP_200_OK
    - access token 
    - refresh token
  - HTTP_400_BAD_REQUEST
      - non_field_errors

#### Refresh JSON Web Token
- **URL**: /jwt/refresh/
- **Method**: POST
- **Request**:
  - refresh token
- Response
  - HTTP_200_OK
    - new access token 
  - HTTP_400_BAD_REQUEST
      - non_field_errors
  
#### Retrieve the authenticated user 
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /users/me
- **Method**:GET 
- **Request**:
- **Response**
  - HTTP_200_OK
    - user id 
    - email
    - username
    - public_key
    - protected_private_key
    - protected_symmetric_key
    - event created list
    - event invited to list
    - contact list

### B) Adding / deleting a contact
#### See my contacts
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/contacts/
- **Method**: GET
- **Request**:

- **Response**
  - HTTP_200_OK
    - List of contacts 

#### Send a contact request
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/contacts/
- **Method**: POST
- **Request**:
  - username_to_add
- **Response**
  - HTTP_201_CREATED
    - "username_to_add": ""

#### See my contact request
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/requests/
- **Method**: GET
- **Request**:

- **Response**
  - HTTP_200_OK
    - List of contacts requests
    
#### Accept contact request
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/requests/
- **Method**: POST
- **Request**:
  - username_to_accept
- **Response**
  - HTTP_201_CREATED
    - username_to_accept 
    
#### Decline contact request
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/decline_request/
- **Method**: POST
- **Request**:
  - username_to_decline
- **Response**
  - HTTP_201_CREATED
    - username_to_decline 
    
#### Delete a contact 
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/delete_contact/
- **Method**: POST
- **Request**:
  - username_to_delete
- **Response**
  - HTTP_201_CREATED
    - username_to_delete


### C) Creating, editing and deleting an event from the server

#### Add an event
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/events/
- **Method**: POST
- **Request**:
  - protected_event_key
  - title
  - start_date
  - end_date
  - description
  - location
- **Response**
  - HTTP_201_CREATED
    - protected_event_key
    - title
    - start_date
    - end_date
    - description
    - locationy
  - HTTP_400_BAD_REQUEST
      - non_fields_errors

#### Update an event (Need to be the creator of the event)
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/events/<event_id>
- **Method**: PUT
- **Request**:
  - title
  - start_date
  - end_date
  - description
  - location
- **Response**
  - HTTP_200_OK
    - protected_event_key
    - title
    - start_date
    - end_date
    - description
    - locationy
  - HTTP_400_BAD_REQUEST
      - non_fields_errors
      - 
#### Delete an event (Need to be the creator of the event)
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/events/<event_id>
- **Method**: DELETE
- **Request**:

- **Response**
  - HTTP 204 No Content
    - "message": "Event deleted"

### D) Invitation to an event
#### Invite a member to my event (Need to be the creator of the event)
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/events/<event_id>/invitations/
- **Method**: POST
- **Response**
  - HTTP 201 Created
    -  "member_invited":
    
#### Respond to an invitation (Need to be the member invited of the invitation)
TODO: Being able to PUT data without the random string at the end of the URL the RandomString 
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/events/<event_id>/invitations/RandomString
- **Method**: PUT or PATCH
- **Request**:
  - acceptedStatus (text instead of bool)
- **Response**
  - HTTP 201 Created
    -  "member_invited":

### E) Checking an agenda
#### List of events I created
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/events/
- **Method**: GET
- **Request**:

- **Response**
  - HTTP_200_OK
    - List of events
    
#### List of events I was invited to 
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/events/my_invitations/
- **Method**: GET
- **Request**:

- **Response**
  - HTTP_200_OK
    - List of events





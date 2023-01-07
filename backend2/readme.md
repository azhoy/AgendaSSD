# SSD - Agenda
## 1. Models

## 2. Features
### A) User registration, authentication and revocation
#### Register 
- **URL**: /users/
- **Method**: POST
- **Request**:
  - email
  - username
  - password
  - re_password
  - public_key
  - protected_private_key
  - protected_symmetric_key
- **Response**
  - HTTP_201_CREATED
  - HTTP_400_BAD_REQUEST
  
#### Activate an account (*)
- **URL**: #/activate/{uid}/{token}
- **URL**: /users/activation/
- **Method**: POST
- **Request**:
  - uid
  - token
- **Response**
  - HTTP_204_NO_CONTENT
  - HTTP_400_BAD_REQUEST
  - HTTP_403_FORBIDDEN (If already activated)

#### Resend activation email
- **URL**:/users/resend_activation/
- **Method**: POST
- **Request**:
  - email
- **Response**
  - HTTP_204_NO_CONTENT
  - HTTP_400_BAD_REQUEST


#### Reset username
- **URL**:#/username/reset/confirm/{uid}/{token}
- **URL**:/users/reset_email/
- **Method**: POST
- **Request**:
  - email
- **Response**
  - HTTP_204_NO_CONTENT
  - HTTP_400_BAD_REQUEST
    -  email

#### Reset username confirmation (*)
- **URL**:/users/reset_email/
- **Method**: POST
- **Request**:
  - uid
  - token
  - new_email
  - re_new_email
- **Response**
  - HTTP_204_NO_CONTENT

#### Reset password
- **URL**:#/password/reset/confirm/{uid}/{token}
- **URL**:/users/reset_email/
- **Method**: POST
- **Request**:
  - email
- **Response**
  - HTTP_204_NO_CONTENT

 #### Reset password confirmation (*)
- **URL**:/users/reset_email/
- **Method**: POST
- **Request**:
  - uid
  - token
  - new_password
  - re_new_password
- **Response**
  - HTTP_204_NO_CONTENT
  - HTTP_400_BAD_REQUEST
  
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
    - access token 
    - refresh token
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
    - username
    - public_key
    - protected_private_key
    - protected_symmetric_key

### B) Adding / deleting a contact
#### See my contacts
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /contacts/all/my_contacts/
- **Method**: GET
- **Request**:
- **Response**
  - HTTP_200_OK
    - List of contacts 

#### Send a contact request
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /contacts/send_contact_request/
- **Method**: POST
- **Request**:
  - username_to_add
- **Response**
  - HTTP_201_CREATED
    - username_to_add

#### See my contact request
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /contacts/my_contact_requests/
- **Method**: GET
- **Request**:
- **Response**
  - HTTP_200_OK
    - List of contacts requests
    
#### Accept contact request
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /contacts/accept_contact_requests/
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
- **URL**: /contacts/decline_contact_requests/
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
- **URL**: /contacts/delete_contact/
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
- **URL**: /create_events/
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
  - HTTP_400_BAD_REQUEST

#### Update an event (Need to be the creator of the event)
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /events/<event_id>
- **Method**: PUT or PATCH
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
    - location
  - HTTP_400_BAD_REQUEST
      - non_fields_errors
    
#### Delete an event (Need to be the creator of the event)
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /events/<event_id>
- **Method**: DELETE
- **Request**:
- **Response**
  - HTTP 204 No Content
    - "message": "Event deleted"

### D) Invitation to an event

#### Invite a contact to my event (Need to be the creator of the event)
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /events/<event_id>/invitations/
- **Method**: POST
- **Request**:
  - username_to_invite
  - protected_event_key: Key of the event protected with the invited member public key,
  enables to read event detail on the event table and the event id on the invitation table.
  - protected_event_id: ID of the event protected with the event key
  - protected_participants_list: The new list of participants that will replace the one on the event table
- **Response**
  - HTTP_201_Created
    
### E) Checking an agenda
#### List of events I created
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /events/my_events/
- **Method**: GET
- **Request**:
- **Response**
  - HTTP_200_OK
    - List of events

#### List of invitations
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /events/my_invitations/
- **Method**: GET
- **Request**:
- **Response**
  - HTTP_200_OK
    - List of invitations

    
#### List of events I was invited to (On the clien side)
=> Use the list of invitations to decipher the protected_event_id with the user public key and see to which event the user was invited to
=> Do it for each invitation





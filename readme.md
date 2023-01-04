# SSD - Agenda
## Models




## Endpoints
### Register 
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
  
### Retrieve the authenticated user 
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

### See all the usernames ( Useful ??? )
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /users/all_users
- **Method **:GET 
- **Request**:
- **Response **
  - HTTP_200_OK
    - list of usernames

### Generate JSON Web Token
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

### Refresh JSON Web Token
- **URL**: /jwt/refresh/
- **Method**: POST
- **Request**:
  - refresh token
- Response
  - HTTP_200_OK
    - new access token 
  - HTTP_400_BAD_REQUEST
      - non_field_errors

### Verify JSON Web Token
- **URL**: /jwt/verify/
- **Method**: POST
- **Request**:
  - token
- Response
  - HTTP_200_OK
  - HTTP_400_BAD_REQUEST
      - non_field_errors


### Change email
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
    
### Change password 
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

### Add an event
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

### Update an event (Need to be the creator of the event)
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
### Delete an event (Need to be the creator of the event)
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/events/<event_id>
- **Method**: DELETE
- **Request**:

- **Response**
  - HTTP 204 No Content
    - "message": "Event deleted"

### List of events I created
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/events/
- **Method**: GET
- **Request**:

- **Response**
  - HTTP_200_OK
    - List of events

    
### List of events I was invited to 
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/events/my_invitations/
- **Method**: GET
- **Request**:

- **Response**
  - HTTP_200_OK
    - List of events

### Invite a member to my event (Need to be the creator of the event)
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/events/<event_id>/invitations/
- **Method**: POST
- **Response**
  - HTTP 201 Created
    -  "member_invited":
    
### Respond to an invitation (Need to be the member invited of the invitation)
- **Header** : 
  - Key : Authorization
  - Value: JWT <access_token>
- **URL**: /agenda/events/<event_id>/invitations/<invitation_id>
- **Method**: PUT
- **Request**:
  - acceptedStatus (text instead of bool)
- **Response**
  - HTTP 201 Created
    -  "member_invited":

## TODO
### Secure Access with JWT (+ Find best time limit)
### 

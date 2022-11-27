

# HackerRank API server
Hackerrank RestAPI implemented using Flask Python framework.

## Goals
In order to have a scalable and efficient application, a Docker image with only RestAPI service is built up.

This allows the server to easiliy duplicate containers through Kubernetees like softwares if an heavy load of requests is received.

Also, Flask is used since it provides an efficient API building system and also it has all advantages Python language offers, such as the infinite amount of libraries a developer can use.


## Description of the API
APi uses a long list of endpoints to allow the communication from front-end to backend, they are all shown below:

```
URL: /
TYPE: GET
BODY: NONE
ENDPOINT USED IN ORDER TO SHOW ALL POSSIBLE ENDPOINTS A CLIENT CAN INTERROGATE.
IT RETURNS A LIST OF AVAILABLE ENDPOINT NAMES
```
```
URL: /login
TYPE: GET
BODY: NONE
HEADER: AUTHORIZATION: Basic base64(email:password)
ENDPOINT USED IN ORDER TO DO A LOGIN GIVEN A MAIL AND A PASSWORD.
IT SETS A COOKIE IS LOGIN IS SUCCESSFUL
```
```
URL: /login
TYPE: POST
BODY: json(email,password, name, surname, role) WHERE role=enum(user,admin,staff)
ENDPOINT USED IN ORDER TO REGISTRATE A USER INTO THE PLATFORM
```
```
URL: /logout
PERMISSIONS: LOGIN REQUIRED
TYPE: GET
BODY: NONE
ENDPOINT USED BY USERS TO PERFORM A LOGOUT IF YOU ARE ALREADY LOGGED
```
```
URL: /channel/<name>
PERMISSIONS: LOGIN REQUIRED
TYPE: GET
BODY: NONE
URL-PARAMETER: NAME OF THE CHANNEL
ENDPOINT USED IN ORDER TO GET ALL COURSES OF A SPECIFIC CHANNEL WHICH NAME IS GIVEN AS LAST PART OF ENDPOINT URL
```
```
URL: /channel
PERMISSIONS: LOGIN REQUIRED
TYPE: POST
BODY: json(channel) where channel = CHANNEL NAME
ENDPOINT USED IN ORDER TO ADD A NEW CHANNEL, ONLY ADMINS AND STAFF MEMBERS CAN PERFORM THIS ACTION
```

```
URL: /channel
PERMISSIONS: LOGIN REQUIRED
TYPE: DELETE
BODY: json(channel) where channel = CHANNEL NAME
ENDPOINT USED BY ADMINS AND STAFF MEMBERS IN ORDER TO REMOVE A CHANNEL
```

```
URL: /course/<name>
TYPE: GET
BODY: NONE
URL-PARAMETER: NAME OF THE COURSE
ENDPOINT USED IN ORDER TO GET ALL FILES AND ASSIGNMENTS OF A SPECIFIC COURSE WHICH NAME IS SPECIFIED INSIDE THE ENDOPOINT URL
NOTE: TO BE COMPLETED
```
```
URL: /course
PERMISSIONS: LOGIN REQUIRED
TYPE: POST
BODY: json(channel,course) WHERE channel = CHANNEL NAME and course = COURSE NAME
ENDPOINT USED BY ADMINS AND STAFF MEMBERS TO ADD A NEW COURSE RELATED TO A CHANNEL
```
```
URL: /course
TYPE: DELETE
BODY: json(channel,course) WHERE channel = CHANNEL NAME and course = COURSE NAME
ENDPOINT USED BY ADMINS AND STAFF MEMBERS TO REMOVE A NEW COURSE RELATED TO A CHANNEL
```
```
URL: /channel_subscription
PERMISSIONS: LOGIN REQUIRED
TYPE: GET
BODY: NONE
ENDPOINT THAT RETURNS ALL CHANNEL SUBSCRIPTIONS OF THE USER WHO COMMIT THE REQUEST
```
```
URL: /channel_subscription
PERMISSIONS: LOGIN REQUIRED
TYPE: POST
BODY: json(channel) WHERE channel = CHANNEL NAME
ENDPOINT USED BY A USER TO ADD A NEW CHANNEL SUBSCRIPTION
```
```
URL: /channel_subscription
PERMISSIONS: LOGIN REQUIRED
TYPE: DELETE
BODY: json(channel) WHERE channel = CHANNEL NAME
ENDPOINT USED BY A USER TO DELETE A NEW CHANNEL SUBSCRIPTION
```
```
URL: /course_subscription
TYPE: GET
BODY: NONE
ENDPOINT USED BY A USER TO GET ALL ITS COURSE SUBSCRIPTIONS
```
```
URL: /course_subscription
PERMISSIONS: LOGIN REQUIRED
TYPE: POST
BODY: json(course) WHERE course = COURSE NAME
ENDPOINT USED BY A USER TO ADD A NEW COURSE SUBSCRIPTION
```
```
URL: /course_subscription
PERMISSIONS: LOGIN REQUIRED
TYPE: DELETE
BODY: json(course) WHERE course = COURSE NAME
ENDPOINT USED BY A USER TO REMOVE A NEW COURSE SUBSCRIPTION
```
```
URL: /file
PERMISSIONS: LOGIN REQUIRED
TYPE: PUT
BODY: json(course,channel) WHERE course = COURSE NAME and channel = CHANNEL NAME
ENDPOINT USED BY AN ADMIN TO UPLOAD A FILE RELATED TO A COURSE AND CHANNEL
```
```
URL: /file
PERMISSIONS: LOGIN REQUIRED
TYPE: DELETE
BODY: json(course,channel,file) WHERE course = COURSE NAME, channel = CHANNEL NAME and file = FILENAME
ENDPOINT USED BY A USER TO DELETE AN ALREADY UPLOADED FILE RELATED TO A COURSE AND CHANNEL
```
```
URL: /message
PERMISSIONS: LOGIN REQUIRED
TYPE: GET
BODY: NONE
ENDPOINT USED IN ORDER TO GET ALL RECEIVED MESSAGES OF AN AUTHENTICATED USER
```
```
URL: /message
PERMISSIONS: LOGIN REQUIRED
TYPE: POST
BODY: json(receiver,object,message) WHERE receiver = RECEIVER EMAIL, object = OBJECT MESSAGE and message = MESSAGE CONTENT
ENDPOINT USED IN ORDER TO SEND A MESSAGE TO AN EXISTING USER
```
```
URL: /assignment
PERMISSIONS: LOGIN REQUIRED
TYPE: POST
BODY: json(name, year,month,day,hour,seconds, course) WHERE name = ASSIGNMENT_NAME, year,month,day,hour and seconds are related to the deadline date of the assignment and course = COURSE ASSOCIATED TO THE ASSIGNMENT
ENDPOINT USED IN ORDER TO CREATE A NEW ASSIGNMENT
```
```
URL: /assignment
PERMISSIONS: LOGIN REQUIRED
TYPE: DELETE
BODY: json(assignment,course) WHERE assignment = ASSIGNMENT_ID and course = COURSE_NAME
ENDPOINT USED IN ORDER TO DELETE AN ASSIGNMENT
NOTE: TO BE COMPLETED
```
```
URL: /exercise
PERMISSIONS: LOGIN REQUIRED
TYPE: GET
BODY: json(assignment) WHERE assignment = ASSIGNMENT ID
ENDPOINT USED IN ORDER TO GET ALL EXERCISES RELATED TO AN ASSIGNMENT
```
```
URL: /exercise
PERMISSIONS: LOGIN REQUIRED
TYPE: POST
BODY: json(quest,correct,assignment,type) OR json(quest,correct,assignment,type,wrong1,wrong2,wrong3) WHERE quest = QUEST_TEXT, correct = CORRECT_ANSWER, assignment = ASSIGNMENT_ID, type = enum(multiple,open,develop,quiz), wrong1 = WRONG1_POSSIBLE_ANSWER, wrong2 = WRONG2_POSSIBLE_ANSWER and wrong3 = WRONG3_POSSIBLE_ANSWER
ENDPOINT USED IN ORDER TO ADD A NEW EXERCISE
```
```
URL: /exercise
PERMISSIONS: LOGIN REQUIRED
TYPE: PUT
BODY: formData(file/text, language, exercise) WHERE file = FILE_UPLOADED, text = TEXT_TO_RUN, language = PROGRAM LANGUAGE OF THE FILE/TEXT, exercise = EXERCISE_ID
ENDPOINT USED IN ORDER TO UPLOAD AS USER AN EXERCISE GIVEN
```
## Authetication 

In order to have a secure login system, **Basic Authentication** and **JWT** technology are used.

First one is a technique that allows the user (client) to pass an information through an HTTP header using a precise format, so in this case for each login request, there is an _Authorization_ HTTP header where its value is a base64 hashing of username:password: 
```
Authorization: Basic base64encode(<username>:<password>)
```
for example, with username = test and password = test we have:
```
Authorization: Basic dGVzdDp0ZXN0
```

This technique doesn't secure the information but at least allows the client not to send it clearly to the server that, as it comes the request, decode the information and elaborate it.

**JWT** (_JSON Web Tokens_) technology instead allows the platform to implement a client-side session system, so the server-side of the platform that is tipically involved to store sessions is now free from this task, from now it must only handle the creation of the token and check its integrity when received.

As the name suggests, JWT is a token formed by three parts:
- Header
- Payload
- Signature

Each part is separated by a dot inside the token. 

_Header_ specifies the algorithm used to encrypt the signature and the type of the token, so for example:
```
{
  "alg": "HS256",
  "typ": "JWT"
}
```
is a valid header. This is then encrypted using base64 algorithm.

_Payload_ contains all information that identify an entity, so for example:
```
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}
```
Also the payload is base64 encoded.

Then, last part is the signature, this is built by using both encoded header and payload, a secret is added and the algorithm specified inside the header is used.
This is needed in order to test the integrity of the jwt a client send to the server because it ensures that the original token wasn't modified. 
So, for example the JWT obtained from the previous header and payload parts using as secret the worl 'secret' is:
```
{
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.XbPfbIHMI6arZ3Y922BhjWgQzWXcXNrz0ogtVhfEd2o
}
```
The generated token can be stored inside a cookie or localStorage browser, in our case it it stored inside a HTTPOnly cookie since localStorage is vulnerable to XSS attacks.


## SQLAlchemy - Persistence Level

Since the application uses a database to store information, an easy and efficient way to handle the communication between the RestAPI and the database is to have a persistence layer that allows us to maintain not only a representation of a table row of the database inside the RestAPI, but also an interface that performs all operation needed. In order to do this _SQLAlchemy_ is used.

Programming using objects is convenient, also because each row of a table can be seen as an independent object, so as written above, a representation of a row of the table as a Python object that can be easily managed without manipulating individually attributes is powerful. SQLAlchemy allows this, an example is shown below:
```
class User(database.Base):
    __tablename__ = 'user'
    email = sqlalchemy.Column(sqlalchemy.String(length=255), primary_key=True)
    password = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=False)
    salt = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String(length=255), nullable=True)
    role = sqlalchemy.Column(roles_enum, nullable=False)
    creation = sqlalchemy.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
```

When a User object is created, it can be easily added to the database using _SQLAlchemy_ interface:
```
def add_user_complete(username, password, salt, name, surname, role):
    session = database.Session()
    if role == 'user' or role == 'admin' or role == 'staff':
        try:
            newUser = User(email=username, password=password, salt=salt, name=name, surname=surname, role=role)
            session.add(newUser)
        except:
            session.rollback()
        else:
            session.commit()
```
As you can see, there is no SQL script but at the same time this program works, this happens because the library abstracts the type of the DBMS used, this allows the program to independently work from the DBMS used.

## How to individually run it



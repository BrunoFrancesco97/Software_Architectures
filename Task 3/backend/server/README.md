

# HackerRank API server
Hackerrank RestAPI implemented using Flask.

## Goals
In order to have a scalable and efficient application, a Docker image with only RestAPI service is built up.

This allows the server to easiliy duplicate containers through Kubernetees like softwares if an heavy load of requests is received.


## Small description of the API
APi uses a long list of endpoints to allow the communication from front-end to backend:

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
BODY: json(email,password, name, surname, role)
ENDPOINT USED IN ORDER TO REGISTRATE A USER INTO THE PLATFORM
```
```
URL: /logout
TYPE: GET
BODY: NONE
ENDPOINT USED BY USERS TO PERFORM A LOGOUT IF YOU ARE ALREADY LOGGED
```
```
URL: /channel/<name>
TYPE: GET
BODY: NONE
URL: NAME OF THE CHANNEL
ENDPOINT USED IN ORDER TO GET ALL COURSES OF A SPECIFIC CHANNEL WHICH NAME IS GIVEN AS LAST PART OF ENDPOINT URL
```

```


```

## How to use it





# HackerRank API server
Hackerrank RestAPI implemented using Flask.

## Goals
In order to have a scalable and efficient application, a Docker image with only RestAPI service is built up.

This allows the server to easiliy duplicate containers through Kubernetees like softwares if an heavy load of requests is received.


## Small description of the API
APi uses a long list of endpoints to allow the communication from front-end to backend:

```
TYPE: GET
BODY: NONE
ENDPOINT USED IN ORDER TO SHOW ALL POSSIBLE ENDPOINTS A CLIENT CAN INTERROGATE.
IT RETURNS A LIST OF AVAILABLE ENDPOINT NAMES
```
```
TYPE: GET
BODY: NONE
HEADER: AUTHORIZATION: Basic base64(email:password)
ENDPOINT USED IN ORDER TO DO A LOGIN GIVEN A MAIL AND A PASSWORD.
IT SETS A COOKIE IS LOGIN IS SUCCESSFUL
```
```
TYPE: POST
BODY: json(email,password, name, surname, role)
ENDPOINT USED IN ORDER TO REGISTRATE A USER INTO THE PLATFORM
```

## How to use it



# Task 3 Documentation
- added app

TODO:
- build guide (super easy)
- add backend
- final build scripts
- final dockerfiles
- final docker-compose

## Backend
Backend is composed from 3 different layers, they are:
- APIRest server
- SQLAlchemy (persistence layer)
- Database layer

These layers must interact with each other in order to have a working application and can be seen as independent layers but since APIRest server and persistence layer are both coded using Python inside the same project, they are both grouped in _Software_Architectures/Task 3/backend/server/_ folder but also in the same Docker image, meanwhile database has an own folder, all its information is stored inside _Software_Architectures/Task 3/backend/db/_ and have also an own Docker image.

### Backend Documentation
Backend documentation can be found inside each respective folder on _main_ branch, so:
- _Software_Architectures/Task 3/backend/server/_ contains a README that explains how to build and run the single image used to run the APIRest server but also it analyzes each endpoint implemented, how login was secured and a small description about SQLAlchemy, a library that allows the persistence of data between the API and the DB;
- _Software_Architectures/Task 3/backend/db/_ contains a README that explains how to build and run the single image used to run the DBMS used but also it contains a small description of the structure of our database.

'''
REPOSITORY                 TAG             IMAGE ID       CREATED          SIZE
<none>                     <none>          872e79c4df55   2 minutes ago    7.05MB
hackerrank.qg/api-server   latest          d260f2929390   6 minutes ago    931MB
hackerrank.qg/db           latest          72c320ba7d16   9 minutes ago    449MB
hackerrank.qg/app-web      latest          5474a7212982   10 minutes ago   44.1MB
'''

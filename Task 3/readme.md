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
- _APIRest_ layer
- _Persistence_ layer
- _Database_ layer

These layers must interact with each other in order to have a working application and at the same time they can be seen as independent layers but since APIRest and persistence layers are both coded using Python inside the same project, they are both grouped in _Software_Architectures/Task 3/backend/server/_ folder but also in the same Docker image, meanwhile database has an own folder, all its information is stored inside _Software_Architectures/Task 3/backend/db/_ and has also an own Docker image.

![Alt Image text](/Task%203/img/backend.png?raw=true "Backend structure")

Above is shown an image where is summarized how backend is structured.

This division of layers allows the program to scale services if needed in an efficient way and also to allow the distribution of the application. For exaxmple if there is an high load of requestes to the RestAPI server, the original container can be duplicated so to help at lowering the load of work independently from the database.

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

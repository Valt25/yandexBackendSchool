 # How to run
 This service use docker to run and deploy itself. All you need is to:
 1. Install docker and docker-compose on machine(this links can help you https://docs.docker.com/install/linux/docker-ce/ubuntu/, https://docs.docker.com/compose/install/)
 2. Then you need to install all other dependencies(git, nano and other utilities) that you will need during deploying. Unfortunately i do not know the whole configurations of every machine where this service going to be deployed. So you need to install needed dependencies according to your analysis of system and its logs.
 3. Copy sources to machine `git clone https://github.com/Valt25/yandexBackendSchool.git` (very probably you need to go in new dir `cd yandexBackendSchool`)
 4. In directory with sources you need to create file db.env `nano db.env` and put there next content:
    ``` 
    POSTGRES_DB=123
    POSTGRES_USER=qwe
    POSTGRES_PASSWORD=asd
    ```
    Hope you understand meaning of this text
  5. Also you need to create dev.env file `nano dev.env`. You can pu here debug flag:
  ``` 
  DEBUG=True
  ```
  6. You need to run `docker-compose up`
  
 ## How to test
 1. You have service running(means that you run `docker-compose up` from guide higher)
 2. Run `docker ps` to see running container
 3. Find container that represents python one(e.g. i have `yandexbackendschool_python_1`)
 4. Run next command to attach to shell of this container `docker exec -it <container-name> bash`(as on my local PC `docker exec -it yandexbackendschool_python_1 bash
`)
 5. Run `python manage.py test` to run tests of this project. Analyse logs yourself.
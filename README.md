# Datathon 2k22 - Season 2
### Team 2 - Data Crafters

```sh
Problem Statement: Dashboard that displays intelligence around time to publication (duration between acceptance and online publication)
```

## Setup

This api is built using *fastapi* library which is one of the leading and quickly buildable api library.

* /bin contains all the shell scripts etc.,
* /docs contains all the related documents of this application
* /app is the main folder which has codes
    * config.py contains all the configs
    * main.py is the main code to be ran
* /tests folder contains all the test cases

To run this, execute the below from the src folder

```sh
uvicorn main:app --reload
```
or run
```sh
python3 main.py
```
This runs on port 8000 and accessible using http://127.0.0.1:8000. 
http://127.0.0.1:8000/docs contains the Swagger docs of all the API.

To build the docker image (run this if there is a change in the dockerfile)
```sh
sh docker_setup.sh
```

Below are the internal steps that happen inside the shell script
```sh
docker build -t datathon-datacrafters .
```
datathon-datacrafters is the service name

To run the container when the above command is ran
```sh
docker run -d --name datathon -p 11202:11202 datathon-datacrafters:latest
```
11202 is the port on which this app will be running

To start and stop the container
```sh
docker start datathon
docker stop datathon
```

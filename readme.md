# Course-Curator Web App:

The repo contains the following
- courses.json file which contians all course information (as a list of courses).
```
   name: The title of the course.
   date: Creation date as a unix timestamp.
   description: The description of the course.
   domain: List of the course domain(s).
   chapters: List of the course chapters.
             Each chapter has a title name and contents text.
```

## Tasks:
1. Write a script to parse course information from courses.json, create the appropriate databases and collection(s) on a local instance of MongoDB, create the appropriate indices (for efficient retrieval)
and finally add the course data on the collection(s).

2. Write a code to create containerized application of the back-end endpoints using FastAPI.
3. Create multiple API's: 
   * Endpoint to get a list of all available courses. This endpoint needs to support 3 modes of
    sorting: Alphabetical (based on course title, ascending), date (descending) and total course
    rating (descending). Additionaly, this endpoint needs to support optional filtering of courses
    based on domain.
   * Endpoint to get the course overview.
   * Endpoint to get specific chapter information.
   * Endpoint to allow users to rate each chapter (positive/negative), while aggregating all ratings
    for each course.
4. Write test-cases for all endpoints to validate that they are working as intended.



## Installation

For the project work you need the following:
* MongoDB
* Python 3.9 or above
* Docker

### Mongo DB
To install mongodb community edition follow the steps share [here](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition) 

### Python
To install python follow the steps shown [here](https://tecadmin.net/how-to-install-python-3-9-on-ubuntu-20-04/)

### Docker
To setup docker follow the steps shown [here](https://docs.docker.com/engine/install/ubuntu/)

## Solutions:
Before we begin to test the module, Let's setup the module. Follow the below given steps to setup the repo.
_Update .env file with required parameters_
_Note: Make sure to install Python (3.9), MongoDB and Docker._

1. Clone the repo: ```git clone git@github.com:Astrix3/mongo-fastapi.git```
2. Go into the directory in which you have clone the code.
3. Install all the libraries required. ```pip install - r requirements.txt```

### Script to parse course information from courses.json
1. Get the local full path of course.json or copy the file into the module directory.
2. Run the following command to create database and collection and indexes.
```bash
python3 load_data.py  --filepath ./data/courses.json
```
### Create and Run docker container for API's
1. Run ```docker build -t getting-started .``` to build docker image locally.
2. Run ```docker run -dp 127.0.0.1:8000:8000 kimo``` to run the image built.

Now you can go to ```http://localhost:8000/docs``` to view your api and run using swagger

### Testing
* To run test cases you can simply run ```pytest``` to run all the test cases.

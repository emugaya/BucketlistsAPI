[![Build Status](https://travis-ci.org/emugaya/BucketlistsAPI.svg?branch=master)](https://travis-ci.org/emugaya/BucketlistsAPI)
[![Codeship Status for emugaya/BucketlistsAPI](https://app.codeship.com/projects/d5ebc4c0-68aa-0135-a28b-5ec5668067cc/status?branch=master)](https://app.codeship.com/projects/241446)
[![Code Climate](https://codeclimate.com/github/emugaya/BucketlistsAPI/badges/gpa.svg)](https://codeclimate.com/github/emugaya/BucketlistsAPI)
[![Test Coverage](https://codeclimate.com/github/emugaya/BucketlistsAPI/badges/coverage.svg)](https://codeclimate.com/github/emugaya/BucketlistsAPI/coverage)
[![Issue Count](https://codeclimate.com/github/emugaya/BucketlistsAPI/badges/issue_count.svg)](https://codeclimate.com/github/emugaya/BucketlistsAPI)

# Bucket Lists Application API
According to Merriam-Webster Dictionary, a Bucket List is a list of things that one has not done before but wants to do before dying.

This API is for an online Bucket List service using Flask. The Backend is being documented using Swagger API Documentation Tool.

The API has been hosted on Heroku and the link is: https://emugaya-bucketlist.herokuapp.com/api/v1/
### Specifications for the API are shown below

| EndPoint | Functionality |
| -------- | ------------- |
| [ POST /auth/login ](#) | Logs a user in |
| [ POST /auth/register ](#) | Register a user |
| [ POST /bucketlists/ ](#) | Create a new bucket list |
| [ GET /bucketlists/ ](#) | List all the created bucket lists |
| [ GET /bucketlists/\<id> ](#) | Get single bucket list |
| [ PUT /bucketlists/\<id> ](#) | Update this bucket list |
| [ DELETE /bucketlists/\<id> ](#) | Delete this single bucket list |
| [ POST /bucketlists/\<id>/items/ ](#) | Create a new item in bucket list |
| [ PUT /bucketlists/\<id>/items/<item_id> ](#) | Update a bucket list item |
| [ DELETE /bucketlists/\<id>/items/<item_id> ](#) | Delete an item from a bucketlist |


### Technology Stack:
- Python 3.5.2
- Flask-HTTPAuth==3.2.3
- flask-restplus==0.10.1
- Flask-SQLAlchemy==2.2
- gunicorn==19.7.1 (Heroku webservice)
- SQLAlchemy==1.1.11
- Install requirements using the requirements.txt file
- Postgres Database version 9.6.4 or later

### How to clone and run the Application
1. Clone the Repository
```
git clone https://github.com/emugaya/BucketlistsAPI.git
```
2. Change Directory to the root of the application folder created after cloning and Create a virtual environment using Python 3.5.2 or later
```
virtualenv .env
```
3. Activate the Virtual environement and install Requirements
```
source .env/bin/activate
pip install -r requirements.txt
```
4. Setup your postgress database using the config file provide. You can use any other database of your choice.
```
###Test Database
create database test_db;

###Development Database
create database bucketlist_db;
```
Update the `config.py` file with your database settings: `username, password, and database name` for the different environments.


5. Run Migrations:
  ```
  python3 manage.py db init
  python3 manage.py db migrate
  python3 manage.py db upgrade
  python3 manage.py db migrate

  ```
6. Test the Application:
```
nosetests tests
```
6. Activate the Development environment and start the application by running:
```
python3 run.py
```

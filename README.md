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
| [ DELETE /bucketlists/\<id>/items/<item_id> ](#) | Delete an item in a bucket list |


### Technology Stack:
- Python 3.5.2
- Flask-HTTPAuth==3.2.3
- flask-restplus==0.10.1
- Flask-SQLAlchemy==2.2
- gunicorn==19.7.1 (Heroku webservice)
- SQLAlchemy==1.1.11
- Install requirements using the requirements.txt file

### How to clone and run the Application
1. Clone this Repository.
2. Create a virtual environment using Python 3.5.2 or later
3. Install all requirements using pip install requirements.txt
4. Setup your postgress database using the config file provide. You can use any other database of your choice.
5. Create an an automatic environment variable file and run it. This should have the mode your running the application in
6. Run the migrations using python3 manage.py db init, python3 manage.py db migrate,python3 manage.py db migrate,
6. Start the application by running python3 run.py







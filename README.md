# **Twitter App Clone** - *Backend*

## Description

- This project aims to clone the Twitter app using RESTful API architecture. It has been built using Django and the Django REST Framework.

- It is a simple CRUD API that allows users to create, read, update and delete posts, comment on posts, and follow other users.

## Setup / Installation Instructions

1. Clone the repository

2. Install the project requirements using the command below:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file at the root of the project and add the following configurations:

    ```bash
    SECRET_KEY='<your_secret_key>'
    DEBUG=True
    ```

4. Run the migrations using the following commands:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser account using the command below: (follow the prompts)

    ```bash
    python manage.py createsuperuser
    ```

6. Run the server using the command below:

    ```bash
    python manage.py runserver
    ```

7. Open the browser and navigate to [`localhost:8000/api/v1`](localhost:8000/api/v1) to access the API endpoints on the browsable API.

8. In order to view the API endpoints on the browsable API, you need to be logged in:

- To register a new user, navigate to [`http://localhost:8000/api/v1/register/`](http://localhost:8000/api/v1/register/) and input the required details.

- If using the browsable API, you can go to [`http://localhost:8000/api/v1/rest-auth/login/`](http://localhost:8000/api/v1/rest-auth/login/) to login this will log you by creating a session cookie that will be used to authenticate you for the rest of the session.

- If using a API client like Postman, you can login by sending a POST request [`http://localhost:8000/api/v1/login/`](http://localhost:8000/api/v1/login/) with the following payload:

    ```json
    {
        "username": "<your_username>",
        "password": "<your_password>"
    }
    ```

- If the login is successful, you will receive a response with the following payload:

    ```json
    {
        "token": "<your_token_key>"
    }
    ```

- From there, all you need to do is append the token to the Authorization header of all subsequent requests in the format:

    ```bash
    Authorization: Token <your_token_key>
    ```

- You can now access all the API endpoints on the browsable API.

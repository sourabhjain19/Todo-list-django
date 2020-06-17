# Todo-list-django

Following are the steps to run this project on your machine

1. Run command ```pip install django-admin```
2. Edit EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in todolist/setting.py file.
3. Edit the `from email address` on line no 96 in todos/views.py file.  
4. Go to the project folder and run command ```python manage.py migrate```
5. In the same folder run command ```python manage.py runserver```
6. Development server will be up on http://127.0.0.1:8000/todos.

This app is currently hosted on https://todolist-django-sourabh.herokuapp.com/todos/

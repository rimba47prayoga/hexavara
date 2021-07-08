# Hexavara test
## Project setup
### Install Python
`required python v3.6`

In the project directory, you can run:

`pip install -r requirements.txt`

Make sure you have created / import database with name `hexavara_questions_phonebilling`
or if you want to change database settings you can open `settings.py` at line 91

#### For Unix / Linux
`./manage.py migrate`

#### For Windows
`python manage.py migrate`

### Run project

#### For Unix / Linux
`./manage runserver`

#### For Windows
`python manage.py runserver`

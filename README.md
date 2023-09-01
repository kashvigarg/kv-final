# Backend for MY-TRAIL (Kavach'23)

Web server that accepts bank statements in csv format, and processes them to highlight fraud-prone transactions.

# Project Structure
Please refer the [documentation](https://docs.djangoproject.com/en/4.2/) to clearly understand main project, app and admin structure. 


# Project Dependencies
- `djangorestframework 3.14.0`
- `Django 4.2.3`
- `scikit-learn 1.3.0`
- `seaborn 0.12.2`
- `numpy 1.25.1`
- `pandas 2.0.3`


# Local Development

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/kashvigarg/kv-final.git
    $ cd kavach
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py makemigrations
    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver

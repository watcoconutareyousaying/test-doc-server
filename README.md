# Test Document Creation Repository

This repository is designed to manage the creation and export of various test documents. The following activities are supported:
- **Test Plan Creation**
- **Test Case Creation**
- **Test Coverage**
- **Bug Report Generation**
- **Test Report Generation**

You can create, edit, and export these documents to Excel (XLSX) format.

## Features:
- Create and manage test plans, test cases, and bug reports.
- Track test coverage and generate detailed test reports.
- Export documents to Excel (XLSX) format for easy sharing and record-keeping.

## Installation

Clone the repository:
   ```bash
   git clone https://github.com/watcoconutareyousaying/TEST-DOCUMENT.git
```
Create and activate a virtual environment (optional but recommended):

```
python3 -m venv env 
```
On Mac use `source env/bin/activate`,  On Windows use `env\Scripts\activate`

### Install required dependencies:

_A guide on how to install the tools needed for running the project._


```bash
pip install -r requirements.txt
```
Set up the database configuration in settings.py based on your choice of database (SQLite, MySQL, PostgreSQL).

#### Database Setup
By default, the project is configured to use `SQLite`. If you're using `MySQL` or `PostgreSQL`, make sure to update the DATABASES settings in `settings.py` accordingly.

##### For PostgreSQL:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
##### For MySQL:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### Running the Project
Apply migrations to set up the database: 
```
python manage.py migrate
```
Create a superuser to access the admin panel (optional):
```
python manage.py createsuperuser
```
Run the development server:
```
python manage.py runserver
```

## Technologies

_Name the technologies used in the project._ 
* [Django Rest Framework](https://www.django-rest-framework.org/) - Framework Used.
* [django-extensions](https://django-extensions.readthedocs.io/en/latest/installation_instructions.html) - install graph model generation.

### Generate a graph model using this command
```bash
python manage.py graph_models -a -g -o api_models.dot
```

#### The graph_models command has several options to customize the output:


- ```-a``` or ```--all-applications``` : Generate the graph for all applications in INSTALLED_APPS.

- ```-g``` or ```--group-models``` : Group models by application.

- ```-o``` or ```--output``` : Specify the output file name and format (e.g., png, jpg).

- ```-l``` or ```--layout``` : Choose a GraphViz layout algorithm (e.g., circo, dot, fdp).

- ```-t``` or ```--theme``` : Select a theme for the graph (e.g., original, django2018).
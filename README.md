# Test Management Backend System

This backend solution is designed to streamline and automate the process of test management for employees involved in quality assurance (QA) and software testing. It offers a comprehensive suite of features to manage test plans, test cases, test coverage, defect reports, and test reports, while providing the ability to export all relevant data into Excel files for easy sharing and documentation.

## Features

### 1. **Create Test Plans**

- Design and define structured test plans that outline testing objectives, scope, resources, schedules, and more.
- Ensures all aspects of the testing process are well-organized and aligned with project goals.

### 2. **Define Test Cases**

- Easily create and manage individual test cases, detailing specific testing steps, expected outcomes, and conditions.
- Enables systematic and repeatable execution of tests.

### 3. **Manage Test Coverage**

- Track and generate test coverage reports to ensure all application features and requirements are tested.
- Ensures comprehensive testing by covering all necessary areas.

### 4. **Log and Track Defects**

- Generate defect reports documenting issues identified during testing.
- Track defect status, severity, priority, and resolutions for improved defect management.

### 5. **Generate Test Reports**

- Automatically generate detailed test reports summarizing test execution results, pass/fail status, and defects.
- Essential for assessing the quality of the application and providing insights for improvement.

### 6. **Export to Excel**

- Export test plans, test cases, coverage reports, defect logs, and test reports into Excel files.
- Easy to share, document, and archive testing progress and outcomes.

## Key Features

- **Seamless Integration**: Connects all aspects of the testing lifecycle into a unified system, reducing manual effort and improving productivity.
- **Automation**: Automates the creation of test reports, test coverage, and defect tracking, minimizing human errors and speeding up the process.
- **Excel Export**: Provides an easy-to-use export feature for sharing and documenting testing progress.
- **Centralized Repository**: Stores all testing artifacts in one place for easy access and management.
- **Customization**: Supports customization to fit the needs and workflows of different QA teams and projects.

## Benefits

- **Improved Efficiency**: Reduces time and effort spent manually compiling and updating testing documents, allowing employees to focus on more critical tasks.
- **Enhanced Reporting**: Offers structured reports that provide insights into the testing process, helping teams make informed decisions.
- **Data-Driven Insights**: Identifies weaknesses in the application through test coverage and defect tracking, allowing teams to address issues before product release.

## Installation

Clone the repository:

```bash
git clone https://github.com/watcoconutareyousaying/test-doc-server.git
```

Create and activate a virtual environment (optional but recommended):

```
python3 -m venv env
```

On Mac use `source env/bin/activate`, On Windows use `env\Scripts\activate`

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

- [Django Rest Framework](https://www.django-rest-framework.org/) - Framework Used.
- [django-extensions](https://django-extensions.readthedocs.io/en/latest/installation_instructions.html) - install graph model generation.

### Generate a graph model using this command

```bash
python manage.py graph_models -a -g -o api_models.dot
```

#### The graph_models command has several options to customize the output:

- `-a` or `--all-applications` : Generate the graph for all applications in INSTALLED_APPS.

- `-g` or `--group-models` : Group models by application.

- `-o` or `--output` : Specify the output file name and format (e.g., png, jpg).

- `-l` or `--layout` : Choose a GraphViz layout algorithm (e.g., circo, dot, fdp).

- `-t` or `--theme` : Select a theme for the graph (e.g., original, django2018).

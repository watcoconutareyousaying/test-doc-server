# 

To generate a graph model

## Installation

Use the package manager [django-extensions](https://django-extensions.readthedocs.io/en/latest/installation_instructions.html) to install graph model generation.

```bash
pip install django-extensions
```
##

The graph_models command has several options to customize the output:

1) ```-a``` or ```--all-applications``` : Generate the graph for all applications in INSTALLED_APPS.
2) ```-g``` or ```--group-models``` : Group models by application.
3) ```-o``` or ```--output``` : Specify the output file name and format (e.g., png, jpg).
4) ```-l``` or ```--layout``` : Choose a GraphViz layout algorithm (e.g., circo, dot, fdp).
5) ```-t``` or ```--theme``` : Select a theme for the graph (e.g., original, django2018).

## Generate a graph model using this command

```bash
python manage.py graph_models -a -g -o api_models.dot
```

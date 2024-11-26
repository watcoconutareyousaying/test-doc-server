from django.urls import path
from api.views import *

urlpatterns = [
    path('project/', project_list, name='project'),
    path('project-detail/<int:pk>/', project_detail, name='project_detail'),
    path('testplan/', testplan_list, name='test-plan'),
    path('testplan_detail/<int:pk>', testplan_detail, name='test-plan-detail')
]

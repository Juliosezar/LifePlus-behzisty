from django.urls import path
from . import views
app_name = 'cases'

urlpatterns = [
    path('', views.CaseCreateView.as_view(), name='new_case'),
]

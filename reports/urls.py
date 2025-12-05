from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('cases-report/', views.CaseReportView.as_view(), name='case_report'),
    path('cases/export/', views.export_cases_to_excel, name='case_export'),
]

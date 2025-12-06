from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('cases-report/', views.CaseReportView.as_view(), name='case_report'),
    path('cases/export/', views.export_cases_to_excel, name='case_export'),
    path('cases/expired-visits/', views.ExpiredVisitsView.as_view(), name='expired_visits'),
    path('cases/expired-commissions/', views.ExpiredCommissionsView.as_view(), name='expired_commissions'),
    path('cases/expired-cards/', views.ExpiredDisabilityCardsView.as_view(), name='expired_cards'),
    path('cases/demands/', views.AllDemandsListView.as_view(), name='all_demands'),


]

from django.urls import path
from . import views
app_name = 'cases'

urlpatterns = [
    path('', views.CaseCreateView.as_view(), name='new_case'),
    path('case/<int:pk>/', views.CaseDetailView.as_view(), name='case_detail'),
    path('case/<int:pk>/edit/', views.CaseUpdateView.as_view(), name='case_edit'),
    path('case/<int:pk>/delete/', views.CaseDeleteView.as_view(), name='case_delete'),
    path('case/<int:pk>/upload/', views.CaseDocumentUploadView.as_view(), name='upload_document'),
    path('cases/search/', views.CaseSearchView.as_view(), name='case_search'),
    path('document/<int:pk>/delete/', views.DeleteCaseDocumentView.as_view(), name='delete_document'),
    path('case/<int:pk>/services/<str:form_type>/', views.CaseServicesView.as_view(), name='case_services'),
    path('case/<int:pk>/add-note/', views.CaseNoteCreateView.as_view(), name='add_note'),
    path('case/<int:pk>/add-visit/', views.VisitCreateView.as_view(), name='add_visit'),


]


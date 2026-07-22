from django.urls import path
from . import views

app_name = 'ai_chat'

urlpatterns = [
    path('', views.ChatPageView.as_view(), name='chat'),
    path('api/', views.ChatAPIView.as_view(), name='chat_api'),
    path('api/export/<int:message_id>/', views.ExportExcelView.as_view(), name='export_excel'),
]

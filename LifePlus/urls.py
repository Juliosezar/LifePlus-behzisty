
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(url="/accounts/home/")),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('cases/', include('cases.urls'), name='cases'),
    path('reports/', include('reports.urls'), name='reports'),
]

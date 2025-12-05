from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import SearchForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        # Redirect to 'home' after successful login
        return reverse_lazy('accounts:home')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


class HomeView(LoginRequiredMixin, FormView):
    template_name = 'accounts/home.html'
    form_class = SearchForm

    def __init__(self, *args, **kwargs):
        from cases.tmp import move, upload
        #move()
        #upload()
        super().__init__(*args, **kwargs)


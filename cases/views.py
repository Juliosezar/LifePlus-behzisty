from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Case
from .forms import CaseForm

class CaseCreateView(LoginRequiredMixin, CreateView):
    model = Case
    form_class = CaseForm
    template_name = 'cases/new_case.html'
    success_url = reverse_lazy('home') # Redirects to dashboard after success

    def form_valid(self, form):
        # If you need to do anything with the user, do it here
        # form.instance.created_by = self.request.user
        return super().form_valid(form)

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .forms import (
    CaseForm,
    CaseDisabilityFormSet,
    ReasonCaseFormSet,
    RecoveredReasonCaseFormSet,
    CaseFamilyMemberFormSet,
    CaseNotesFormSet,
    CaseDocumentForm,
    CaseNoteForm,
    DemandForm, 
    ServiceProvidedForm, 
    VisitForm
)
from .models import Case, CaseDocuments, CaseNotes,  Visit
from django.views.generic import View
from django.db.models import Q


class CaseCreateView(LoginRequiredMixin, CreateView):
    model = Case
    form_class = CaseForm
    template_name = 'cases/new_case.html'

    def get_success_url(self):
        return reverse_lazy('cases:case_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['disabilities'] = CaseDisabilityFormSet(self.request.POST)
            data['reasons'] = ReasonCaseFormSet(self.request.POST)
            data['recovered'] = RecoveredReasonCaseFormSet(self.request.POST)
            data['family'] = CaseFamilyMemberFormSet(self.request.POST)
            data['notes'] = CaseNotesFormSet(self.request.POST)
        else:
            data['disabilities'] = CaseDisabilityFormSet()
            data['reasons'] = ReasonCaseFormSet()
            data['recovered'] = RecoveredReasonCaseFormSet()
            data['notes'] = CaseNotesFormSet()
            data['family'] = CaseFamilyMemberFormSet(initial=[
                {'relation': 'father'}, 
                {'relation': 'mother'}
            ])
        data['is_edit'] = False
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        disabilities = context['disabilities']
        reasons = context['reasons']
        recovered = context['recovered']
        family = context['family']
        notes = context['notes']

        if (disabilities.is_valid() and reasons.is_valid() and 
            recovered.is_valid() and family.is_valid() and notes.is_valid()):
            
            with transaction.atomic():
                self.object = form.save()
                
                disabilities.instance = self.object
                reasons.instance = self.object
                recovered.instance = self.object
                family.instance = self.object
                notes.instance = self.object

                disabilities.save()
                reasons.save()
                recovered.save()
                family.save()

                note_instances = notes.save(commit=False)
                for note in note_instances:
                    note.added_by = self.request.user
                    note.save()
                
                for deleted_object in notes.deleted_objects:
                    if deleted_object.pk:
                        deleted_object.delete()

            return super().form_valid(form)
        
        else:
            return self.render_to_response(self.get_context_data(form=form))


class CaseUpdateView(LoginRequiredMixin, UpdateView):
    model = Case
    form_class = CaseForm
    template_name = 'cases/edit_case.html'

    def get_success_url(self):
        return reverse_lazy('cases:case_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['disabilities'] = CaseDisabilityFormSet(self.request.POST, instance=self.object)
            data['reasons'] = ReasonCaseFormSet(self.request.POST, instance=self.object)
            data['recovered'] = RecoveredReasonCaseFormSet(self.request.POST, instance=self.object)
            data['family'] = CaseFamilyMemberFormSet(self.request.POST, instance=self.object)
            data['notes'] = CaseNotesFormSet(self.request.POST, instance=self.object)
        else:
            data['disabilities'] = CaseDisabilityFormSet(instance=self.object)
            data['reasons'] = ReasonCaseFormSet(instance=self.object)
            data['recovered'] = RecoveredReasonCaseFormSet(instance=self.object)
            data['family'] = CaseFamilyMemberFormSet(instance=self.object)
            data['notes'] = CaseNotesFormSet(instance=self.object)
        
        data['is_edit'] = True
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        disabilities = context['disabilities']
        reasons = context['reasons']
        recovered = context['recovered']
        family = context['family']
        notes = context['notes']

        if (disabilities.is_valid() and reasons.is_valid() and 
            recovered.is_valid() and family.is_valid() and notes.is_valid()):
            
            with transaction.atomic():
                self.object = form.save()
                disabilities.save()
                reasons.save()
                recovered.save()
                family.save()
                
                notes.instance = self.object
                note_instances = notes.save(commit=False)
                
                for note in note_instances:
                    if not note.pk: 
                        note.added_by = self.request.user
                    note.save()
                
                for deleted_object in notes.deleted_objects:
                    if deleted_object.pk: 
                        deleted_object.delete()

            return super().form_valid(form)
        
        else:
            return self.render_to_response(self.get_context_data(form=form))



class CaseDetailView(LoginRequiredMixin, DetailView):
    model = Case
    template_name = 'cases/case_detail.html'
    context_object_name = 'case'

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'disabilities',
            'reasons',
            'recovered_reasons',
            'family',
            'casenotes_set',
            'casedocuments_set', 
            'visits'
        )


class CaseDeleteView(LoginRequiredMixin, DeleteView):
    model = Case
    template_name = 'cases/case_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('accounts:home')





class CaseDocumentUploadView(LoginRequiredMixin, CreateView):
    model = CaseDocuments
    form_class = CaseDocumentForm
    template_name = 'cases/upload_document.html'

    def form_valid(self, form):
        case = get_object_or_404(Case, pk=self.kwargs['pk'])
        
        form.instance.case = case
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['case'] = get_object_or_404(Case, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('cases:case_detail', kwargs={'pk': self.kwargs['pk']})


class DeleteCaseDocumentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        document = get_object_or_404(CaseDocuments, pk=pk)
        case_id = document.case.pk
        
        document.delete()
        
        return redirect('cases:case_detail', pk=case_id)



class CaseSearchView(LoginRequiredMixin, ListView):
    model = Case
    template_name = 'cases/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('search')
        
        if query:
            return Case.objects.filter(
                Q(first_name__icontains=query) | 
                Q(last_name__icontains=query) | 
                Q(national_id__icontains=query)
            )
        return Case.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('search', '')
        return context


from .models import Case, Demands, Services_provided
from .forms import DemandForm, ServiceProvidedForm

class CaseServicesView(LoginRequiredMixin, View):
    template_name = 'cases/case_services.html'

    def get(self, request, pk, form_type):
        case = get_object_or_404(Case, pk=pk)
        self.form_type = form_type
        demand_form = DemandForm(prefix='demand')
        service_form = ServiceProvidedForm(prefix='service')
        
        return render(request, self.template_name, {
            'case': case,
            'demand_form': demand_form,
            'service_form': service_form,
            'form_type': form_type
        })

    def post(self, request, pk, form_type):
        case = get_object_or_404(Case, pk=pk)
        
        if 'submit_demand' in request.POST:
            demand_form = DemandForm(request.POST, prefix='demand')
            service_form = ServiceProvidedForm(prefix='service') # Empty other form
            
            if demand_form.is_valid():
                demand = demand_form.save(commit=False)
                demand.case = case
                demand.save()
                return redirect('cases:case_detail', pk=pk)
                
        elif 'submit_service' in request.POST:
            service_form = ServiceProvidedForm(request.POST, prefix='service')
            demand_form = DemandForm(prefix='demand') # Empty other form
            
            if service_form.is_valid():
                service = service_form.save(commit=False)
                service.case = case
                service.save()
                return redirect('cases:case_detail', pk=pk)
        
        return render(request, self.template_name, {
            'case': case,
            'demand_form': demand_form,
            'service_form': service_form,
            'form_type': form_type
        })



class CaseNoteCreateView(LoginRequiredMixin, CreateView):
    model = CaseNotes
    form_class = CaseNoteForm
    template_name = 'cases/add_note.html'

    def form_valid(self, form):
        case = get_object_or_404(Case, pk=self.kwargs['pk'])
        form.instance.case = case
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['case'] = get_object_or_404(Case, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('cases:case_detail', kwargs={'pk': self.kwargs['pk']})




class VisitCreateView(LoginRequiredMixin, CreateView):
    model = Visit
    form_class = VisitForm
    template_name = 'cases/add_visit.html'

    def form_valid(self, form):
        case = get_object_or_404(Case, pk=self.kwargs['pk'])
        form.instance.case = case
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['case'] = get_object_or_404(Case, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('cases:case_detail', kwargs={'pk': self.kwargs['pk']})




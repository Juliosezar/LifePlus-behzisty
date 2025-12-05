from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .models import Case
from .forms import (
    CaseForm,
    CaseDisabilityFormSet,
    ReasonCaseFormSet,
    RecoveredReasonCaseFormSet,
    CaseFamilyMemberFormSet,
    CaseNotesFormSet
)
from .models import Case, CaseDocuments
from .forms import CaseDocumentForm
from django.views.generic import View
from django.db.models import Q
from django.views.generic import ListView
from .models import Case




# ==========================================
# 1. CREATE VIEW
# ==========================================
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

        # 1. Check validity of ALL formsets *before* saving anything
        if (disabilities.is_valid() and reasons.is_valid() and 
            recovered.is_valid() and family.is_valid() and notes.is_valid()):
            
            with transaction.atomic():
                # 2. Now it is safe to save the Parent Case
                self.object = form.save()
                
                # 3. Assign the new Case instance to all formsets
                disabilities.instance = self.object
                reasons.instance = self.object
                recovered.instance = self.object
                family.instance = self.object
                notes.instance = self.object

                # 4. Save Standard Formsets
                disabilities.save()
                reasons.save()
                recovered.save()
                family.save()

                # 5. Save Notes (Custom Logic for User)
                note_instances = notes.save(commit=False)
                for note in note_instances:
                    note.added_by = self.request.user
                    note.save()
                
                # Handle deleted notes
                for deleted_object in notes.deleted_objects:
                    if deleted_object.pk:
                        deleted_object.delete()

            return super().form_valid(form)
        
        else:
            # If any formset is invalid, we do NOT save the Case.
            # We re-render the page with errors.
            return self.render_to_response(self.get_context_data(form=form))


# ==========================================
# 2. UPDATE VIEW
# ==========================================
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

        # 1. Check validity of ALL formsets first
        if (disabilities.is_valid() and reasons.is_valid() and 
            recovered.is_valid() and family.is_valid() and notes.is_valid()):
            
            with transaction.atomic():
                # 2. Save the Parent Case changes
                self.object = form.save()
                
                # 3. Save Standard Formsets (Handles Add/Update/Delete automatically)
                disabilities.save()
                reasons.save()
                recovered.save()
                family.save()
                
                # 4. Save Notes (Custom Logic)
                notes.instance = self.object
                note_instances = notes.save(commit=False)
                
                for note in note_instances:
                    # Only set user for NEW notes
                    if not note.pk: 
                        note.added_by = self.request.user
                    note.save()
                
                # Manual delete for notes
                for deleted_object in notes.deleted_objects:
                    if deleted_object.pk: 
                        deleted_object.delete()

            return super().form_valid(form)
        
        else:
            # If invalid, don't save changes to Case, just reload
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
        # Get the case from the URL parameter
        case = get_object_or_404(Case, pk=self.kwargs['pk'])
        
        # Attach the case to the document instance
        form.instance.case = case
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the case to the template for the header/back button
        context['case'] = get_object_or_404(Case, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        # Redirect back to the Case Detail page
        return reverse_lazy('cases:case_detail', kwargs={'pk': self.kwargs['pk']})


class DeleteCaseDocumentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Find the document
        document = get_object_or_404(CaseDocuments, pk=pk)
        
        # Store case ID to redirect back later
        case_id = document.case.pk
        
        # Delete the object (and the file from S3 usually, handled by django-storages)
        document.delete()
        
        # Redirect back to the case detail page
        return redirect('cases:case_detail', pk=case_id)



class CaseSearchView(LoginRequiredMixin, ListView):
    model = Case
    template_name = 'cases/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('search')
        
        if query:
            # Filter by First Name OR Last Name OR National ID
            return Case.objects.filter(
                Q(first_name__icontains=query) | 
                Q(last_name__icontains=query) | 
                Q(national_id__icontains=query)
            )
        return Case.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the search term back to the template to show "Results for: ..."
        context['query'] = self.request.GET.get('search', '')
        return context

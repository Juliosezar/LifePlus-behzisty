from django.shortcuts import render
from django.views.generic import ListView
from cases.models import Case
from .forms import CaseReportForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CaseReportForm


class CaseReportView(LoginRequiredMixin, ListView):
    model = Case
    template_name = 'reports/report.html'
    context_object_name = 'cases'

    def get_queryset(self):
        # Start with all cases, ordered by newest
        queryset = Case.objects.all().order_by('-created_at')
        
        if self.request.GET:
            form = CaseReportForm(self.request.GET)
            if form.is_valid():
                data = form.cleaned_data
                
                # List of all filter fields in your form
                filter_fields = [
                    'gender', 'case_type', 'military_serveice', 'pension_status',
                    'housing_status', 'education', 'insurance', 
                    'residencial_area', 'marrige_status'
                ]

                # Loop through and apply filters if data exists
                for field in filter_fields:
                    if data.get(field):
                        # Construct the lookup keyword dynamically (e.g., gender__in)
                        lookup = f"{field}__in"
                        queryset = queryset.filter(**{lookup: data[field]})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CaseReportForm(self.request.GET or None)
        return context


import openpyxl
from django.http import HttpResponse
from cases.models import Case
from .forms import CaseReportForm

def export_cases_to_excel(request):
    # 1. RE-APPLY FILTERS (Same logic as CaseReportView)
    queryset = Case.objects.all().order_by('-created_at')
    
    if request.GET:
        form = CaseReportForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            filter_fields = [
                'gender', 'case_type', 'military_serveice', 'pension_status',
                'housing_status', 'education', 'insurance', 
                'residencial_area', 'marrige_status'
            ]
            for field in filter_fields:
                if data.get(field):
                    lookup = f"{field}__in"
                    queryset = queryset.filter(**{lookup: data[field]})

    # 2. CREATE WORKBOOK
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "گزارش پرونده ها"
    ws.sheet_view.rightToLeft = True # Set sheet direction for Persian

    # 3. ADD HEADERS
    headers = [
        'نام', 'نام خانوادگی', 'کد ملی', 'جنسیت', 'نوع پرونده', 
        'شماره تماس', 'تحصیلات', 'وضعیت مسکن', 'بیمه', 'وضعیت تاهل'
    ]
    ws.append(headers)

    # 4. ADD DATA ROWS
    for case in queryset:
        row = [
            case.first_name,
            case.last_name,
            case.national_id,
            case.get_gender_display(),          # Use display value (e.g. 'مرد' not 'M')
            case.get_case_type_display(),
            case.phone_number,
            case.get_education_display(),
            case.get_housing_status_display(),
            case.get_insurance_display(),
            case.get_marrige_status_display(),
        ]
        ws.append(row)

    # 5. PREPARE RESPONSE
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="cases_report.xlsx"'
    
    wb.save(response)
    return response

from django.views.generic import ListView
from cases.models import Case
from .forms import CaseReportForm
from django.contrib.auth.mixins import LoginRequiredMixin
import openpyxl
from django.http import HttpResponse
from django.db.models import Max
from datetime import timedelta
import datetime
import jdatetime
from cases.models import CaseDocuments
from cases.models import Demands
from django.db.models import Q




class CaseReportView(LoginRequiredMixin, ListView):
    model = Case
    template_name = 'reports/report.html'
    context_object_name = 'cases'

    def get_queryset(self):
        queryset = Case.objects.all().order_by('-created_at').prefetch_related('disabilities', 'reasons', 'recovered_reasons')
        
        if self.request.GET:
            form = CaseReportForm(self.request.GET)
            if form.is_valid():
                data = form.cleaned_data
                
                filter_fields = [
                    'gender', 'case_type', 'military_serveice', 'pension_status',
                    'housing_status', 'education', 'insurance', 
                    'residencial_area', 'marrige_status', 'birth_date_from', 'birth_date_to',
                    'disability_type', 'disability_level', 'reasons', 'recovered_reasons'
                ]

                for field in filter_fields:
                    if data.get(field):

                        if field == 'disability_type':
                            queryset = queryset.filter(disabilities__disability_type__in=data[field])
                        elif field == 'disability_level':
                            queryset = queryset.filter(disabilities__disability_level__in=data[field])

                        elif field == 'birth_date_from' or field == 'birth_date_to':
                            if not data['birth_date_from']:
                                queryset = queryset.filter(date_of_birth__lte=data['birth_date_to'])
                            elif not data['birth_date_to']:
                                queryset = queryset.filter(date_of_birth__gte=data['birth_date_from'])
                            else:
                                queryset = queryset.filter(date_of_birth__gte=data['birth_date_from'], date_of_birth__lte=data['birth_date_to'])
                        elif field == 'reasons':
                            queryset = queryset.filter(reasons__reason__in=data[field])
                        elif field == 'recovered_reasons':
                            queryset = queryset.filter(recovered_reasons__reason__in=data[field])
                        else:
                            lookup = f"{field}__in"
                            queryset = queryset.filter(**{lookup: data[field]})

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CaseReportForm(self.request.GET or None)
        return context




def export_cases_to_excel(request):
    queryset = Case.objects.all().order_by('-created_at').prefetch_related('reasons', 'disabilities', 'recovered_reasons')
    
    if request.GET:
        form = CaseReportForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            
            filter_fields = [
                'gender', 'case_type', 'military_serveice', 'pension_status',
                'housing_status', 'education', 'insurance', 
                'residencial_area', 'marrige_status', 'birth_date_from', 'birth_date_to',
                'disability_type', 'disability_level', 'reasons', 'recovered_reasons'
            ]

            for field in filter_fields:
                print(field)
                if data.get(field):
                    if field == 'disability_type':
                        queryset = queryset.filter(disabilities__disability_type__in=data[field])
                    elif field == 'disability_level':
                        queryset = queryset.filter(disabilities__disability_level__in=data[field])

                    elif field == 'birth_date_from' or field == 'birth_date_to':
                        if not data['birth_date_from']:
                            queryset = queryset.filter(date_of_birth__lte=data['birth_date_to'])
                        elif not data['birth_date_to']:
                            queryset = queryset.filter(date_of_birth__gte=data['birth_date_from'])
                        else:
                            queryset = queryset.filter(date_of_birth__gte=data['birth_date_from'], date_of_birth__lte=data['birth_date_to'])
                    elif field == 'reasons':
                        queryset = queryset.filter(reasons__reason__in=data[field])
                    elif field == 'recovered_reasons':
                        queryset = queryset.filter(recovered_reasons__reason__in=data[field])
                    else:
                        lookup = f"{field}__in"
                        queryset = queryset.filter(**{lookup: data[field]})


    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "گزارش پرونده ها"
    ws.sheet_view.rightToLeft = True # Set sheet direction for Persian

    headers = [
        'نام', 'نام خانوادگی', 'کد ملی', 'جنسیت','تاریخ تولد', 'نوع پرونده', 
        'شماره تماس', 'تحصیلات', 'وضعیت مسکن', 'بیمه', 'وضعیت تاهل'
    ]
    ws.append(headers)

    for case in queryset.distinct():
        disabilty_types = '// '.join([f'{d.get_disability_type_display()}-{d.get_disability_level_display()}' for d in case.disabilities.all()])
        reasons = ', '.join([r.get_reason_display() for r in case.reasons.all()])
        recovered_reasons = ', '.join([rr.get_reason_display() for rr in case.recovered_reasons.all()])
        row = [
            case.first_name,
            case.last_name,
            case.national_id,
            case.get_gender_display(),          
            case.date_of_birth.strftime('%Y/%m/%d') if case.date_of_birth else '',
            case.get_case_type_display(),
            case.phone_number,
            case.get_education_display(),
            case.get_housing_status_display(),
            case.get_insurance_display(),
            case.get_marrige_status_display(),
            disabilty_types,
            reasons,
            recovered_reasons,
        ]
        ws.append(row)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="cases_report.xlsx"'
    
    wb.save(response)
    return response




class ExpiredVisitsView(LoginRequiredMixin, ListView):
    model = Case
    template_name = 'reports/expired_visits.html'
    context_object_name = 'expired_cases'

    def get_queryset(self):
        today = datetime.date.today()
        threshold_date = today - timedelta(days=180)

        queryset = Case.objects.annotate(
            last_visit_date=Max('visits__visit_date')
        ).filter(
            last_visit_date__lt=threshold_date  # Filter: Date is older than 6 months ago
        ).order_by('-last_visit_date') 

        results = []
        for case in queryset:
            if case.last_visit_date:
                if isinstance(case.last_visit_date, jdatetime.date):
                    greg_last_visit = case.last_visit_date.togregorian()
                else:
                    greg_last_visit = case.last_visit_date

                greg_due_date = greg_last_visit + timedelta(days=180)
                overdue_days = (today - greg_due_date).days

                case.display_last_visit = case.last_visit_date 
                case.display_due_date = jdatetime.date.fromgregorian(date=greg_due_date)
                case.overdue_days = overdue_days
                
                results.append(case)
        
        return results



class ExpiredCommissionsView(LoginRequiredMixin, ListView):
    model = CaseDocuments
    template_name = 'reports/expired_commissions.html'
    context_object_name = 'expired_docs'

    def get_queryset(self):
        today = datetime.date.today()
        
        documents = CaseDocuments.objects.filter(
            doc_type='commition',
            date__isnull=False,
            expiry_diuration__isnull=False
        ).select_related('case')

        expired_list = []

        for doc in documents:
            if isinstance(doc.date, jdatetime.date):
                start_date_greg = doc.date.togregorian()
            else:
                start_date_greg = doc.date
            duration_days = int(doc.expiry_diuration * 365)
            expiry_date_greg = start_date_greg + timedelta(days=duration_days)

            if today > expiry_date_greg:
                days_passed = (today - expiry_date_greg).days
                
                doc.days_passed = days_passed
                doc.calculated_expiry_date = jdatetime.date.fromgregorian(date=expiry_date_greg)
                
                expired_list.append(doc)

        return sorted(expired_list, key=lambda x: x.days_passed, reverse=False)



class ExpiredDisabilityCardsView(LoginRequiredMixin, ListView):
    model = Case
    template_name = 'reports/expired_disability_cards.html'
    context_object_name = 'expired_cases'

    def get_queryset(self):
        today = datetime.date.today()

        queryset = Case.objects.annotate(
            last_card_expiry=Max(
                'casedocuments__expiry_date', 
                filter=Q(casedocuments__doc_type='disabiliti_card')
            )
        ).filter(
            last_card_expiry__lt=today,     
            last_card_expiry__isnull=False 
        ).order_by('last_card_expiry')      

        results = []
        for case in queryset:
            if isinstance(case.last_card_expiry, jdatetime.date):
                greg_expiry = case.last_card_expiry.togregorian()
            else:
                greg_expiry = case.last_card_expiry

            days_passed = (today - greg_expiry).days
            
            case.days_passed = days_passed
            results.append(case)
        
        return results



class AllDemandsListView(LoginRequiredMixin, ListView):
    model = Demands
    template_name = 'reports/all_demands.html'
    context_object_name = 'demands'
    paginate_by = 50  

    def get_queryset(self):
        return Demands.objects.select_related('case').order_by('-date', '-id')

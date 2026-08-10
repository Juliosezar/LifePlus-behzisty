import json
from django.views.generic import ListView, View
from cases.models import Case
from .forms import CaseReportForm
from django.contrib.auth.mixins import LoginRequiredMixin
import openpyxl
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Max
from datetime import timedelta
import datetime
import jdatetime
from cases.models import CaseDocuments
from cases.models import Demands
from django.db.models import Q
from .agent import generate_report, transcribe_audio




class CaseReportView(LoginRequiredMixin, ListView):
    model = Case
    template_name = 'reports/report.html'
    context_object_name = 'cases'

    def get_queryset(self):
        queryset = Case.objects.all().order_by('-created_at').prefetch_related('disabilities', 'reasons', 'recovered_reasons')

        archive_state = self.request.GET.get('archive', 'active')
        if archive_state == 'archived':
            queryset = queryset.filter(archive=True)
        elif archive_state == 'active':
            queryset = queryset.filter(archive=False)

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
    queryset = Case.objects.all().order_by('-created_at').prefetch_related(
        'reasons', 'disabilities', 'recovered_reasons', 'family',
        'visits', 'demands', 'services_provided'
    )

    archive_state = request.GET.get('archive', 'active')
    if archive_state == 'archived':
        queryset = queryset.filter(archive=True)
    elif archive_state == 'active':
        queryset = queryset.filter(archive=False)

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
        'نام', 'نام خانوادگی', 'کد ملی', 'جنسیت', 'وضعیت سربازی', 'شماره شناسنامه',
        'تاریخ تولد', 'محل تولد', 'تحصیلات', 'رشته تحصیلی', 'بیمه', 'شغل',
        'شماره تماس', 'تلفن ثابت', 'وضعیت مسکن', 'رهن', 'اجاره', 'منطقه مسکونی',
        'آدرس', 'کد پستی', 'متراژ آپارتمان', 'نوع ساختمان', 'تعداد اتاق',
        'وضعیت مستمری', 'نوع پرونده', 'شماره کارت', 'شماره حساب', 'شماره شبا',
        'وضعیت تاهل', 'تعداد برادران', 'تعداد خواهران', 'تعداد افراد تحت تکفل',
        'تعداد فرزندان', 'تاریخ ایجاد', 'تاریخ بروزرسانی',
        'پدر - نام', 'پدر - نام خانوادگی', 'پدر - کد ملی', 'پدر - تحصیلات', 'پدر - شغل',
        'مادر - نام', 'مادر - نام خانوادگی', 'مادر - کد ملی', 'مادر - تحصیلات', 'مادر - شغل',
        'اعضای خانواده',
        'تاریخ آخرین بازدید',
        'درخواست‌ها',
        'خدمات ارائه شده'
    ]
    ws.append(headers)

    for case in queryset.distinct():
        disabilty_types = '// '.join([f'{d.get_disability_type_display()}-{d.get_disability_level_display()}' for d in case.disabilities.all()])
        reasons = ', '.join([r.get_reason_display() for r in case.reasons.all()])
        recovered_reasons = ', '.join([rr.get_reason_display() for rr in case.recovered_reasons.all()])

        father = case.family.filter(relation='father').first()
        mother = case.family.filter(relation='mother').first()

        other_family = case.family.exclude(relation__in=['father', 'mother'])
        family_str = ', '.join([
            f'{f.get_relation_display()}:{f.first_name or ""} {f.last_name or ""}'
            for f in other_family
        ])

        last_visit = case.visits.order_by('-visit_date').first()
        last_visit_date = last_visit.visit_date.strftime('%Y/%m/%d') if last_visit and last_visit.visit_date else ''

        demands_str = ', '.join([d.request for d in case.demands.all()])
        services_str = ', '.join([s.service for s in case.services_provided.all()])

        row = [
            case.first_name,
            case.last_name,
            case.national_id,
            case.get_gender_display(),
            case.get_military_serveice_display() if case.military_serveice else '',
            case.birth_certificate_number or '',
            case.date_of_birth.strftime('%Y/%m/%d') if case.date_of_birth else '',
            case.birth_place or '',
            case.get_education_display(),
            case.field_of_study or '',
            case.get_insurance_display(),
            case.job or '',
            case.phone_number or '',
            case.home_phone_number or '',
            case.get_housing_status_display(),
            case.house_mortgage if case.house_mortgage is not None else '',
            case.house_rent if case.house_rent is not None else '',
            case.get_residencial_area_display() if case.residencial_area else '',
            case.address or '',
            case.postal_code or '',
            case.apartment_area if case.apartment_area is not None else '',
            case.get_building_type_display() if case.building_type else '',
            case.room_count if case.room_count is not None else '',
            case.get_pension_status_display() if case.pension_status else '',
            case.get_case_type_display(),
            case.bank_card_number or '',
            case.bank_account_number or '',
            case.bank_shaba_number or '',
            case.get_marrige_status_display(),
            case.brothers_count if case.brothers_count is not None else '',
            case.sisters_count if case.sisters_count is not None else '',
            case.dependents_count if case.dependents_count is not None else '',
            case.children_count if case.children_count is not None else '',
            case.created_at.strftime('%Y/%m/%d %H:%M') if case.created_at else '',
            case.updated_at.strftime('%Y/%m/%d %H:%M') if case.updated_at else '',
            father.first_name if father else '',
            father.last_name if father else '',
            father.national_id if father else '',
            father.get_education_display() if father and father.education else '',
            father.job if father else '',
            mother.first_name if mother else '',
            mother.last_name if mother else '',
            mother.national_id if mother else '',
            mother.get_education_display() if mother and mother.education else '',
            mother.job if mother else '',
            family_str,
            last_visit_date,
            demands_str,
            services_str,
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
            last_visit_date__lt=threshold_date,  # Filter: Date is older than 6 months ago
            archive=False
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
            expiry_diuration__isnull=False,
            case__archive=False
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
            last_card_expiry__isnull=False,
            archive=False
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


class GenerateReportView(LoginRequiredMixin, View):
    template_name = 'reports/generate_report.html'

    def _serialize_case(self, case):
        father = case.family.filter(relation='father').first()
        father_name = f"{father.first_name or ''}" if father else '-'

        disabilities = [
            {'type': d.get_disability_type_display(), 'level': d.get_disability_level_display()}
            for d in case.disabilities.all()
        ]

        family_members = []
        for m in case.family.all():
            family_members.append({
                'relation': m.get_relation_display(),
                'name': f"{m.first_name or ''} {m.last_name or ''}".strip() or '-',
                'education': m.get_education_display() if m.education else None,
                'job': m.job,
                'description': m.description,
            })

        return {
            'first_name': case.first_name,
            'last_name': case.last_name,
            'father_name': father_name,
            'national_id': case.national_id,
            'birth_certificate_number': case.birth_certificate_number or '-',
            'date_of_birth': str(case.date_of_birth) if case.date_of_birth else '-',
            'birth_place': case.birth_place or '-',
            'gender': case.get_gender_display(),
            'education': case.get_education_display() if case.education else '-',
            'field_of_study': case.field_of_study or '-',
            'marriage_status': case.get_marrige_status_display() if case.marrige_status else '-',
            'military_service': case.get_military_serveice_display() if case.military_serveice else '-',
            'job': case.job or '-',
            'phone_number': case.phone_number or '-',
            'home_phone_number': case.home_phone_number or '-',
            'case_type': case.get_case_type_display() if case.case_type else '-',
            'pension_status': case.get_pension_status_display() if case.pension_status else '-',
            'insurance': case.get_insurance_display() if case.insurance else '-',
            'housing_status': case.get_housing_status_display() if case.housing_status else '-',
            'house_mortgage': case.house_mortgage,
            'house_rent': case.house_rent,
            'residential_area': case.get_residencial_area_display() if case.residencial_area else '-',
            'address': case.address or '-',
            'apartment_area': case.apartment_area,
            'building_type': case.get_building_type_display() if case.building_type else '-',
            'room_count': case.room_count,
            'children_count': case.children_count,
            'dependents_count': case.dependents_count,
            'brothers_count': case.brothers_count,
            'sisters_count': case.sisters_count,
            'disabilities': disabilities,
            'reasons': [r.get_reason_display() for r in case.reasons.all()],
            'recovered_reasons': [
                f"{r.get_reason_display()} | مهارت: {r.skill or '-'} | سابقه: {r.work_experience or '-'}"
                for r in case.recovered_reasons.all()
            ],
            'family_members': family_members,
            'services_provided': [s.service for s in case.services_provided.all()],
            'demands': [d.request for d in case.demands.all()],
            'notes': [n.note for n in case.casenotes_set.all()],
        }

    def get(self, request, pk):
        case = get_object_or_404(
            Case.objects.prefetch_related(
                'disabilities', 'reasons', 'recovered_reasons',
                'family', 'services_provided', 'demands', 'casenotes_set', 'visits'
            ),
            pk=pk
        )
        return render(request, self.template_name, {'case': case})

    def post(self, request, pk):
        case = get_object_or_404(
            Case.objects.prefetch_related(
                'disabilities', 'reasons', 'recovered_reasons',
                'family', 'services_provided', 'demands', 'casenotes_set', 'visits'
            ),
            pk=pk
        )

        try:
            body = json.loads(request.body)
            user_input = body.get('extra_details', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not user_input:
            return JsonResponse({'error': 'لطفاً توضیحات را وارد کنید.'}, status=400)

        try:
            case_data = self._serialize_case(case)
            report_text = generate_report(case_data, user_input)
            return JsonResponse({'report': report_text})
        except Exception as e:
            return JsonResponse({'error': f'خطا در تولید گزارش: {str(e)}'}, status=500)


class TranscribeAudioView(LoginRequiredMixin, View):
    def post(self, request):
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return JsonResponse({'error': 'فایل صوتی ارسال نشده.'}, status=400)

        import tempfile, os
        suffix = '.webm'
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        try:
            for chunk in audio_file.chunks():
                tmp.write(chunk)
            tmp.close()

            text = transcribe_audio(tmp.name)
            return JsonResponse({'text': text})
        except Exception as e:
            return JsonResponse({'error': f'خطا در تبدیل صدا: {str(e)}'}, status=500)
        finally:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass

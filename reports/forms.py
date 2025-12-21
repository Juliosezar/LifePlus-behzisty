from django import forms
from cases.models import Case
from django_jalali.forms import jDateInput
import jdatetime
from cases.models import Disability, ReasonCase, RecoveredReasonCase

class CaseReportForm(forms.Form):
    gender = forms.MultipleChoiceField(
        choices=Case.GENDER_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="جنسیت"
    )
    case_type = forms.MultipleChoiceField(
        choices=Case.TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="نوع پرونده"
    )
    military_serveice = forms.MultipleChoiceField(
        choices=Case.MILITARY_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="وضعیت سربازی"
    )
    pension_status = forms.MultipleChoiceField(
        choices=Case.PENSION_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="وضعیت مستمری"
    )
    housing_status = forms.MultipleChoiceField(
        choices=Case.HOUSING_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="وضعیت مسکن"
    )
    education = forms.MultipleChoiceField(
        choices=Case.EDUCATION_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="تحصیلات"
    )
    insurance = forms.MultipleChoiceField(
        choices=Case.INSURANCE_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="بیمه"
    )
    residencial_area = forms.MultipleChoiceField(
        choices=Case.AREA_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="منطقه مسکونی"
    )
    marrige_status = forms.MultipleChoiceField(
        choices=Case.MARRIAGE_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="وضعیت تاهل"
    )
    birth_date_from = forms.CharField(
        widget=jDateInput(attrs={
            'placeholder': 'Click here', 
            'class': 'text-left', 
            'data-jdp': ''
        }),
        label='تاریخ تولد از',
        required=False
    )
    birth_date_to = forms.CharField(
        widget=jDateInput(attrs={
            'placeholder': 'Click here', 
            'class': 'text-left', 
            'data-jdp': ''
        }),
        label='تاریخ تولد تا',
        required=False
    )
    disability_type = forms.MultipleChoiceField(
        choices=Disability.DISABILY_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="نوع معلولیت"
    )
    disability_level = forms.MultipleChoiceField(
        choices=Disability.DISABILITY_LEVEL_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="شدت معلولیت"
    )
    reasons = forms.MultipleChoiceField(
        choices=ReasonCase.REASON_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="علت تشکیل پرونده"
    )
    recovered_reasons = forms.MultipleChoiceField(
        choices=RecoveredReasonCase.REASON_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="علت تشکیل پرونده (بهبود یافته)"
    )



    def clean_birth_date_from(self):
        return self._clean_jalali_date('birth_date_from')


    def clean_birth_date_to(self):
        return self._clean_jalali_date('birth_date_to')

    def _clean_jalali_date(self, field_name):
        """Helper to parse Jalali dates manually"""
        data = self.cleaned_data.get(field_name)
        
        if not data:
            return None

        trans_table = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
        data = data.translate(trans_table)

        try:
            if '/' in data:
                return jdatetime.datetime.strptime(data, '%Y/%m/%d').date()
            elif '-' in data:
                return jdatetime.datetime.strptime(data, '%Y-%m-%d').date()
            else:
                raise forms.ValidationError("فرمت تاریخ نامعتبر است. مثال: 1402/01/01")
        except ValueError:
            raise forms.ValidationError("تاریخ نامعتبر است.")

    def clean_date(self):
        return self._clean_jalali_date('date')

    def clean_expiry_date(self):
        return self._clean_jalali_date('expiry_date')

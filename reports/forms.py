from django import forms
from cases.models import Case


class CaseReportForm(forms.Form):
    # 1. Gender
    gender = forms.MultipleChoiceField(
        choices=Case.GENDER_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="جنسیت"
    )
    # 2. Case Type
    case_type = forms.MultipleChoiceField(
        choices=Case.TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="نوع پرونده"
    )
    # 3. Military (Note: keeping your spelling 'serveice')
    military_serveice = forms.MultipleChoiceField(
        choices=Case.MILITARY_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="وضعیت سربازی"
    )
    # 4. Pension
    pension_status = forms.MultipleChoiceField(
        choices=Case.PENSION_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="وضعیت مستمری"
    )
    # 5. Housing
    housing_status = forms.MultipleChoiceField(
        choices=Case.HOUSING_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="وضعیت مسکن"
    )
    # 6. Education
    education = forms.MultipleChoiceField(
        choices=Case.EDUCATION_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="تحصیلات"
    )
    # 7. Insurance
    insurance = forms.MultipleChoiceField(
        choices=Case.INSURANCE_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="بیمه"
    )
    # 8. Residential Area
    residencial_area = forms.MultipleChoiceField(
        choices=Case.AREA_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="منطقه مسکونی"
    )
    # 9. Marriage Status
    marrige_status = forms.MultipleChoiceField(
        choices=Case.MARRIAGE_CHOICES,
        widget=forms.CheckboxSelectMultiple, required=False, label="وضعیت تاهل"
    )

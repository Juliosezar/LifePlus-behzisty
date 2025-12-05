from django import forms
from django_jalali.forms import jDateInput
from .models import Case, Disability, CaseNotes, ReasonCase, CaseFamilyMembers, RecoveredReasonCase
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
import jdatetime  # Import this

class CaseForm(forms.ModelForm):
    # 1. Change this to CharField to bypass strict initial validation
    date_of_birth = forms.CharField(
        required=False,
        widget=jDateInput(attrs={
            'placeholder': '1370/01/01', 
            'class': 'text-left', 
            'data-jdp': ''
        }),
        label='تاریخ تولد'
    )

    class Meta:
        model = Case
        exclude = ['created_at', 'updated_at']
        
        widgets = {
            'gender': forms.Select(attrs={'class': 'cursor-pointer'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }
        
         
        error_messages = {
            'first_name': {
                'required': 'لطفا نام را وارد کنید.',
                'max_length': 'تعداد کاراکترها بیش از حد مجاز است.',
            },
            'last_name': {
                'required': 'لطفا نام خانوادگی را وارد کنید.',
                'max_length': 'تعداد کاراکترها بیش از حد مجاز است.',
            },
            'national_id': {
                'required': 'کد ملی الزامی است.',
                'unique': 'پرونده‌ای با این کد ملی قبلا ثبت شده است.',
                'invalid': 'کد ملی نامعتبر است.',
            },
            'gender': {
                'required': 'لطفا جنسیت را انتخاب کنید.',
            },
            'case_type': {
                'required': 'لطفا نوع پرونده را انتخاب کنید.',
            },

        }

    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)
        
        required_fields = ['first_name', 'last_name', 'national_id', 'gender', 'case_type']

        for field_name, field in self.fields.items():
            if field_name not in required_fields:
                field.required = False

            current_classes = field.widget.attrs.get('class', '')
            tailwind_class = f"w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-3 outline-none transition-all duration-200 {current_classes}"
            field.widget.attrs.update({'class': tailwind_class})

            field.error_messages.update({
                'required': 'پر کردن این فیلد الزامی است.',
                'invalid': 'مقدار وارد شده معتبر نیست.',
                'max_length': 'تعداد کاراکترها بیش از حد مجاز است.',
                'unique': 'پرونده‌ای با این کد ملی قبلا ثبت شده است.',

            })

    def clean_date_of_birth(self):
        data = self.cleaned_data.get('date_of_birth')
        if not data:
            return None
        trans_table = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
        data = data.translate(trans_table)
        try:
            if '/' in data:
                date_obj = jdatetime.datetime.strptime(data, '%Y/%m/%d').date()
            elif '-' in data:
                date_obj = jdatetime.datetime.strptime(data, '%Y-%m-%d').date()
            else:
                raise forms.ValidationError("فرمت تاریخ نامعتبر است")
            return date_obj
        except ValueError:
            raise forms.ValidationError("فرمت تاریخ صحیح نیست. مثال: 1400/01/01")

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 2:
            raise ValidationError("طول مقدار نام و نام خانوادگی باید بیشتر از 2 کاراکتر باشد.")
        for i in first_name:
            if i.isdigit():
                raise ValidationError("نام و نام خانوادگی نمیتواند حاوی عدد باشد.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) < 2:
            raise ValidationError("طول مقدار نام و نام خانوادگی باید بیشتر از 2 کاراکتر باشد.")
        for i in last_name:
            if i.isdigit():
                raise ValidationError("نام و نام خانوادگی نمیتواند حاوی عدد باشد.")
        return last_name

    def birth_certificate_number(self):
        birth_certificate_number = self.cleaned_data['birth_certificate_number']
        if len(birth_certificate_number) != 0:
            for i in birth_certificate_number:
                if not i.isdigit():
                    raise ValidationError("شناسنامه نمیتواند حاوی حروف باشد")
        return birth_certificate_number


    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if national_id is None :
            raise ValidationError("کدملی نمیتواند خالی باشد.")
        for i in national_id:
            if not i.isdigit():
                raise ValidationError("کدملی نمیتواند حاوی حروف باشد")
        if (len(national_id) != 10) and (len(national_id) != 12):
            raise ValidationError("مقدار کدملی باید 10 یا 12 (متولد افغانستان) باشد.")
        if len(national_id) == 10:
            if not check_national_id(national_id):
                raise ValidationError("کد ملی اشتباه است.")
        return national_id

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if phone_number is not None and len(phone_number) != 0:
            for i in phone_number:
                if not i.isdigit():
                    raise ValidationError("شماره موبایل نمیتواند حاوی حروف باشد.")
            if len(phone_number) != 11:
                raise ValidationError("شماره موبایل باید 11 رقمی باشد.")
        return phone_number

    def clean_home_phone_number(self):
        home_phone_number = self.cleaned_data['home_phone_number']
        if home_phone_number is not None and  len(home_phone_number) != 0:
            for i in home_phone_number:
                if not i.isdigit():
                    raise ValidationError("شماره منزل نمیتواند حاوی حروف باشد.")
            if (len(home_phone_number) != 11) and (len(home_phone_number) != 8):
                raise ValidationError("شماره منزل باید 8 یا 11 رقمی باشد.")
        return home_phone_number

    def clean_bank_card_number(self):
        bank_card_number = self.cleaned_data['bank_card_number']
        if bank_card_number is not None and len(bank_card_number) != 0:
            for i in bank_card_number:
                if not i.isdigit():
                    raise ValidationError("اطلاعات بانکی نمیتوانند حاوی حروف باشند.")
            if len(bank_card_number) != 16:
                raise ValidationError("شماره کارت اشتباه است. (باید 16 رقم باشد.)")
        return bank_card_number

    def clean_bank_account_number(self):
        bank_account_number = self.cleaned_data['bank_account_number']
        if bank_account_number is not None and len(bank_account_number) != 0:
            for i in bank_account_number:
                if not i.isdigit():
                    raise ValidationError("اطلاعات بانکی نمیتوانند حاوی حروف باشند.")
        return bank_account_number

    def clean_bank_shaba_number(self):
        bank_shaba_number = self.cleaned_data['bank_shaba_number']
        if bank_shaba_number is not None and len(bank_shaba_number) != 0:
            for i in bank_shaba_number:
                if not i.isdigit():
                    raise ValidationError("اطلاعات بانکی نمیتوانند حاوی حروف باشند.")
            if len(bank_shaba_number) != 24:
                raise ValidationError("شماره شبا اشتباه است.(باید 24 رقم باشد.)")
        return bank_shaba_number

def check_national_id(national_id):
    control_num = int(national_id[9:])
    num = national_id
    num9dig = num[:9]
    sum1 = 0
    count_num = 10
    for i in num9dig:
        i = int(i)
        sum1 += (i * count_num)
        count_num -= 1
    result = sum1 % 11
    if result < 2:
        return result == control_num
    else:
        return control_num == (11 - result)



class DisabilityForm(forms.ModelForm):
    class Meta:
        model = Disability
        fields = ['disability_type', 'disability_level']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-3'
            })

# 3. Create the Formset
CaseDisabilityFormSet = inlineformset_factory(
    Case, 
    Disability, 
    form=DisabilityForm,
    extra=1,       # Start with 1 empty row
    can_delete=True # Allow deleting rows
)


class CaseNotesForm(forms.ModelForm):
    class Meta:
        model = CaseNotes
        fields = ['note'] # We exclude 'added_by' here
        widgets = {
             'note': forms.Textarea(attrs={'rows': 2, 'placeholder': 'توضیحات تکمیلی یا مشاهدات...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-3'
            })

# 2. Create the Formset
CaseNotesFormSet = inlineformset_factory(
    Case, 
    CaseNotes, 
    form=CaseNotesForm,
    extra=1,       
    can_delete=True
)


# 1. Create the Reason Form
class ReasonCaseForm(forms.ModelForm):
    class Meta:
        model = ReasonCase
        fields = ['reason']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-3'
            })

# 2. Create the Formset
ReasonCaseFormSet = inlineformset_factory(
    Case, 
    ReasonCase, 
    form=ReasonCaseForm,
    extra=1,
    can_delete=True
)


# 1. Family Member Form
class CaseFamilyMemberForm(forms.ModelForm):
    class Meta:
        model = CaseFamilyMembers
        fields = ['relation', 'first_name', 'last_name', 'national_id', 'education', 'job', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1, 'placeholder': 'توضیحات...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-3'
            })


    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if national_id is not None:
            for i in national_id:
                if not i.isdigit():
                    raise ValidationError("کدملی نمیتواند حاوی حروف باشد")
            if (len(national_id) != 10) and (len(national_id) != 12):
                raise ValidationError("مقدار کدملی باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(national_id) == 10:
                if not check_national_id(national_id):
                    raise ValidationError("کد ملی اشتباه است.")
        return national_id

# 2. Family Formset
CaseFamilyMemberFormSet = inlineformset_factory(
    Case,
    CaseFamilyMembers,
    form=CaseFamilyMemberForm,
    extra=2, # We want exactly 2 forms (Father/Mother) initially
    can_delete=True
)

# 1. Create Form for Recovered Case
class RecoveredReasonCaseForm(forms.ModelForm):
    class Meta:
        model = RecoveredReasonCase
        fields = ['reason', 'skill', 'work_experience', 'insurance_type']
        widgets = {
            'skill': forms.TextInput(attrs={'placeholder': 'مثال: خیاطی، مکانیکی...'}),
            'work_experience': forms.TextInput(attrs={'placeholder': 'مدت زمان سابقه کار...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-3'
            })

# 2. Create Formset
RecoveredReasonCaseFormSet = inlineformset_factory(
    Case,
    RecoveredReasonCase,
    form=RecoveredReasonCaseForm,
    extra=1,
    can_delete=True
)














from django import forms
from django_jalali.forms import jDateInput
from .models import CaseDocuments

from django import forms
from django_jalali.forms import jDateInput
from .models import Case, CaseDocuments
import jdatetime # Make sure this is imported

class CaseDocumentForm(forms.ModelForm):
    # 1. Override fields to CharField to accept the raw string from picker
    date = forms.CharField(
        required=False,
        widget=jDateInput(attrs={
            'class': 'text-left', 
            'placeholder': '1402/01/01', 
            'data-jdp': ''
        }),
        label='تاریخ برگزاری کمیسیون'
    )
    
    expiry_date = forms.CharField(
        required=False,
        widget=jDateInput(attrs={
            'class': 'text-left', 
            'placeholder': '1405/01/01', 
            'data-jdp': ''
        }),
        label='تاریخ انقضا (کارت معلولیت)'
    )

    class Meta:
        model = CaseDocuments
        fields = ['doc_type', 'picture', 'date', 'expiry_diuration', 'expiry_date']
        
        widgets = {
            'doc_type': forms.Select(attrs={'class': 'cursor-pointer'}),
            'expiry_diuration': forms.Select(attrs={'class': 'cursor-pointer'}),
        }
        
        labels = {
            'doc_type': 'نوع مدرک',
            'picture': 'تصویر مدرک',
            'expiry_diuration': 'مدت اعتبار (کمیسیون)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Apply Tailwind styles
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-3"

    # --- MANUAL DATE CLEANING LOGIC ---

    def _clean_jalali_date(self, field_name):
        """Helper to parse Jalali dates manually"""
        data = self.cleaned_data.get(field_name)
        
        if not data:
            return None

        # 1. Convert Persian digits to English (e.g. ۱۴۰۲ -> 1402)
        trans_table = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
        data = data.translate(trans_table)

        # 2. Parse the string
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

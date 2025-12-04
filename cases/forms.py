from django import forms
from django_jalali.forms import jDateInput
from .models import Case
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
        
        # Keep your labels exactly as they were
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'national_id': 'کد ملی',
            'birth_certificate_number': 'شماره شناسنامه',
            'date_of_birth': 'تاریخ تولد',
            'birth_place': 'محل تولد',
            'gender': 'جنسیت',
            'education': 'تحصیلات',
            'field_of_study': 'رشته تحصیلی',
            'insurance': 'وضعیت بیمه',
            'job': 'شغل',
            'phone_number': 'شماره همراه',
            'home_phone_number': 'تلفن ثابت',
            'housing_status': 'وضعیت مسکن',
            'residencial_area': 'منطقه مسکونی',
            'address': 'آدرس کامل',
            'pension_status': 'وضعیت مستمری',
            'case_type': 'نوع پرونده',
            'bank_card_number': 'شماره کارت',
            'bank_account_number': 'شماره حساب',
            'bank_shaba_number': 'شماره شبا',
            'marrige_status': 'وضعیت تاهل',
            'brothers_count': 'تعداد برادران',
            'sisters_count': 'تعداد خواهران',
            'dependents_count': 'تعداد افراد تحت تکفل',
            'children_count': 'تعداد فرزندان',
        }

    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)
        
        required_fields = ['first_name', 'last_name', 'national_id', 'gender']

        for field_name, field in self.fields.items():
            if field_name not in required_fields:
                field.required = False

            current_classes = field.widget.attrs.get('class', '')
            tailwind_class = f"w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-3 outline-none transition-all duration-200 {current_classes}"
            field.widget.attrs.update({'class': tailwind_class})

    # --- THE FIX IS HERE ---
    def clean_date_of_birth(self):
        data = self.cleaned_data.get('date_of_birth')
        
        if not data:
            return None

        # 1. Convert Persian digits to English (e.g. ۱۴۰۲ -> 1402)
        trans_table = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
        data = data.translate(trans_table)

        # 2. Parse the string manually
        try:
            # Attempt to convert "1402/09/12" to a real date object
            if '/' in data:
                date_obj = jdatetime.datetime.strptime(data, '%Y/%m/%d').date()
            elif '-' in data:
                date_obj = jdatetime.datetime.strptime(data, '%Y-%m-%d').date()
            else:
                raise forms.ValidationError("فرمت تاریخ نامعتبر است")
            
            return date_obj
            
        except ValueError:
            raise forms.ValidationError("فرمت تاریخ صحیح نیست. مثال: 1400/01/01")

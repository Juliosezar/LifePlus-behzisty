from django.db import models
from django_jalali.db import models as jmodels
from uuid import uuid4
import os
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class Case(models.Model):
    # --- Choices Definitions ---

    EDUCATION_CHOICES = (
        ('illiterate', 'بی سواد'),
        ('elementary', 'ابتدایی'),
        ('middle_school', 'متوسطه اول (سیکل)'),
        ('high_school', 'متوسطه دوم (دیپلم)'),
        ('associate', 'کاردانی (فوق دیپلم)'),
        ('bachelor', 'کارشناسی (لیسانس)'),
        ('master', 'کارشناسی ارشد (فوق لیسانس)'),
        ('phd', 'دکترا'),
        ('post_doc', 'فوق دکترا'),
    )

    HOUSING_CHOICES = (
        ('rental', 'استیجاری'),
        ('paternal', 'پدری'),
        ('relatives', 'منزل بستگان'),
        ('endowment', 'مسکن وقفی'),
        ('owned', 'مسکن شخصی'),
        ('homeless', 'بی خانمان'),
        ('inherited', 'ورثه ای'),
        ('org_housing', 'منازل سازمانی'),
        ('care_center', 'مرکز نگهداری'),
    )

    AREA_CHOICES = (
        ('industrial_city', 'شهر صنعتی'),
        ('railway', 'راه آهن'),
        ('gerdo_town', 'شهرک گردو'),
        ('shariati', 'شریعتی'),
        ('maskan', 'مسکن'),
        ('alamolhoda', 'علم الهدی'),
        ('rodaki', 'رودکی'),
        ('khorram', 'خرم'),
        ('hossein_abad', 'حسین آباد'),
        ('nazm_abad', 'نظم آباد'),
        ('karahroud', 'کرهرود'),
        ('jahan_panah', 'جهان پناه'),
        ('malek', 'ملک'),
        ('abbas_abad', 'عباس آباد'),
        ('valiasr_town', 'شهرک ولی عصر'),
        ('robat_mil', 'رباط میل'),
        ('ban', 'بان'),
        ('jahangiri', 'جهانگیری'),
    )

    PENSION_CHOICES = (
        ('continuous', 'مستمر'),
        ('non_continuous', 'غیرمستمر'),
    )

    TYPE_CHOICES = (
        ('rehab', 'توانبخشی'),
        ('social', 'اجتماعی'),
        ('recovered', 'بهبود یافته'),
    )

    GENDER_CHOICES = (
        ('M', 'مرد'), 
        ('F', 'زن'), 
        ('O', 'سایر')
    )

    # 2. Marriage Status Choices (From your image)
    MARRIAGE_CHOICES = (
        ('married', 'متاهل'),
        ('divorced', 'مطلقه'),
        ('separated', 'متارکه'),
        ('single', 'مجرد'),
        ('widowed', 'همسر فوت شده'),
    )
    INSURANCE_CHOICES = (
        ('none', 'ندارد'),
        ('social_security', 'تامین اجتماعی'),
        ('welfare', 'بهزیستی'),
        ('carpet_weaving', 'قالی بافی'),
        ('self_employed', 'خویش فرمایی'),
        ('life', 'عمر'),
        ('employer', 'کارفرمایی'),
        ('labor', 'کارگری'),
        ('medical_services', 'خدمات درمانی'),
        ('housewives', 'زنان خانه دار'),
        ('rural', 'روستاییان'),
        ('iranian_health', 'سلامت ایرانیان'),
        ('universal_health', 'سلامت همگانی'),
        ('gov_employees', 'سلامت - کارکنان دولت'),
        ('other_sectors', 'سلامت - سایر اقشار'),
        ('armed_forces', 'نیروهای مسلح'),
        ('special_patients', 'بیماران خاص'),
    )
    # 3. Count Choices (0 to 10)
    # Creates a list like [(0, '0'), (1, '1'), ... (10, '10')]
    COUNT_CHOICES = [(i, str(i)) for i in range(11)]

    # --- Fields ---

    # REQUIRED FIELDS (No blank=True)
    first_name = models.CharField(max_length=30, verbose_name="نام")
    last_name = models.CharField(max_length=30, verbose_name="نام خانوادگی")
    national_id = models.CharField(max_length=30, unique=True, verbose_name="کد ملی")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="جنسیت")

    # OPTIONAL FIELDS (blank=True, null=True)
    birth_certificate_number = models.CharField(max_length=30, verbose_name="شماره شناسنامه", blank=True, null=True)
    date_of_birth = jmodels.jDateField(verbose_name="تاریخ تولد", blank=True, null=True)
    birth_place = models.CharField(max_length=30, verbose_name="محل تولد", blank=True, null=True)
    
    education = models.CharField(max_length=30, choices=EDUCATION_CHOICES, verbose_name="تحصیلات", blank=True, null=True)
    field_of_study = models.CharField(max_length=30, verbose_name="رشته تحصیلی", blank=True, null=True)
    insurance = models.CharField(max_length=30, choices=INSURANCE_CHOICES, verbose_name="وضعیت بیمه", blank=True, null=True)
    job = models.CharField(max_length=30, verbose_name="شغل", blank=True, null=True)

    phone_number = models.CharField(max_length=30, verbose_name="شماره همراه", blank=True, null=True)
    home_phone_number = models.CharField(max_length=30, verbose_name="تلفن ثابت", blank=True, null=True)
    
    housing_status = models.CharField(max_length=30, choices=HOUSING_CHOICES, verbose_name="وضعیت مسکن", blank=True, null=True)
    residencial_area = models.CharField(max_length=30, choices=AREA_CHOICES, verbose_name="منطقه مسکونی", blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name="آدرس", blank=True, null=True)
    
    pension_status = models.CharField(max_length=30, choices=PENSION_CHOICES, verbose_name="وضعیت مستمری", blank=True, null=True)
    case_type = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name="نوع پرونده", blank=True, null=True)
    
    bank_card_number = models.CharField(max_length=30, verbose_name="شماره کارت", blank=True, null=True)
    bank_account_number = models.CharField(max_length=30, verbose_name="شماره حساب", blank=True, null=True)
    bank_shaba_number = models.CharField(max_length=30, verbose_name="شماره شبا", blank=True, null=True)
    
    # Updated Marriage Field
    marrige_status = models.CharField(max_length=30, choices=MARRIAGE_CHOICES, verbose_name="وضعیت تاهل", blank=True, null=True)
    
    # Updated Count Fields (Choice 0-10)
    brothers_count = models.IntegerField(choices=COUNT_CHOICES, verbose_name="تعداد برادران", blank=True, null=True)
    sisters_count = models.IntegerField(choices=COUNT_CHOICES, verbose_name="تعداد خواهران", blank=True, null=True)
    dependents_count = models.IntegerField(choices=COUNT_CHOICES, verbose_name="تعداد افراد تحت تکفل", blank=True, null=True)
    children_count = models.IntegerField(choices=COUNT_CHOICES, verbose_name="تعداد فرزندان", blank=True, null=True)

    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.national_id}"

class CaseFamilyMembers(models.Model):
    relation = models.CharField(max_length=30)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    national_id = models.CharField(max_length=30)
    education = models.CharField(max_length=30)
    job = models.CharField(max_length=30)
    description = models.CharField(max_length=500)



class CaseNotes(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    note = models.CharField(max_length=500)
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)




def get_file_path(instance, filename):
    """Generate a unique file name with the given prefix."""
    ext = os.path.splitext(filename)[1]
    return os.path.join("pics", f"{uuid4().hex}{ext}")

class CaseDocuments(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_file_path, null=False, blank=False)
    doc_type = models.CharField(max_length=30)
    date = jmodels.jDateField()
    expiry_date = jmodels.jDateField()
    expiry_diuration = models.CharField(max_length=30)



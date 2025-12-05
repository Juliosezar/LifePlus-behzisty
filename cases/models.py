from django.db import models
from django_jalali.db import models as jmodels
from uuid import uuid4
import os
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from .utils import AwsHandler


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
    MILITARY_CHOICES = (
        ('absence', 'غیبت'),
        ('exempt', 'معافیت'),
        ('passed', 'گذرانده'),
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
    military_serveice = models.CharField(max_length=30, choices=MILITARY_CHOICES, verbose_name="وضعیت سربازی", blank=True, null=True)

    # OPTIONAL FIELDS (blank=True, null=True)
    birth_certificate_number = models.CharField(max_length=30, verbose_name="شماره شناسنامه", blank=True, null=True)
    date_of_birth = jmodels.jDateField(verbose_name="تاریخ تولد", blank=True, null=True)
    birth_place = models.CharField(max_length=30, verbose_name="محل تولد", blank=True, null=True)
    
    education = models.CharField(max_length=30, choices=EDUCATION_CHOICES, verbose_name="تحصیلات", blank=True, null=True)
    field_of_study = models.CharField(max_length=50, verbose_name="رشته تحصیلی", blank=True, null=True)
    insurance = models.CharField(max_length=50, choices=INSURANCE_CHOICES, verbose_name="وضعیت بیمه", blank=True, null=True)
    job = models.CharField(max_length=100, verbose_name="شغل", blank=True, null=True)

    phone_number = models.CharField(max_length=30, verbose_name="شماره همراه", blank=True, null=True)
    home_phone_number = models.CharField(max_length=30, verbose_name="تلفن ثابت", blank=True, null=True)
    
    housing_status = models.CharField(max_length=30, choices=HOUSING_CHOICES, verbose_name="وضعیت مسکن", blank=True, null=True)
    house_mortgage = models.IntegerField(verbose_name="رهن", blank=True, null=True)
    house_rent = models.FloatField(verbose_name="اجاره", blank=True, null=True)
    residencial_area = models.CharField(max_length=30, choices=AREA_CHOICES, verbose_name="منطقه مسکونی", blank=True, null=True)
    address = models.CharField(max_length=400, verbose_name="آدرس", blank=True, null=True)
    
    pension_status = models.CharField(max_length=30, choices=PENSION_CHOICES, verbose_name="وضعیت مستمری", blank=True, null=True)
    case_type = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name="نوع پرونده", blank=True, null=True)
    
    bank_card_number = models.CharField(max_length=30, verbose_name="شماره کارت", blank=True, null=True)
    bank_account_number = models.CharField(max_length=30, verbose_name="شماره حساب", blank=True, null=True)
    bank_shaba_number = models.CharField(max_length=30, verbose_name="شماره شبا", blank=True, null=True)
    marrige_status = models.CharField(max_length=30, choices=MARRIAGE_CHOICES, verbose_name="وضعیت تاهل", blank=True, null=True)
    brothers_count = models.IntegerField(choices=COUNT_CHOICES, verbose_name="تعداد برادران", blank=True, null=True)
    sisters_count = models.IntegerField(choices=COUNT_CHOICES, verbose_name="تعداد خواهران", blank=True, null=True)
    dependents_count = models.IntegerField(choices=COUNT_CHOICES, verbose_name="تعداد افراد تحت تکفل", blank=True, null=True)
    children_count = models.IntegerField(choices=COUNT_CHOICES, verbose_name="تعداد فرزندان", blank=True, null=True)

    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.national_id}"

class CaseFamilyMembers(models.Model):
    RELATION_CHOICES = (
        ('father', 'پدر'),
        ('mother', 'مادر'),
        ('brother', 'برادر'),
        ('sister', 'خواهر'),
        ('son', 'پسر'),
        ('daughter', 'دختر'),
        ('husband', 'شوهر'),
        ('wife', 'زن'),
    )
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
    # I added related_name='family' for easier access
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='family')
    relation = models.CharField(max_length=30, choices=RELATION_CHOICES, verbose_name="نسبت")
    first_name = models.CharField(max_length=30, verbose_name="نام", blank=True, null=True)
    last_name = models.CharField(max_length=30, verbose_name="نام خانوادگی", blank=True, null=True)
    national_id = models.CharField(max_length=30, verbose_name="کد ملی", blank=True, null=True)
    education = models.CharField(choices=EDUCATION_CHOICES, max_length=30, verbose_name="تحصیلات", blank=True, null=True)
    job = models.CharField(max_length=50, verbose_name="شغل", blank=True, null=True)
    description = models.CharField(max_length=500, verbose_name="توضیحات", blank=True, null=True)


class CaseNotes(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    note = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)


class Disability(models.Model):
    DISABILY_TYPE_CHOICES = (
        ('body_movment', 'جسمی حرکتی'),
        ('body_movment_ms', 'جسمی حرکتی(ام اس)'),
        ('nerves_psyche', 'اعصاب و روان'),
        ('hearing', 'شنوایی'),
        ('vision', 'بینایی'),
        ('mental', 'ذهنی'),
        ('spoken', 'گفتاری'),
        ('autism', 'اوتیسم'),
        ('spinal_cord', 'ضایعه نخاعی'),
        ('old_age', 'سالمندی'),
        ('alzheimer', 'آلزایمر'),
        ('dementia', 'دمانس'),
        ('no_disability', 'فاقد معلولیت'),
        ('no_document', 'فاقد مدارک لازم'),
    )
    DISABILITY_LEVEL_CHOICES = (
        ('level1', 'خفیف'),
        ('level2', 'متوسط'),
        ('level3', 'شدید'),
        ('level4', 'خیلی شدید'),
        ('none', 'ندارد'),
    )

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='disabilities')
    disability_type = models.CharField(max_length=30, verbose_name="نوع معلولیت", choices=DISABILY_TYPE_CHOICES)
    disability_level = models.CharField(max_length=30, verbose_name="شدت معلولیت", choices=DISABILITY_LEVEL_CHOICES)

class ReasonCase(models.Model):
    REASON_CHOICES = (
        ('man_cant_work', 'مرد از کار افتاده'),
        ('husbend_died', 'شوهر فوت شده'),
        ('divorce', 'طلاق گرفته'),
        ('self_governing_girl', 'دختر خود سرپرست'),
        ('bad_guardian_girl', 'دختر بد سرپرست'),
        ('leaved_partner', 'متارکه کرده'),
        ('no_family_child', 'کودک فاقد سرپرست'),
    )
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='reasons', verbose_name="علت تشکیل پرونده")
    reason = models.CharField(max_length=500, null=True, blank=True, choices=REASON_CHOICES)

class RecoveredReasonCase(models.Model):
    REASON_CHOICES = (
        ('employment_loan', 'وام اشتغال'),
        ('insurance_right', 'حق بیمه'),
        ('cost_reduction', 'کاهش هزینه انشعابات'),
    )
    INSURANCE_TYPE_CHOICES = (
        ('self', 'خویش فرمایی'),
        ('employes', 'کارفرمایی'),
    )
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='recovered_reasons', verbose_name="علت تشکیل پرونده (بهبود یافته)")
    reason = models.CharField(max_length=500, null=True, blank=True, choices=REASON_CHOICES)
    skill = models.CharField(max_length=500, null=True, blank=True)
    work_experience = models.CharField(max_length=500, null=True, blank=True)
    insurance_type = models.CharField(max_length=500, null=True, blank=True, choices=INSURANCE_TYPE_CHOICES)


def get_file_path(instance, filename):
    """Generate a unique file name with the given prefix."""
    ext = os.path.splitext(filename)[1]
    return os.path.join("pics", f"{uuid4().hex}{ext.lower()}")

class CaseDocuments(models.Model):
    DOC_TYPE_CHOICES = (
        ('commition', 'کمیسیون'),
        ('needs_form', 'تعیین نیاز'),
        ('birt_certificat', 'شناسنامه'),
        ('disabiliti_card', 'کارت معلولیت'),
        ('national_id', 'کارت ملی'),
        ('bank', 'مدارک بانکی'),
        ('military_serveice', 'کارت پایان خدمت'),
        ('pic3x4', 'عکس 3x4'),
        ('rehab_tools', 'لوازم توانبخشی'),
        ('military_exemtion', 'کارت معافیت از خدمت'),
        ('foreign_national_id', 'کارت اقامت اتباع خارجی'),
        ('insurance', 'بیمه'),
        ('divorce_id', 'طلاق نامه'),
        ('death_certificate', 'گواهی فوت'),
        ('children_docs', 'مدارک فرزندان'),
        ('skill_certificate', 'گواهی مهارت'),
        ('other', 'متفرقه')
    )
    EXPIRY_DIURATION = (
        (5, '5 سال بعد'),
        (10, '10 سال بعد'),
        (1, '1 سال بعد'),
        (2, '2 سال بعد'),
        (3, '3 سال بعد'),
        (4, '4 سال بعد'),
        (6, '6 سال بعد'),
        (7, '7 سال بعد'),
        (8, '8 سال بعد'),
        (9, '9 سال بعد'),
        (0.5, '6 ماه بعد'),
    )
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_file_path)
    doc_type = models.CharField(max_length=30, choices=DOC_TYPE_CHOICES)
    date = jmodels.jDateField(null=True, blank=True)
    expiry_date = jmodels.jDateField(null=True, blank=True)
    expiry_diuration = models.FloatField( null=True, blank=True, choices=EXPIRY_DIURATION)

    @property
    def signed_url(self):
        if self.picture:
            # self.picture.name returns the path stored in DB (e.g., "pics/image.jpg")
            return AwsHandler.get_file_tmp_url(self.picture.name)
        return ""


class Visit(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='visits')
    visit_date = jmodels.jDateField()
    
    def __str__(self):
        return f"{self.case.first_name} {self.case.last_name} - {self.visit_date}"



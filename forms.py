# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from .models import People

my_default_errors = {
    'required': 'فیلد های نام و نام خانوادگی و کدملی و جنسیت اجباری هستند.',
    'invalid': 'ورودی شما نامعتبر است.'}

CHOICESsex = [("-----", "-----------"), ("مرد", "مرد"), ("زن", "زن")]
CHOICESmostamary = [("-----", "-----------"), ("مستمر", "مستمر"), ("غیرمستمر", "غیرمستمر")]
day = [("--", "روز")]
for i in range(1, 32):
    day.append((i, i))
month = [("--", "ماه")]
for i in range(1, 13):
    month.append((i, i))
year = [("----", "سال")]
for i in range(1300, 1420):
    year.append((i, i))

year3 = [("----", "سال")]
for i in range(1399, 1420):
    year3.append((i, i))

siblings_num = [("--", "---")]
for i in range(0, 10):
    siblings_num.append((i, i))
bime_type_ch = [("-----", "-----------"), ("خویش فرمایی", "خویش فرمایی"), ("کارفرمایی", "کارفرمایی")]

takafol_num_ch = [("---","---------") , (0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9)]

choises_tahsilat = [("-----", "-----------"), ("بی سواد", "بی سواد"), ("ابتدایی", "ابتدایی"),
                    ("متوسطه اول (سیکل)", "متوسطه اول (سیکل)"),
                    ("متوسطه دوم (دیپلم)", "متوسطه دوم (دیپلم)"), ("کاردانی (فوق دیپلم)", "کاردانی (فوق دیپلم)"),
                    ("کارشناسی (لیسانس)", "کارشناسی (لیسانس)"),
                    ("کارشناسی ارشد (فوق لیسانس)", "کارشناسی ارشد (فوق لیسانس)"), ("دکترا", "دکترا"),
                    ("فوق دکترا", "فوق دکترا")]

parvande_type_choose = [("-----", "-----------"), ("توانبخشی", "توانبخشی"), ("اجتماعی", "اجتماعی"),
                        ("بهبود یافته", "بهبود یافته")]

pt_ejtemaee_choice = [("-----", "-----------"), ("مرد از کار افتاده", "مرد از کار افتاده"),
                      ("شوهر فوت شده", "شوهر فوت شده"), ("طلاق گرفته", "طلاق گرفته"),
                      ("دختر خود سرپرست", "دختر خود سرپرست"), ("دختر بد سرپرست", "دختر بد سرپرست"),
                      ("متارکه کرده", "متارکه کرده"), ("کودک فاقد سرپرست", "کودک فاقد سرپرست")]

pt_behboodyafte_choice = [("-----", "-----------"), ("وام اشتغال", "وام اشتغال"), ("حق بیمه", "حق بیمه"),
                          ("کاهش هزینه انشعابات", "کاهش هزینه انشعابات")]

illness_choice = [("-----", "-----------"), ("جسمی حرکتی", "جسمی حرکتی"),
                  ("جسمی حرکتی(ام اس)", "جسمی حرکتی(ام اس)"), ("اعصاب و روان", "اعصاب و روان"),
                  ("شنوایی", "شنوایی"), ("بینایی", "بینایی"), ("ذهنی", "ذهنی"), ("گفتاری", "گفتاری"),
                  ("اوتیسم", "اوتیسم"), ("ضایعه نخاعی", "ضایعه نخاعی"), ("سالمندی", "سالمندی"),
                  ("آلزایمر", "آلزایمر"), ("دمانس", "دمانس"), ("فاقد معلولیت", "فاقد معلولیت"),
                  ("فاقد مدارک لازم", "فاقد مدارک لازم")]

level_choice = [("-----", "-----------"), ("خفیف", "خفیف"), ("متوسط", "متوسط"), ("شدید", "شدید"),
                ("خیلی شدید", "خیلی شدید"), ("ندارد", "ندارد")]

expirenum = [(0, 0), (100, "6ماه")]
for i in range(1, 11):
    expirenum.append((i, str(i) + " سال"))

residenty_area_choose = [("-----", "-----------"), ("شهر صنعتی", "شهر صنعتی"), ("راه آهن", "راه آهن"),
                         ("شهرک گردو", "شهرک گردو"),
                         ("شریعتی", "شریعتی"), ("مسکن", "مسکن"), ("علم الهدی", "علم الهدی"),
                         ("رودکی", "رودکی"), ("خرم", "خرم"), ("حسین آباد", "حسین آباد"), ("نظم آباد", "نظم آباد"),
                         ("کرهرود", "کرهرود"),
                         ("جهان پناه", "جهان پناه"), ("ملک", "ملک"), ("عباس آباد", "عباس آباد"),
                         ("شهرک ولی عصر", "شهرک ولی عصر"), ("رباط میل", "رباط میل"), ("بان", "بان"),
                         ("جهانگیری", "جهانگیری")]

taahol_choice = [("-----", "-----------"), ("متاهل", "متاهل"), ("مطلقه", "مطلقه"), ("متارکه", "متارکه"),
                 ("مجرد", "مجرد"), ("همسر فوت شده", "همسر فوت شده")]

choose_bime = [("-----", "-----------"), ("ندارد", "ندارد"), ("تامین اجتماعی", "تامین اجتماعی"), ("بهزیستی", "بهزیستی"),
               ("قالی بافی", "قالی بافی"),
               ("خویش فرمایی", "خویش فرمایی"), ("عمر", "عمر"),
               ("کارفرمایی", "کارفرمایی"), ("کارگری", "کارگری"),
               ("خدمات درمانی", "خدمات درمانی"), ("زنان خانه دار", "زنان خانه دار"),
               ("روستاییان", "روستاییان"), ("سلامت ایرانیان", "سلامت ایرانیان"), ("سلامت همگانی", "سلامت همگانی"),
               ("سلامت - کارکنان دولت", "سلامت - کارکنان دولت"), ("سلامت - سایر اقشار", "سلامت - سایر اقشار"),
               ("نیروهای مسلح", "نیروهای مسلح"), ("بیماران خاص", "بیماران خاص")]

sarbazi_choice = [("-----", "-----------"), ("معافیت", "معافیت"), ("گذرانده", "گذرانده"), ("غیبت", "غیبت")]

child_num_choice = [(-100, "-----------"), (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7)]

live_situation_choice = [("-----", "-----------"), ("استیجاری", "استیجاری"), ("پدری", "پدری"),
                         ("منزل بستگان", "منزل بستگان"), ("مسکن وقفی", "مسکن وقفی"),
                         ("مسکن شخصی", "مسکن شخصی"), ("بی خانمان", "بی خانمان"), ("ورثه ای", "ورثه ای"),
                         ("منازل سازمانی", "منازل سازمانی"), ("مرکز نگهداری", "مرکز نگهداری")]


def test_melly_code(num):
    num9dig = num[:9]
    sum1 = 0
    count_num = 10
    for i in num9dig:
        i = int(i)
        sum1 += (i * count_num)
        count_num -= 1
    return sum1 % 11


def send_test_melly_result(num):
    control_num = int(num[9:])
    result = test_melly_code(num)
    if result < 2:
        return result == control_num
    else:
        return control_num == (11 - result)


class CreatPersonForm(forms.Form):
    fname = forms.CharField(max_length=20, required=True, error_messages=my_default_errors)
    lname = forms.CharField(max_length=20, required=True, error_messages=my_default_errors)
    melly_code = forms.CharField(max_length=12, required=True)
    sex = forms.ChoiceField(required=True, choices=CHOICESsex)
    shenasnameh = forms.CharField(max_length=14, required=False)
    birthday_day = forms.ChoiceField(choices=day, required=False)
    birthday_month = forms.ChoiceField(choices=month, required=False)
    birthday_year = forms.ChoiceField(choices=year, required=False)
    birth_place = forms.CharField(max_length=50, required=False)
    tahsilat = forms.ChoiceField(required=False, choices=choises_tahsilat)
    reshteh_tahsili = forms.CharField(max_length=50, required=False)
    bime = forms.ChoiceField(choices=choose_bime, required=False)
    job = forms.CharField(max_length=70, required=False)
    sarbazi_status = forms.ChoiceField(choices=sarbazi_choice, required=False)
    parvande_type = forms.ChoiceField(choices=parvande_type_choose, required=False)
    pt_ejtemaee = forms.ChoiceField(choices=pt_ejtemaee_choice, required=False)
    pt_behboodyafte = forms.ChoiceField(choices=pt_behboodyafte_choice, required=False)
    mostamary_status = forms.ChoiceField(required=True, choices=CHOICESmostamary)
    maharat_behbod = forms.CharField(required=False, max_length=70)
    work_history = forms.CharField(required=False, max_length=20)
    bime_type = forms.ChoiceField(required=False, choices=bime_type_ch)
    taahol_status = forms.ChoiceField(choices=taahol_choice, required=False)
    illness1 = forms.ChoiceField(choices=illness_choice, required=False)
    level1 = forms.ChoiceField(choices=level_choice, required=False)
    illness2 = forms.ChoiceField(choices=illness_choice, required=False)
    level2 = forms.ChoiceField(choices=level_choice, required=False)
    illness3 = forms.ChoiceField(choices=illness_choice, required=False)
    level3 = forms.ChoiceField(choices=level_choice, required=False)
    illness4 = forms.ChoiceField(choices=illness_choice, required=False)
    level4 = forms.ChoiceField(choices=level_choice, required=False)
    address = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    residancy_area = forms.ChoiceField(choices=residenty_area_choose, required=False)
    phone_num = forms.CharField(max_length=11, required=False)
    home_num = forms.CharField(max_length=11, required=False)
    note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    father_name = forms.CharField(max_length=50, required=False)
    mother_fname = forms.CharField(max_length=50, required=False)
    mother_lname = forms.CharField(max_length=50, required=False)
    father_job = forms.CharField(max_length=50, required=False)
    mother_job = forms.CharField(max_length=50, required=False)
    father_degree = forms.ChoiceField(choices=choises_tahsilat, required=False)
    mother_degree = forms.ChoiceField(choices=choises_tahsilat, required=False)
    father_mellycode = forms.CharField(required=False)
    mother_mellycode = forms.CharField(required=False)

    brothers_num = forms.ChoiceField(choices=siblings_num, required=False)
    sisters_num = forms.ChoiceField(choices=siblings_num, required=False)
    takafol_num = forms.ChoiceField(choices=takafol_num_ch , required=False)
    live_situation = forms.ChoiceField(required=False, choices=live_situation_choice)
    rahn = forms.IntegerField(required=False, min_value=0)
    ejareh = forms.FloatField(required=False, min_value=0)

    card_num = forms.CharField(required=False)
    hesab_num = forms.CharField(required=False)
    shaba_num = forms.CharField(required=False)

    husbent_name = forms.CharField(required=False, max_length=50)
    husbent_codemelly = forms.CharField(required=False, max_length=50)
    husbent_job = forms.CharField(required=False, max_length=50)
    husbent_tahsilat = forms.ChoiceField(required=False, choices=choises_tahsilat)
    childs_number = forms.ChoiceField(choices=child_num_choice, required=False)
    child1_name = forms.CharField(max_length=60, required=False)
    child1_mellycode = forms.CharField(max_length=12, required=False)
    child1_tahsilat = forms.ChoiceField(choices=choises_tahsilat, required=False)
    child1_note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    child2_name = forms.CharField(max_length=60, required=False)
    child2_mellycode = forms.CharField(max_length=12, required=False)
    child2_tahsilat = forms.ChoiceField(choices=choises_tahsilat, required=False)
    child2_note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    child3_name = forms.CharField(max_length=60, required=False)
    child3_mellycode = forms.CharField(max_length=12, required=False)
    child3_tahsilat = forms.ChoiceField(choices=choises_tahsilat, required=False)
    child3_note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    child4_name = forms.CharField(max_length=60, required=False)
    child4_mellycode = forms.CharField(max_length=12, required=False)
    child4_tahsilat = forms.ChoiceField(choices=choises_tahsilat, required=False)
    child4_note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    child5_name = forms.CharField(max_length=60, required=False)
    child5_mellycode = forms.CharField(max_length=12, required=False)
    child5_tahsilat = forms.ChoiceField(choices=choises_tahsilat, required=False)
    child5_note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    child6_name = forms.CharField(max_length=60, required=False)
    child6_mellycode = forms.CharField(max_length=12, required=False)
    child6_tahsilat = forms.ChoiceField(choices=choises_tahsilat, required=False)
    child6_note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    child7_name = forms.CharField(max_length=60, required=False)
    child7_mellycode = forms.CharField(max_length=12, required=False)
    child7_tahsilat = forms.ChoiceField(choices=choises_tahsilat, required=False)
    child7_note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    im_sure = forms.BooleanField(required=False)

    def clean_fname(self):
        fname = self.cleaned_data['fname']
        if len(fname) < 2:
            raise ValidationError("طول مقدار نام و نام خانوادگی باید بیشتر از 2 کاراکتر باشد.")
        for i in fname:
            if i.isdigit():
                raise ValidationError("نام و نام خانوادگی نمیتواند حاوی عدد باشد.")
        return fname

    def clean_lname(self):
        lname = self.cleaned_data['lname']
        if len(lname) < 2:
            raise ValidationError("طول مقدار نام و نام خانوادگی باید بیشتر از 2 کاراکتر باشد.")
        for i in lname:
            if i.isdigit():
                raise ValidationError("نام و نام خانوادگی نمیتواند حاوی عدد باشد.")
        return lname

    def clean_melly_code(self):
        mellycode = self.cleaned_data['melly_code']
        for i in mellycode:
            if not i.isdigit():
                raise ValidationError("کدملی نمیتواند حاوی حروف باشد")
        if (len(mellycode) != 10) and (len(mellycode) != 12):
            raise ValidationError("مقدار کدملی باید 10 یا 12 (متولد افغانستان) باشد.")
        if len(mellycode) == 10:
            if not send_test_melly_result(mellycode):
                raise ValidationError("کد ملی اشتباه است.")
        db = People.objects.filter(melly_code=mellycode).exists()
        if db:
            raise ValidationError("این کد ملی قبلا ثبت شده است.")
        return mellycode

    def clean_shenasnameh(self):
        shenasnameh = self.cleaned_data["shenasnameh"]
        for i in shenasnameh:
            if not i.isdigit():
                raise ValidationError("شناسنامه نمیتواند حاوی حروف باشد")
        return shenasnameh

    def clean_phone_num(self):
        phone_number = self.cleaned_data["phone_num"]
        if len(phone_number) != 0:
            for i in phone_number:
                if not i.isdigit():
                    raise ValidationError("شماره موبایل نمیتواند حاوی حروف باشد.")
            if len(phone_number) != 11:
                raise ValidationError("شماره موبایل باید 11 رقمی باشد.")
        return phone_number

    def clean_home_num(self):
        home_num = self.cleaned_data["home_num"]
        if len(home_num) != 0:
            print(len(home_num))
            for i in home_num:
                if not i.isdigit():
                    raise ValidationError("شماره موبایل نمیتواند حاوی حروف باشد.")
            if (len(home_num) != 11) and (len(home_num) != 8):
                raise ValidationError("شماره منزل باید 8 یا 11 رقمی باشد.")
        return home_num

    def clean_card_num(self):
        card_num = self.cleaned_data["card_num"]
        if len(card_num) != 0:
            for i in card_num:
                if not i.isdigit():
                    raise ValidationError("اطلاعات بانکی نمیتوانند حاوی حروف باشند.")
            if len(card_num) != 16:
                raise ValidationError("شماره کارت اشتباه است. (باید 16 رقم باشد.)")
        return card_num

    def clean_hesab_num(self):
        hesab_num = self.cleaned_data["hesab_num"]
        if len(hesab_num) != 0:
            for i in hesab_num:
                if not i.isdigit():
                    raise ValidationError("اطلاعات بانکی نمیتوانند حاوی حروف باشند.")
        return hesab_num

    def clean_shaba_num(self):
        shaba_num = self.cleaned_data["shaba_num"]
        if len(shaba_num) != 0:
            for i in shaba_num:
                if not i.isdigit():
                    raise ValidationError("اطلاعات بانکی نمیتوانند حاوی حروف باشند.")
            if len(shaba_num) != 24:
                raise ValidationError("شماره شبا اشتباه است.(باید 24 رقم باشد.)")
        return shaba_num

    def clean_birth_place(self):
        birth_place = self.cleaned_data["birth_place"]
        for i in birth_place:
            if i.isdigit():
                raise ValidationError("نام و نام خانوادگی نمیتواند حاوی عدد باشد.")
        return birth_place

    def clean_sex(self):
        sex = self.cleaned_data['sex']
        if sex == "-----":
            raise ValidationError("جنسیت را مشخص کنید.")
        return sex

    def clean_im_sure(self):
        im_sure = self.cleaned_data["im_sure"]
        if not im_sure:
            raise ValidationError("تیک تایید اطلاعات وارد شده را در انتهای صفحه بزنید.")
        return im_sure

    def clean_job(self):
        job = self.cleaned_data["job"]
        for i in job:
            if i.isdigit():
                raise ValidationError("فیلد شغل نمیتواند عدد حروف باشد")
        return job

    def clean_mother_mellycode(self):
        mother_mellycode = self.cleaned_data['mother_mellycode']
        if len(mother_mellycode) != 0:
            for i in mother_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی مادر نمیتواند حاوی حروف باشد")
            if (len(mother_mellycode) != 10) and (len(mother_mellycode) != 12):
                raise ValidationError("مقدار کدملی مادر باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(mother_mellycode) == 10:
                if not send_test_melly_result(mother_mellycode):
                    raise ValidationError("کد ملی مادر اشتباه است.")
        return mother_mellycode

    def clean_father_mellycode(self):
        father_mellycode = self.cleaned_data['father_mellycode']
        if len(father_mellycode) != 0:
            for i in father_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی پدر نمیتواند حاوی حروف باشد")
            if (len(father_mellycode) != 10) and (len(father_mellycode) != 12):
                raise ValidationError("مقدار کدملی پدر باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(father_mellycode) == 10:
                if not send_test_melly_result(father_mellycode):
                    raise ValidationError("کد ملی پدر اشتباه است.")
        return father_mellycode

    def clean_child1_mellycode(self):
        child1_mellycode = self.cleaned_data['child1_mellycode']
        if len(child1_mellycode) != 0:
            for i in child1_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی فرزند1 نمیتواند حاوی حروف باشد")
            if (len(child1_mellycode) != 10) and (len(child1_mellycode) != 12):
                raise ValidationError("مقدار کدملی فرزند1 باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(child1_mellycode) == 10:
                if not send_test_melly_result(child1_mellycode):
                    raise ValidationError("کد ملی فرزند1 اشتباه است.")
        return child1_mellycode

    def clean_child2_mellycode(self):
        child2_mellycode = self.cleaned_data['child2_mellycode']
        if len(child2_mellycode) != 0:
            for i in child2_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی فرزند2 نمیتواند حاوی حروف باشد")
            if (len(child2_mellycode) != 10) and (len(child2_mellycode) != 12):
                raise ValidationError("مقدار کدملی فرزند2 باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(child2_mellycode) == 10:
                if not send_test_melly_result(child2_mellycode):
                    raise ValidationError("کد ملی فرزند2 اشتباه است.")
        return child2_mellycode

    def clean_child3_mellycode(self):
        child3_mellycode = self.cleaned_data['child3_mellycode']
        if len(child3_mellycode) != 0:
            for i in child3_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی فرزند3 نمیتواند حاوی حروف باشد")
            if (len(child3_mellycode) != 10) and (len(child3_mellycode) != 12):
                raise ValidationError("مقدار کدملی فرزند3 باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(child3_mellycode) == 10:
                if not send_test_melly_result(child3_mellycode):
                    raise ValidationError("کد ملی فرزند3 اشتباه است.")
        return child3_mellycode

    def clean_child4_mellycode(self):
        child4_mellycode = self.cleaned_data['child4_mellycode']
        if len(child4_mellycode) != 0:
            for i in child4_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی فرزند 4 نمیتواند حاوی حروف باشد")
            if (len(child4_mellycode) != 10) and (len(child4_mellycode) != 12):
                raise ValidationError("مقدار کدملی فرزند 4 باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(child4_mellycode) == 10:
                if not send_test_melly_result(child4_mellycode):
                    raise ValidationError("کد ملی فرزند 4 اشتباه است.")
        return child4_mellycode

    def clean_child5_mellycode(self):
        child5_mellycode = self.cleaned_data['child5_mellycode']
        if len(child5_mellycode) != 0:
            for i in child5_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی فرزند5 نمیتواند حاوی حروف باشد")
            if (len(child5_mellycode) != 10) and (len(child5_mellycode) != 12):
                raise ValidationError("مقدار کدملی فرزند5 باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(child5_mellycode) == 10:
                if not send_test_melly_result(child5_mellycode):
                    raise ValidationError("کد ملی فرزند5 اشتباه است.")
        return child5_mellycode

    def clean_child6_mellycode(self):
        child6_mellycode = self.cleaned_data['child6_mellycode']
        if len(child6_mellycode) != 0:
            for i in child6_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی فرزند6 نمیتواند حاوی حروف باشد")
            if (len(child6_mellycode) != 10) and (len(child6_mellycode) != 12):
                raise ValidationError("مقدار کدملی فرزند6 باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(child6_mellycode) == 10:
                if not send_test_melly_result(child6_mellycode):
                    raise ValidationError("کد ملی فرزند6 اشتباه است.")
        return child6_mellycode

    def clean_child7_mellycode(self):
        child7_mellycode = self.cleaned_data['child7_mellycode']
        if len(child7_mellycode) != 0:
            for i in child7_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی فرزند 7 نمیتواند حاوی حروف باشد")
            if (len(child7_mellycode) != 10) and (len(child7_mellycode) != 12):
                raise ValidationError("مقدار کدملی فرزند 7 باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(child7_mellycode) == 10:
                if not send_test_melly_result(child7_mellycode):
                    raise ValidationError("کد ملی فرزند 7 اشتباه است.")
        return child7_mellycode

    def clean_husbent_codemelly(self):
        husbent_codemelly = self.cleaned_data['husbent_codemelly']
        if len(husbent_codemelly) != 0:
            for i in husbent_codemelly:
                if not i.isdigit():
                    raise ValidationError("کدملی همسر نمیتواند حاوی حروف باشد")
            if (len(husbent_codemelly) != 10) and (len(husbent_codemelly) != 12):
                raise ValidationError("مقدار کدملی همسر باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(husbent_codemelly) == 10:
                if not send_test_melly_result(husbent_codemelly):
                    raise ValidationError("کد ملی همسر اشتباه است.")
        return husbent_codemelly

    def clean(self):
        birtday_day = self.cleaned_data["birthday_day"]
        birtday_month = self.cleaned_data["birthday_month"]
        birtday_year = self.cleaned_data["birthday_year"]
        if (birtday_day == "--" or birtday_month == "--" or birtday_year == "----") and not (
                birtday_day == "--" and birtday_month == "--" and birtday_year == "----"):
            raise ValidationError("تاریخ تولد اشتباه است (میتوانید هر سه را خالی بگذارید.)")

        pt_type = self.cleaned_data["parvande_type"]
        illness1 = self.cleaned_data["illness1"]
        level1 = self.cleaned_data['level1']
        illness2 = self.cleaned_data["illness2"]
        level2 = self.cleaned_data['level2']
        illness3 = self.cleaned_data["illness3"]
        level3 = self.cleaned_data['level3']
        illness4 = self.cleaned_data["illness4"]
        level4 = self.cleaned_data['level4']
        if pt_type == "توانبخشی":
            if level1 != "-----" and illness1 == "-----":
                raise ValidationError("شما شدت معلولیت 1 را مشخص کردید ولی نوع معلولیت را مشخص نکردید.")
            if level2 != "-----" and illness2 == "-----":
                raise ValidationError("شما شدت معلولیت 2 را مشخص کردید ولی نوع معلولیت را مشخص نکردید.")
            if level3 != "-----" and illness3 == "-----":
                raise ValidationError("شما شدت معلولیت 3 را مشخص کردید ولی نوع معلولیت را مشخص نکردید.")
            if level4 != "-----" and illness4 == "-----":
                raise ValidationError("شما شدت معلولیت 4 را مشخص کردید ولی نوع معلولیت را مشخص نکردید.")


#############################################################
class SearchPerson(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'جستجو بر اساس نام ، نام خانوادگی ، کدملی'}))


#############################################################


class EditPersonForm(forms.Form):
    sex = forms.ChoiceField(required=True, choices=CHOICESsex)
    shenasnameh = forms.CharField(max_length=12, required=False)
    birthday_day = forms.ChoiceField(choices=day, required=False)
    birthday_month = forms.ChoiceField(choices=month, required=False)
    birthday_year = forms.ChoiceField(choices=year, required=False)
    birth_place = forms.CharField(max_length=50, required=False)
    tahsilat = forms.ChoiceField(required=False, choices=choises_tahsilat)
    reshteh_tahsili = forms.CharField(max_length=50, required=False)
    bime = forms.ChoiceField(choices=choose_bime, required=False)
    job = forms.CharField(max_length=70, required=False)
    sarbazi_status = forms.ChoiceField(choices=sarbazi_choice, required=False)
    parvande_type = forms.ChoiceField(choices=parvande_type_choose, required=False)
    pt_ejtemaee = forms.ChoiceField(choices=pt_ejtemaee_choice, required=False)
    pt_behboodyafte = forms.ChoiceField(choices=pt_behboodyafte_choice, required=False)
    maharat_behbod = forms.CharField(required=False, max_length=70)
    work_history = forms.CharField(required=False, max_length=20)
    bime_type = forms.ChoiceField(required=False, choices=bime_type_ch)
    mostamary_status = forms.ChoiceField(required=False, choices=CHOICESmostamary)
    report_date_day = forms.ChoiceField(required=False, choices=day)
    report_date_month = forms.ChoiceField(required=False, choices=month)
    report_date_year = forms.ChoiceField(required=False, choices=year3)
    taahol_status = forms.ChoiceField(choices=taahol_choice, required=False)
    illness1 = forms.ChoiceField(choices=illness_choice, required=False)
    level1 = forms.ChoiceField(choices=level_choice, required=False)
    illness2 = forms.ChoiceField(choices=illness_choice, required=False)
    level2 = forms.ChoiceField(choices=level_choice, required=False)
    illness3 = forms.ChoiceField(choices=illness_choice, required=False)
    level3 = forms.ChoiceField(choices=level_choice, required=False)
    illness4 = forms.ChoiceField(choices=illness_choice, required=False)
    level4 = forms.ChoiceField(choices=level_choice, required=False)
    address = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    residancy_area = forms.ChoiceField(choices=residenty_area_choose, required=False)
    phone_num = forms.CharField(max_length=11, required=False)
    home_num = forms.CharField(max_length=11, required=False)
    note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    father_name = forms.CharField(max_length=50, required=False)
    mother_fname = forms.CharField(max_length=50, required=False)
    mother_lname = forms.CharField(max_length=50, required=False)
    father_job = forms.CharField(max_length=50, required=False)
    mother_job = forms.CharField(max_length=50, required=False)
    father_degree = forms.ChoiceField(choices=choises_tahsilat, required=False)
    mother_degree = forms.ChoiceField(choices=choises_tahsilat, required=False)
    father_mellycode = forms.CharField(required=False)
    mother_mellycode = forms.CharField(required=False)
    brothers_num = forms.ChoiceField(choices=siblings_num, required=False)
    sisters_num = forms.ChoiceField(choices=siblings_num, required=False)
    takafol_num = forms.ChoiceField(choices=takafol_num_ch , required=False)
    live_situation = forms.ChoiceField(required=False, choices=live_situation_choice)
    rahn = forms.IntegerField(required=False, min_value=0)
    ejareh = forms.FloatField(required=False, min_value=0)
    card_num = forms.CharField(required=False)
    hesab_num = forms.CharField(required=False)
    shaba_num = forms.CharField(required=False)
    husbent_name = forms.CharField(required=False, max_length=50)
    husbent_codemelly = forms.CharField(required=False, max_length=50)
    husbent_job = forms.CharField(required=False, max_length=50)
    husbent_tahsilat = forms.ChoiceField(required=False, choices=choises_tahsilat)
    childs_number = forms.ChoiceField(choices=child_num_choice, required=False)
    child1_name = forms.CharField(max_length=60, required=False)
    child1_mellycode = forms.CharField(max_length=12, required=False)
    child1_tahsilat = forms.ChoiceField(choices=choises_tahsilat, required=False)
    child1_note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    child2_name = forms.CharField(max_length=60, required=False)
    child2_mellycode = forms.CharField(max_length=12, required=False)
    child2_tahsilat = forms.ChoiceField(choices=choises_tahsilat, required=False)
    child2_note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    child3_name = forms.CharField(max_length=60, required=False)
    child3_mellycode = forms.CharField(max_length=12, required=False)
    child3_tahsilat = forms.ChoiceField(choices=choises_tahsilat, required=False)
    child3_note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    child4_name = forms.CharField(max_length=60, required=False)
    child4_mellycode = forms.CharField(max_length=12, required=False)
    child4_tahsilat = forms.ChoiceField(choices=choises_tahsilat, required=False)
    child4_note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    child5_name = forms.CharField(max_length=60, required=False)
    child5_mellycode = forms.CharField(max_length=12, required=False)
    child5_tahsilat = forms.ChoiceField(choices=choises_tahsilat, required=False)
    child5_note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    child6_name = forms.CharField(max_length=60, required=False)
    child6_mellycode = forms.CharField(max_length=12, required=False)
    child6_tahsilat = forms.ChoiceField(choices=choises_tahsilat, required=False)
    child6_note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    child7_name = forms.CharField(max_length=60, required=False)
    child7_mellycode = forms.CharField(max_length=12, required=False)
    child7_tahsilat = forms.ChoiceField(choices=choises_tahsilat, required=False)
    child7_note = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    im_sure = forms.BooleanField(required=False)

    def __init__(self, code_melly, *args, **kwargs):
        super(EditPersonForm, self).__init__(*args, **kwargs)
        person = People.objects.get(melly_code=code_melly)
        if person.shenasnameh != "-----":
            self.fields['shenasnameh'].initial = person.shenasnameh
        self.fields['sex'].initial = person.sex
        self.fields['birthday_day'].initial = person.birthday_day
        self.fields['birthday_month'].initial = person.birthday_month
        self.fields['birthday_year'].initial = person.birthday_year

        self.fields["report_date_day"].initial = person.report_date_day
        self.fields["report_date_month"].initial = person.report_date_month
        self.fields["report_date_year"].initial = person.report_date_year

        if person.birth_place != "-----":
            self.fields['birth_place'].initial = person.birth_place

        self.fields['tahsilat'].initial = person.tahsilat
        if person.reshteh_tahsili != "-----":
            self.fields['reshteh_tahsili'].initial = person.reshteh_tahsili
        self.fields['bime'].initial = person.bime

        if person.job != "-----":
            self.fields['job'].initial = person.job

        self.fields['sarbazi_status'].initial = person.sarbazi_status
        self.fields['parvande_type'].initial = person.parvande_type
        self.fields['pt_ejtemaee'].initial = person.pt_ejtemaee
        self.fields['pt_behboodyafte'].initial = person.pt_behboodyafte
        self.fields['mostamary_status'].initial = person.mostamary_status
        self.fields['taahol_status'].initial = person.taahol_status
        self.fields['illness1'].initial = person.illness1
        self.fields['level1'].initial = person.level1
        self.fields['illness2'].initial = person.illness2
        self.fields['level2'].initial = person.level2
        self.fields['illness3'].initial = person.illness3
        self.fields['level3'].initial = person.level3
        self.fields['illness4'].initial = person.illness4
        self.fields['level4'].initial = person.level4

        self.fields['maharat_behbod'].initial = person.maharat_behbod
        self.fields["work_history"].initial = person.work_history
        self.fields["bime_type"].initial = person.bime_type
        if person.address != "-----":
            self.fields['address'].initial = person.address

        self.fields['residancy_area'].initial = person.residancy_area

        if person.phone_num != "-----":
            self.fields['phone_num'].initial = person.phone_num

        if person.home_num != "-----":
            self.fields['home_num'].initial = person.home_num

        if person.card_num != "-----":
            self.fields["card_num"].initial = person.card_num

        if person.hesab_num != "-----":
            self.fields["hesab_num"].initial = person.hesab_num

        if person.shaba_num != "-----":
            self.fields["shaba_num"].initial = person.shaba_num

        if person.note != "-----":
            self.fields['note'].initial = person.note

        if person.father_name != "-----":
            self.fields['father_name'].initial = person.father_name

        if person.mother_fname != "-----":
            self.fields['mother_fname'].initial = person.mother_fname

        if person.mother_lname != "-----":
            self.fields['mother_lname'].initial = person.mother_lname

        if person.father_job != "-----":
            self.fields['father_job'].initial = person.father_job

        if person.mother_job != "-----":
            self.fields['mother_job'].initial = person.mother_job

        self.fields['father_degree'].initial = person.father_degree
        self.fields['mother_degree'].initial = person.mother_degree

        if person.father_mellycode != "-----":
            self.fields['father_mellycode'].initial = person.father_mellycode

        if person.mother_mellycode != "-----":
            self.fields['mother_mellycode'].initial = person.mother_mellycode

        self.fields["sisters_num"].initial = person.sisters_num
        self.fields["brothers_num"].initial = person.brothers_num
        self.fields["takafol_num"].initial = person.takafol_num
        self.fields['live_situation'].initial = person.live_situation

        if person.rahn != "-----":
            self.fields['rahn'].initial = person.rahn

        if person.ejareh != "-----":
            self.fields['ejareh'].initial = person.ejareh

        if person.husbent_name != "-----":
            self.fields['husbent_name'].initial = person.husbent_name

        if person.husbent_codemelly != "-----":
            self.fields['husbent_codemelly'].initial = person.husbent_codemelly

        if person.husbent_job != "-----":
            self.fields['husbent_job'].initial = person.husbent_job

        self.fields['husbent_tahsilat'].initial = person.husbent_tahsilat
        self.fields['childs_number'].initial = person.childs_number

        if person.child1_name != "-----":
            self.fields['child1_name'].initial = person.child1_name

        if person.child1_mellycode != "-----":
            self.fields['child1_mellycode'].initial = person.child1_mellycode

        self.fields['child1_tahsilat'].initial = person.child1_tahsilat

        if person.child1_note != "-----":
            self.fields['child1_note'].initial = person.child1_note

        if person.child2_name != "-----":
            self.fields['child2_name'].initial = person.child2_name

        if person.child2_mellycode != "-----":
            self.fields['child2_mellycode'].initial = person.child2_mellycode

        self.fields['child2_tahsilat'].initial = person.child2_tahsilat

        if person.child2_note != "-----":
            self.fields['child2_note'].initial = person.child2_note

        if person.child3_name != "-----":
            self.fields['child3_name'].initial = person.child3_name

        if person.child3_mellycode != "-----":
            self.fields['child3_mellycode'].initial = person.child3_mellycode

        self.fields['child3_tahsilat'].initial = person.child3_tahsilat

        if person.child3_note != "-----":
            self.fields['child3_note'].initial = person.child3_note

        if person.child4_name != "-----":
            self.fields['child4_name'].initial = person.child4_name

        if person.child4_mellycode != "-----":
            self.fields['child4_mellycode'].initial = person.child4_mellycode

        self.fields['child4_tahsilat'].initial = person.child4_tahsilat

        if person.child4_note != "-----":
            self.fields['child4_note'].initial = person.child4_note

        if person.child5_name != "-----":
            self.fields['child5_name'].initial = person.child5_name

        if person.child5_mellycode != "-----":
            self.fields['child5_mellycode'].initial = person.child5_mellycode

        self.fields['child5_tahsilat'].initial = person.child5_tahsilat

        if person.child5_note != "-----":
            self.fields['child5_note'].initial = person.child5_note

        if person.child6_name != "-----":
            self.fields['child6_name'].initial = person.child6_name

        if person.child6_mellycode != "-----":
            self.fields['child6_mellycode'].initial = person.child6_mellycode

        self.fields['child6_tahsilat'].initial = person.child6_tahsilat

        if person.child6_note != "-----":
            self.fields['child6_note'].initial = person.child6_note

        if person.child7_name != "-----":
            self.fields['child7_name'].initial = person.child7_name

        if person.child7_mellycode != "-----":
            self.fields['child7_mellycode'].initial = person.child7_mellycode

        self.fields['child7_tahsilat'].initial = person.child7_tahsilat

        if person.child7_note != "-----":
            self.fields['child7_note'].initial = person.child7_note

    def clean_fname(self):
        fname = self.cleaned_data['fname']
        if len(fname) < 2:
            raise ValidationError("طول مقدار نام و نام خانوادگی باید بیشتر از 2 کاراکتر باشد.")
        for i in fname:
            if i.isdigit():
                raise ValidationError("نام و نام خانوادگی نمیتواند حاوی عدد باشد.")
        return fname

    def clean_lname(self):
        lname = self.cleaned_data['lname']
        if len(lname) < 2:
            raise ValidationError("طول مقدار نام و نام خانوادگی باید بیشتر از 2 کاراکتر باشد.")
        for i in lname:
            if i.isdigit():
                raise ValidationError("نام و نام خانوادگی نمیتواند حاوی عدد باشد.")
        return lname

    def clean_melly_code(self):
        mellycode = self.cleaned_data['melly_code']
        for i in mellycode:
            if not i.isdigit():
                raise ValidationError("کدملی نمیتواند حاوی حروف باشد")
        if (len(mellycode) != 10) and (len(mellycode) != 12):
            raise ValidationError("مقدار کدملی باید 10 یا 12 (متولد افغانستان) باشد.")
        if len(mellycode) == 10:
            if not send_test_melly_result(mellycode):
                raise ValidationError("کد ملی اشتباه است.")
        db = People.objects.filter(melly_code=mellycode).exists()
        if db:
            raise ValidationError("این کد ملی قبلا ثبت شده است.")
        return mellycode

    def clean_shenasnameh(self):
        shenasnameh = self.cleaned_data["shenasnameh"]
        for i in shenasnameh:
            if not i.isdigit():
                raise ValidationError("شناسنامه نمیتواند حاوی حروف باشد")
        return shenasnameh

    def clean_phone_num(self):
        phone_number = self.cleaned_data["phone_num"]
        if len(phone_number) != 0:
            for i in phone_number:
                if not i.isdigit():
                    raise ValidationError("شماره موبایل نمیتواند حاوی حروف باشد.")
            if len(phone_number) != 11:
                raise ValidationError("شماره موبایل باید 11 رقمی باشد.")
        return phone_number

    def clean_card_num(self):
        card_num = self.cleaned_data["card_num"]
        if len(card_num) != 0:
            for i in card_num:
                if not i.isdigit():
                    raise ValidationError("اطلاعات بانکی نمیتوانند حاوی حروف باشند.")
            if len(card_num) != 16:
                raise ValidationError("شماره کارت اشتباه است. (باید 16 رقم باشد.)")
        return card_num

    def clean_hesab_num(self):
        hesab_num = self.cleaned_data["hesab_num"]
        if len(hesab_num) != 0:
            for i in hesab_num:
                if not i.isdigit():
                    raise ValidationError("اطلاعات بانکی نمیتوانند حاوی حروف باشند.")
        return hesab_num

    def clean_shaba_num(self):
        shaba_num = self.cleaned_data["shaba_num"]
        if len(shaba_num) != 0:
            for i in shaba_num:
                if not i.isdigit():
                    raise ValidationError("اطلاعات بانکی نمیتوانند حاوی حروف باشند.")
            if len(shaba_num) != 24:
                raise ValidationError("شماره شبا اشتباه است.(باید 24 رقم باشد.)")
        return shaba_num

    def clean_home_num(self):
        home_num = self.cleaned_data["home_num"]
        if len(home_num) != 0:
            print(len(home_num))
            for i in home_num:
                if not i.isdigit():
                    raise ValidationError("شماره موبایل نمیتواند حاوی حروف باشد.")
            if (len(home_num) != 11) and (len(home_num) != 8):
                raise ValidationError("شماره منزل باید 8 یا 11 رقمی باشد.")
        return home_num

    def clean_birth_place(self):
        birth_place = self.cleaned_data["birth_place"]
        for i in birth_place:
            if i.isdigit():
                raise ValidationError("نام و نام خانوادگی نمیتواند حاوی عدد باشد.")
        return birth_place

    def clean_sex(self):
        sex = self.cleaned_data['sex']
        if sex == "-----":
            raise ValidationError("جنسیت را مشخص کنید.")
        return sex

    def clean_im_sure(self):
        im_sure = self.cleaned_data["im_sure"]
        if not im_sure:
            raise ValidationError("تیک تایید اطلاعات وارد شده را در انتهای صفحه بزنید.")
        return im_sure

    def clean_job(self):
        job = self.cleaned_data["job"]
        for i in job:
            if i.isdigit():
                raise ValidationError("فیلد شغل نمیتواند حاوی عدد باشد")
        return job

    def clean_mother_mellycode(self):
        mother_mellycode = self.cleaned_data['mother_mellycode']
        if len(mother_mellycode) != 0:
            for i in mother_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی مادر نمیتواند حاوی حروف باشد")
            if (len(mother_mellycode) != 10) and (len(mother_mellycode) != 12):
                raise ValidationError("مقدار کدملی مادر باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(mother_mellycode) == 10:
                if not send_test_melly_result(mother_mellycode):
                    raise ValidationError("کد ملی مادر اشتباه است.")
        return mother_mellycode

    def clean_father_mellycode(self):
        father_mellycode = self.cleaned_data['father_mellycode']
        if len(father_mellycode) != 0:
            for i in father_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی پدر نمیتواند حاوی حروف باشد")
            if (len(father_mellycode) != 10) and (len(father_mellycode) != 12):
                raise ValidationError("مقدار کدملی پدر باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(father_mellycode) == 10:
                if not send_test_melly_result(father_mellycode):
                    raise ValidationError("کد ملی پدر اشتباه است.")
        return father_mellycode

    def clean_child1_mellycode(self):
        child1_mellycode = self.cleaned_data['child1_mellycode']
        if len(child1_mellycode) != 0:
            for i in child1_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی فرزند1 نمیتواند حاوی حروف باشد")
            if (len(child1_mellycode) != 10) and (len(child1_mellycode) != 12):
                raise ValidationError("مقدار کدملی فرزند1 باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(child1_mellycode) == 10:
                if not send_test_melly_result(child1_mellycode):
                    raise ValidationError("کد ملی فرزند1 اشتباه است.")
        return child1_mellycode

    def clean_child2_mellycode(self):
        child2_mellycode = self.cleaned_data['child2_mellycode']
        if len(child2_mellycode) != 0:
            for i in child2_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی فرزند2 نمیتواند حاوی حروف باشد")
            if (len(child2_mellycode) != 10) and (len(child2_mellycode) != 12):
                raise ValidationError("مقدار کدملی فرزند2 باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(child2_mellycode) == 10:
                if not send_test_melly_result(child2_mellycode):
                    raise ValidationError("کد ملی فرزند2 اشتباه است.")
        return child2_mellycode

    def clean_child3_mellycode(self):
        child3_mellycode = self.cleaned_data['child3_mellycode']
        if len(child3_mellycode) != 0:
            for i in child3_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی فرزند3 نمیتواند حاوی حروف باشد")
            if (len(child3_mellycode) != 10) and (len(child3_mellycode) != 12):
                raise ValidationError("مقدار کدملی فرزند3 باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(child3_mellycode) == 10:
                if not send_test_melly_result(child3_mellycode):
                    raise ValidationError("کد ملی فرزند3 اشتباه است.")
        return child3_mellycode

    def clean_child4_mellycode(self):
        child4_mellycode = self.cleaned_data['child4_mellycode']
        if len(child4_mellycode) != 0:
            for i in child4_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی فرزند 4 نمیتواند حاوی حروف باشد")
            if (len(child4_mellycode) != 10) and (len(child4_mellycode) != 12):
                raise ValidationError("مقدار کدملی فرزند 4 باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(child4_mellycode) == 10:
                if not send_test_melly_result(child4_mellycode):
                    raise ValidationError("کد ملی فرزند 4 اشتباه است.")
        return child4_mellycode

    def clean_child5_mellycode(self):
        child5_mellycode = self.cleaned_data['child5_mellycode']
        if len(child5_mellycode) != 0:
            for i in child5_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی فرزند5 نمیتواند حاوی حروف باشد")
            if (len(child5_mellycode) != 10) and (len(child5_mellycode) != 12):
                raise ValidationError("مقدار کدملی فرزند5 باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(child5_mellycode) == 10:
                if not send_test_melly_result(child5_mellycode):
                    raise ValidationError("کد ملی فرزند5 اشتباه است.")
        return child5_mellycode

    def clean_child6_mellycode(self):
        child6_mellycode = self.cleaned_data['child6_mellycode']
        if len(child6_mellycode) != 0:
            for i in child6_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی فرزند6 نمیتواند حاوی حروف باشد")
            if (len(child6_mellycode) != 10) and (len(child6_mellycode) != 12):
                raise ValidationError("مقدار کدملی فرزند6 باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(child6_mellycode) == 10:
                if not send_test_melly_result(child6_mellycode):
                    raise ValidationError("کد ملی فرزند6 اشتباه است.")
        return child6_mellycode

    def clean_child7_mellycode(self):
        child7_mellycode = self.cleaned_data['child7_mellycode']
        if len(child7_mellycode) != 0:
            for i in child7_mellycode:
                if not i.isdigit():
                    raise ValidationError("کدملی فرزند 7 نمیتواند حاوی حروف باشد")
            if (len(child7_mellycode) != 10) and (len(child7_mellycode) != 12):
                raise ValidationError("مقدار کدملی فرزند 7 باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(child7_mellycode) == 10:
                if not send_test_melly_result(child7_mellycode):
                    raise ValidationError("کد ملی فرزند 7 اشتباه است.")
        return child7_mellycode

    def clean_husbent_codemelly(self):
        husbent_codemelly = self.cleaned_data['husbent_codemelly']
        if len(husbent_codemelly) != 0:
            for i in husbent_codemelly:
                if not i.isdigit():
                    raise ValidationError("کدملی همسر نمیتواند حاوی حروف باشد")
            if (len(husbent_codemelly) != 10) and (len(husbent_codemelly) != 12):
                raise ValidationError("مقدار کدملی همسر باید 10 یا 12 (متولد افغانستان) باشد.")
            if len(husbent_codemelly) == 10:
                if not send_test_melly_result(husbent_codemelly):
                    raise ValidationError("کد ملی همسر اشتباه است.")
        return husbent_codemelly

    def clean(self):
        birtday_day = self.cleaned_data["birthday_day"]
        birtday_month = self.cleaned_data["birthday_month"]
        birtday_year = self.cleaned_data["birthday_year"]
        if (birtday_day == "--" or birtday_month == "--" or birtday_year == "----") and not (
                birtday_day == "--" and birtday_month == "--" and birtday_year == "----"):
            raise ValidationError("تاریخ تولد اشتباه است (میتوانید هر سه را خالی بگذارید.)")

        report_date_day = self.cleaned_data["report_date_day"]
        report_date_month = self.cleaned_data["report_date_month"]
        report_date_year = self.cleaned_data["report_date_year"]
        if (report_date_day == "--" or report_date_month == "--" or report_date_year == "----") and not (
                report_date_day == "--" and report_date_month == "--" and report_date_year == "----"):
            raise ValidationError("تاریخ آخرین بازدید از منزل اشتباه است (میتوانید هر سه را خالی بگذارید.)")

        pt_type = self.cleaned_data["parvande_type"]
        illness1 = self.cleaned_data["illness1"]
        level1 = self.cleaned_data['level1']
        illness2 = self.cleaned_data["illness2"]
        level2 = self.cleaned_data['level2']
        illness3 = self.cleaned_data["illness3"]
        level3 = self.cleaned_data['level3']
        illness4 = self.cleaned_data["illness4"]
        level4 = self.cleaned_data['level4']
        if pt_type == "توانبخشی":
            if level1 != "-----" and illness1 == "-----":
                raise ValidationError("شما شدت معلولیت 1 را مشخص کردید ولی نوع معلولیت را مشخص نکردید.")
            if level2 != "-----" and illness2 == "-----":
                raise ValidationError("شما شدت معلولیت 2 را مشخص کردید ولی نوع معلولیت را مشخص نکردید.")
            if level3 != "-----" and illness3 == "-----":
                raise ValidationError("شما شدت معلولیت 3 را مشخص کردید ولی نوع معلولیت را مشخص نکردید.")
            if level4 != "-----" and illness4 == "-----":
                raise ValidationError("شما شدت معلولیت 4 را مشخص کردید ولی نوع معلولیت را مشخص نکردید.")


class NewHomeReport(forms.Form):
    report_date_day = forms.ChoiceField(required=False, choices=day)
    report_date_month = forms.ChoiceField(required=False, choices=month)
    report_date_year = forms.ChoiceField(required=False, choices=year3)

    def clean(self):
        report_date_day = self.cleaned_data["report_date_day"]
        report_date_month = self.cleaned_data["report_date_month"]
        report_date_year = self.cleaned_data["report_date_year"]
        if report_date_day == "--" or report_date_month == "--" or report_date_year == "----":
            raise ValidationError("تاریخ اشتباه است.")


class NewKhadamat(forms.Form):
    Khedmat_name = forms.CharField(required=False)
    khedmat_date_day = forms.ChoiceField(required=False, choices=day)
    khedmat_date_month = forms.ChoiceField(required=False, choices=month)
    khedmat_date_year = forms.ChoiceField(required=False, choices=year3)
    tozihat = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)
    mail_code = forms.CharField(required=False)

    def clean_Khedmat_name(self):
        Khedmat_name = self.cleaned_data["Khedmat_name"]
        if len(Khedmat_name) < 2:
            raise ValidationError("فیلد (موضوع خدمات ارائه شده) اجباری است.")
        return Khedmat_name

    def clean(self):
        khedmat_date_day = self.cleaned_data["khedmat_date_day"]
        khedmat_date_month = self.cleaned_data["khedmat_date_month"]
        khedmat_date_year = self.cleaned_data["khedmat_date_year"]
        if khedmat_date_day == "--" or khedmat_date_month == "--" or khedmat_date_year == "----":
            raise ValidationError("تاریخ اشتباه است.")


class NewDarkhast(forms.Form):
    darkhast_name = forms.CharField(required=False)
    darkhast_date_day = forms.ChoiceField(required=False, choices=day)
    darkhast_date_month = forms.ChoiceField(required=False, choices=month)
    darkhast_date_year = forms.ChoiceField(required=False, choices=year3)
    tozihat = forms.CharField(widget=forms.Textarea, max_length=9999, required=False)

    def clean_darkhast_name(self):
        darkhast_name = self.cleaned_data["darkhast_name"]
        if len(darkhast_name) < 2:
            raise ValidationError("فیلد (موضوع درخواست) اجباری است.")
        return darkhast_name

    def clean(self):
        darkhast_date_day = self.cleaned_data["darkhast_date_day"]
        darkhast_date_month = self.cleaned_data["darkhast_date_month"]
        darkhast_date_year = self.cleaned_data["darkhast_date_year"]
        if darkhast_date_day == "--" or darkhast_date_month == "--" or darkhast_date_year == "----":
            raise ValidationError("تاریخ اشتباه است.")

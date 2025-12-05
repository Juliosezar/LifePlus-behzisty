from math import prod
from .models import Case, CaseDocuments, CaseFamilyMembers, CaseNotes, Disability, ReasonCase, RecoveredReasonCase, Visit


import sqlite3
def move():
        case = Case.objects.all()
        case.delete()
        case_family_members = CaseFamilyMembers.objects.all()
        case_family_members.delete()
        case_notes = CaseNotes.objects.all()
        case_notes.delete()
        disability = Disability.objects.all()
        disability.delete()
        reason_case = ReasonCase.objects.all()
        reason_case.delete()
        recovered_reason_case = RecoveredReasonCase.objects.all()
        recovered_reason_case.delete()
        visit = Visit.objects.all()
        visit.delete()


        import os
        import sqlite3

        # CHANGE THIS to your exact path starting with /home/...
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, 'db.sqlite3')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM people_people;")


        rows = cursor.fetchall()
        for row in rows:
            first_name = row[1]
            last_name = row[2]
            national_id = row[3]
            sex = row[5]
            if sex == "زن":
                gender = "F"
            else:
                gender = "M"
            shenasnameh = row[6]
            if shenasnameh == "-----" or shenasnameh == '0':
                shenasnameh = None
            else:
                shenasnameh = shenasnameh
            bith_day = row[7]
            bith_month = row[8]
            bith_year = row[9]
            if bith_day == "--" or bith_month == "--" or bith_year == "----":
                birthdate = None
            else:
                birthdate = f"{bith_year}-{bith_month}-{bith_day}"
            birth_place = row[10]
            if birth_place == "-----":
                birth_place = None
            education = row[11]
            if education == "-----":
                education = None
            elif education == 'بی سواد':
                education = "illiterate"
            elif education == "ابتدایی":
                education = "elementary"
            elif education == "متوسطه اول (سیکل)":
                education = "middle_school"
            elif education == "متوسطه دوم (دیپلم)":
                education = "high_school"
            elif education == "کاردانی (فوق دیپلم)":
                education = "associate"
            elif education == "کارشناسی (لیسانس)":
                education = "bachelor"
            elif education == "کارشناسی ارشد (فوق لیسانس)":
                education = "master"
            elif education == "دکترا":
                education = "phd"
            elif education == "فوق دکترا":
                education = "post_doc"
            education_field = row[12]
            if education_field == "-----":
                education_field = None
            bime = row[13]
            if bime == "-----":
                bime = None
            elif bime == "ندارد":
                bime = 'none'
            elif bime == "تامین اجتماعی":
                bime = 'social_security'
            elif bime == "بهزیستی":
                bime = 'welfare'
            elif bime == "قالی بافی":
                bime = 'carpet_weaving'
            elif bime == "خویش فرمایی":
                bime = 'self_employed'
            elif bime == "عمر":
                bime = 'life'
            elif bime == "کارفرمایی":
                bime = 'employer'
            elif bime == "کارگری":
                bime = 'labor'
            elif bime == "خدمات درمانی":
                bime = 'medical_services'
            elif bime == "زنان خانه دار":
                bime = 'housewives'
            elif bime == "روستاییان":
                bime = 'rural'
            elif bime == "سلامت ایرانیان":
                bime = 'iranian_health'
            elif bime == "سلامت همگانی":
                bime = 'universal_health'
            elif bime == "سلامت - کارکنان دولت":
                bime = 'gov_employees'
            elif bime == "سلامت - سایر اقشار":
                bime = 'other_sectors'
            elif bime == "نیروهای مسلح":
                bime = 'armed_forces'
            elif bime == "بیماران خاص":
                bime = 'special_patients'
            job = row[14]
            if job == "-----":
                job = None
            military = row[15]
            if military == "-----":
                military = None
            elif military == "غیبت":
                military = 'absence'
            elif military == "معافیت":
                military = 'exempt'
            elif military == "گذرانده":
                military = 'passed'
            case_type = row[16]
            if case_type == "-----":
                case_type = None
            elif case_type == "توانبخشی":
                case_type = 'rehab'
            elif case_type == "اجتماعی":
                case_type = 'social'
            elif case_type == "بهبود یافته":
                case_type = 'recovered'
            ejtemaie_reson = row[17]
            if ejtemaie_reson == "-----":
                ejtemaie_reson = None
            elif ejtemaie_reson == "مرد از کار افتاده":
                ejtemaie_reson = 'man_cant_work'
            elif ejtemaie_reson == "شوهر فوت شده":
                ejtemaie_reson = 'husbend_died'
            elif ejtemaie_reson == "طلاق گرفته":
                ejtemaie_reson = 'divorce'
            elif ejtemaie_reson == "دختر خود سرپرست":
                ejtemaie_reson = 'self_governing_girl'
            elif ejtemaie_reson == "دختر بد سرپرست":
                ejtemaie_reson = 'bad_guardian_girl'
            elif ejtemaie_reson == "متارکه کرده":
                ejtemaie_reson = 'leaved_partner'
            elif ejtemaie_reson == "کودک فاقد سرپرست":
                ejtemaie_reson = 'no_family_child'
            recovered_reason = row[18]
            if recovered_reason == "-----":
                recovered_reason = None
            elif recovered_reason == "وام اشتغال":
                recovered_reason = 'employment_loan'
            elif recovered_reason == "حق بیمه":
                recovered_reason = 'insurance_right'
            elif recovered_reason == "کاهش هزینه انشعابات":
                recovered_reason = 'cost_reduction'
            pension = row[19]
            if pension == "-----":
                pension = None
            elif pension == "مستمر":
                pension = 'continuous'
            elif pension == "غیرمستمر":
                pension = 'non_continuous'
            
            marriage = row[20]
            if marriage == "-----":
                marriage = None
            elif marriage == "متاهل":
                marriage = 'married'
            elif marriage == "مطلقه":
                marriage = 'divorced'
            elif marriage == "متارکه":
                marriage = 'separated'
            elif marriage == "مجرد":
                marriage = 'single'
            elif marriage == "همسر فوت شده":
                marriage = 'widowed'
  
            illness1 = row[21]
            level1 = row[22]
            illness2 = row[23]
            level2 = row[24]
            illness3 = row[25]
            level3 = row[26]
            illness4 = row[27]
            level4 = row[28]
            if illness1 == "-----":
                illness1 = None
            elif illness1 == "جسمی حرکتی":
                illness1 = 'body_movment'
            elif illness1 == "جسمی حرکتی(ام اس)":
                illness1 = 'body_movment_ms'
            elif illness1 == "اعصاب و روان":
                illness1 = 'nerves_psyche'
            elif illness1 == "شنوایی":
                illness1 = 'hearing'
            elif illness1 == "بینایی":
                illness1 = 'vision'
            elif illness1 == "ذهنی":
                illness1 = 'mental'
            elif illness1 == "گفتاری":
              illness1 = 'spoken'
            elif illness1 == "اوتیسم":
                illness1 = 'autism'
            elif illness1 == "ضایعه نخاعی":
                illness1 = 'spinal_cord'
            elif illness1 == "سالمندی":
                illness1 = 'old_age'
            elif illness1 == "آلزایمر":
                illness1 = 'alzheimer'
            elif illness1 == "دمانس":
                illness1 = 'dementia'
            elif illness1 == "فاقد معلولیت":
                illness1 = 'no_disability'
            elif illness1 == "فاقد مدارک لازم":
                illness1 = 'no_document'
            if illness2 == "-----":
                illness2 = None
            elif illness2 == "جسمی حرکتی":
                illness2 = 'body_movment'
            elif illness2 == "جسمی حرکتی(ام اس)":
                illness2 = 'body_movment_ms'
            elif illness2 == "اعصاب و روان":
                illness2 = 'nerves_psyche'
            elif illness2 == "شنوایی":
                illness2 = 'hearing'
            elif illness2 == "بینایی":
                illness2 = 'vision'
            elif illness2 == "ذهنی":
                illness2 = 'mental'
            elif illness2 == "گفتاری":
                illness2 = 'spoken'
            elif illness2 == "اوتیسم":
                illness2 = 'autism'
            elif illness2 == "ضایعه نخاعی":
                illness2 = 'spinal_cord'
            elif illness2 == "سالمندی":
                illness2 = 'old_age'
            elif illness2 == "آلزایمر":
                illness2 = 'alzheimer'
            elif illness2 == "دمانس":
                illness2 = 'dementia'
            elif illness2 == "فاقد معلولیت":
                illness2 = 'no_disability'
            elif illness2 == "فاقد مدارک لازم":
                illness2 = 'no_document'
            if illness3 == "-----":
                illness3 = None
            elif illness3 == "جسمی حرکتی":
                illness3 = 'body_movment'
            elif illness3 == "جسمی حرکتی(ام اس)":
                illness3 = 'body_movment_ms'
            elif illness3 == "اعصاب و روان":
                illness3 = 'nerves_psyche'
            elif illness3 == "شنوایی":
                illness3 = 'hearing'
            elif illness3 == "بینایی":
                illness3 = 'vision'
            elif illness3 == "ذهنی":
                illness3 = 'mental'
            elif illness3 == "گفتاری":
                illness3 = 'spoken'
            elif illness3 == "اوتیسم":
                illness3 = 'autism'
            elif illness3 == "ضایعه نخاعی":
                illness3 = 'spinal_cord'
            elif illness3 == "سالمندی":
                illness3 = 'old_age'
            elif illness3 == "آلزایمر":
                illness3 = 'alzheimer'
            elif illness3 == "دمانس":
                illness3 = 'dementia'
            elif illness3 == "فاقد معلولیت":
                illness3 = 'no_disability'
            elif illness3 == "فاقد مدارک لازم":
                illness3 = 'no_document'
            if illness4 == "-----":
                illness4 = None
            elif illness4 == "جسمی حرکتی":
                illness4 = 'body_movment'
            elif illness4 == "جسمی حرکتی(ام اس)":
                illness4 = 'body_movment_ms'
            elif illness4 == "اعصاب و روان":
                illness4 = 'nerves_psyche'
            elif illness4 == "شنوایی":
                illness4 = 'hearing'
            elif illness4 == "بینایی":
                illness4 = 'vision'
            elif illness4 == "ذهنی":
                illness4 = 'mental'
            elif illness4 == "گفتاری":
                illness4 = 'spoken'
            elif illness4 == "اوتیسم":
                illness4 = 'autism'
            elif illness4 == "ضایعه نخاعی":
                illness4 = 'spinal_cord'
            elif illness4 == "سالمندی":
                illness4 = 'old_age'
            elif illness4 == "آلزایمر":
                illness4 = 'alzheimer'
            elif illness4 == "دمانس":
                illness4 = 'dementia'
            elif illness4 == "فاقد معلولیت":
                illness4 = 'no_disability'
            elif illness4 == "فاقد مدارک لازم":
                illness4 = 'no_document'
            if level1 == "-----":
                level1 = None
            elif level1 == "خفیف":
                level1 = 'level1'
            elif level1 == "متوسط":
                level1 = 'level2'
            elif level1 == "شدید":
                level1 = 'level3'
            elif level1 == "خیلی شدید":
                level1 = 'level4'
            elif level1 == "ندارد":
                level1 = 'none'
            if level2 == "-----":
                level2 = None
            elif level2 == "خفیف":
                level2 = 'level1'
            elif level2 == "متوسط":
                level2 = 'level2'
            elif level2 == "شدید":
                level2 = 'level3'
            elif level2 == "خیلی شدید":
                level2 = 'level4'
            elif level2 == "ندارد":
                level2 = 'none'
            if level3 == "-----":
                level3 = None
            elif level3 == "خفیف":
                level3 = 'level1'
            elif level3 == "متوسط":
                level3 = 'level2'
            elif level3 == "شدید":
                level3 = 'level3'
            elif level3 == "خیلی شدید":
                level3 = 'level4'
            elif level3 == "ندارد":
                level3 = 'none'
            if level4 == "-----":
                level4 = None
            elif level4 == "خفیف":
                level4 = 'level1'
            elif level4 == "متوسط":
                level4 = 'level2'
            elif level4 == "شدید":
                level4 = 'level3'
            elif level4 == "خیلی شدید":
                level4 = 'level4'
            elif level4 == "ندارد":
                level4 = 'none'
            address = row[29]
            if address == "-----":
                address = None
            residance_area = row[30]
            if residance_area == "-----":
                residance_area = None
            elif residance_area == "شهر صنعتی": 
                residance_area = 'industrial_city'
            elif residance_area == "راه آهن":
                residance_area = 'railway'
            elif residance_area == "شهرک گردو":
                residance_area = 'gerdo_town'
            elif residance_area == "شریعتی":
                residance_area = 'shariati'
            elif residance_area == "مسکن":
                residance_area = 'maskan'
            elif residance_area == "علم الهدی":
                residance_area = 'alamolhoda'
            elif residance_area == "رودکی":
                residance_area = 'rodaki'
            elif residance_area == "خرم":
                residance_area = 'khorram'
            elif residance_area == "حسین آباد":
                residance_area = 'hossein_abad'
            elif residance_area == "نظم آباد":
                residance_area = 'nazm_abad'
            elif residance_area == "کرهرود":
                residance_area = 'karahroud'
            elif residance_area == "جهان پناه":
                residance_area = 'jahan_panah'
            elif residance_area == "ملک":
                residance_area = 'malek'
            elif residance_area == "عباس آباد":
                residance_area = 'abbas_abad'
            elif residance_area == "شهرک ولی عصر":
                residance_area = 'valiasr_town'
            elif residance_area == "رباط میل":
                residance_area = 'robat_mil'
            elif residance_area == "بان":
                residance_area = 'ban'
            elif residance_area == "جهانگیری":
                residance_area = 'jahangiri'
            phone_number = row[31]
            if phone_number == "-----":
                phone_number = None

            home_phone_number = row[32]
            if home_phone_number == "-----":
                home_phone_number = None

            visit_day = row[33]
            if visit_day == "--":
                visit_day = None
            visit_month = row[34]
            if visit_month == "--":
                visit_month = None
            visit_year = row[35]
            if visit_year == "----":
                visit_year = None
            note = row[36]
            if note == "-----":
                note = None

            father_name = row[37]
            if father_name == "-----":
                father_name = None
            father_last_name = last_name
            mother_first_name = row[38]
            if mother_first_name == "-----":
                mother_first_name = None
            mother_last_name = row[39]
            if mother_last_name == "-----":
                mother_last_name = None
            father_job = row[40]
            if father_job == "-----":
                father_job = None
            mother_job = row[41]
            if mother_job == "-----":
                mother_job = None
            father_education = row[42]
            if father_education == "-----":
                father_education = None
            elif father_education == "بی سواد":
                father_education = "illiterate"
            elif father_education == "ابتدایی":
                father_education = "elementary"
            elif father_education == "متوسطه اول (سیکل)":
                father_education = "middle_school"
            elif father_education == "متوسطه دوم (دیپلم)":
                father_education = "high_school"
            elif father_education == "کاردانی (فوق دیپلم)":
                father_education = "associate"
            elif father_education == "کارشناسی (لیسانس)":
                father_education = "bachelor"
            elif father_education == "کارشناسی ارشد (فوق لیسانس)":
                father_education = "master"
            elif father_education == "دکترا":
                father_education = "phd"
            elif father_education == "فوق دکترا":
                father_education = "post_doc"
            mother_education = row[43]
            if mother_education == "-----":
                mother_education = None
            elif mother_education == "بی سواد":
                mother_education = "illiterate"
            elif mother_education == "ابتدایی":
                mother_education = "elementary"
            elif mother_education == "متوسطه اول (سیکل)":
                mother_education = "middle_school"
            elif mother_education == "متوسطه دوم (دیپلم)":
                mother_education = "high_school"
            elif mother_education == "کاردانی (فوق دیپلم)":
                mother_education = "associate"
            elif mother_education == "کارشناسی (لیسانس)":
                mother_education = "bachelor"
            elif mother_education == "کارشناسی ارشد (فوق لیسانس)":
                mother_education = "master"
            elif mother_education == "دکترا":
                mother_education = "phd"
            elif mother_education == "فوق دکترا":
                mother_education = "post_doc"
            father_national_id = row[44]
            if father_national_id == "-----":
                father_national_id = None
            mother_national_id = row[45]
            if mother_national_id == "-----":
                mother_national_id = None
            live_situation = row[46]
            if live_situation == "-----":
                live_situation = None
            elif live_situation == "استیجاری":
                live_situation = 'rental'
            elif live_situation == "پدری":
                live_situation = 'paternal'
            elif live_situation == "منزل بستگان":
                live_situation = 'relatives'
            elif live_situation == "مسکن وقفی":
                live_situation = 'endowment'
            elif live_situation == "مسکن شخصی":
                live_situation = 'owned'
            elif live_situation == "بی خانمان":
                live_situation = 'homeless'
            elif live_situation == "ورثه ای":
                live_situation = 'inherited'
            elif live_situation == "منازل سازمانی":
                live_situation = 'org_housing'
            elif live_situation == "مرکز نگهداری":
                live_situation = 'care_center'
            morgage = row[47]
            if morgage == "-----":
                morgage = None
            rent = row[48]
            if rent == "-----":
                rent = None
            bank_card_number = row[49]
            if bank_card_number == "-----":
                bank_card_number = None
            bank_account_number = row[50]
            if bank_account_number == "-----":
                bank_account_number = None
            bank_shaba_number = row[51]
            if bank_shaba_number == "-----":
                bank_shaba_number = None
            husband_name = row[52]
            if husband_name == "-----":
                husband_first_name = None
                husband_last_name = None
            else:
                husband_list = husband_name.split(" ")
                husband_first_name = husband_list[0]
                if len(husband_list) > 1:
                    husband_last_name = husband_list[1]
            husband_national_id = row[53]
            if husband_national_id == "-----":
                husband_national_id = None
            husband_job = row[54]
            if husband_job == "-----":
                husband_job = None
            husband_education = row[55]
            if husband_education == "-----":
                husband_education = None
            elif husband_education == "بی سواد":
                husband_education = "illiterate"
            elif husband_education == "ابتدایی":
                husband_education = "elementary"
            elif husband_education == "متوسطه اول (سیکل)":
                husband_education = "middle_school"
            elif husband_education == "متوسطه دوم (دیپلم)":
                husband_education = "high_school"
            elif husband_education == "کاردانی (فوق دیپلم)":
                husband_education = "associate"
            elif husband_education == "کارشناسی (لیسانس)":
                husband_education = "bachelor"
            elif husband_education == "کارشناسی ارشد (فوق لیسانس)":
                husband_education = "master"
            elif husband_education == "دکترا":
                husband_education = "phd"
            elif husband_education == "فوق دکترا":
                husband_education = "post_doc"
            children_count = row[56]
            if children_count == -100:
                children_count = None
            child1_name = row[57]
            if child1_name == "-----":
                child1_first_name = None
                child1_last_name = None
            else:
                child_list = child1_name.split(" ")
                child1_first_name = child_list[0]
                if len(child_list) > 1:
                    child1_last_name = child_list[1]
            child1_national_id = row[58]
            if child1_national_id == "-----":
                child1_national_id = None
            child1_education = row[59]
            if child1_education == "-----":
                child1_education = None
            elif child1_education == "بی سواد":
                child1_education = "illiterate"
            elif child1_education == "ابتدایی":
                child1_education = "elementary"
            elif child1_education == "متوسطه اول (سیکل)":
                child1_education = "middle_school"
            elif child1_education == "متوسطه دوم (دیپلم)":
                child1_education = "high_school"
            elif child1_education == "کاردانی (فوق دیپلم)":
                child1_education = "associate"
            elif child1_education == "کارشناسی (لیسانس)":
                child1_education = "bachelor"
            elif child1_education == "کارشناسی ارشد (فوق لیسانس)":
                child1_education = "master"
            elif child1_education == "دکترا":
                child1_education = "phd"
            elif child1_education == "فوق دکترا":
                child1_education = "post_doc"
            child1_description = row[60]
            if child1_description == "-----":
                child1_description = None
            child2_name = row[61]
            if child2_name == "-----":
                child2_first_name = None
                child2_last_name = None
            else:
                child_list = child2_name.split(" ")
                child2_first_name = child_list[0]
                if len(child_list) > 1:
                    child2_last_name = child_list[1]
            child2_national_id = row[62]
            if child2_national_id == "-----":
                child2_national_id = None
            child2_education = row[63]
            if child2_education == "-----":
                child2_education = None
            elif child2_education == "بی سواد":
                child2_education = "illiterate"
            elif child2_education == "ابتدایی":
                child2_education = "elementary"
            elif child2_education == "متوسطه اول (سیکل)":
                child2_education = "middle_school"
            elif child2_education == "متوسطه دوم (دیپلم)":
                child2_education = "high_school"
            elif child2_education == "کاردانی (فوق دیپلم)":
                child2_education = "associate"
            elif child2_education == "کارشناسی (لیسانس)":
                child2_education = "bachelor"                
            elif child2_education == "کارشناسی ارشد (فوق لیسانس)":
                child2_education = "master"
            elif child2_education == "دکترا":
                child2_education = "phd"
            elif child2_education == "فوق دکترا":
                child2_education = "post_doc"
            child2_description = row[64]
            if child2_description == "-----":
                child2_description = None
            child3_name = row[65]
            if child3_name == "-----":
                child3_first_name = None
                child3_last_name = None
            else:
                child_list = child3_name.split(" ")
                child3_first_name = child_list[0]
                if len(child_list) > 1:
                    child3_last_name = child_list[1]
            child3_national_id = row[66]
            if child3_national_id == "-----":
                child3_national_id = None
            child3_education = row[67]
            if child3_education == "-----":
                child3_education = None
            elif child3_education == "بی سواد":
                child3_education = "illiterate"
            elif child3_education == "ابتدایی":
                child3_education = "elementary"
            elif child3_education == "متوسطه اول (سیکل)":
                child3_education = "middle_school"
            elif child3_education == "متوسطه دوم (دیپلم)":
                child3_education = "high_school"
            elif child3_education == "کاردانی (فوق دیپلم)":
                child3_education = "associate"
            elif child3_education == "کارشناسی (لیسانس)":
                child3_education = "bachelor"
            elif child3_education == "کارشناسی ارشد (فوق لیسانس)":
                child3_education = "master"
            elif child3_education == "دکترا":
                child3_education = "phd"
            elif child3_education == "فوق دکترا":
                child3_education = "post_doc"
            child3_description = row[68]
            if child3_description == "-----":
                child3_description = None
            child4_name = row[69]
            if child4_name == "-----":
                child4_first_name = None
                child4_last_name = None
            else:
                child_list = child4_name.split(" ")
                child4_first_name = child_list[0]
                if len(child_list) > 1:
                    child4_last_name = child_list[1]
            child4_national_id = row[70]
            if child4_national_id == "-----":
                child4_national_id = None
            child4_education = row[71]
            if child4_education == "-----":
                child4_education = None
            elif child4_education == "بی سواد":
                child4_education = "illiterate"
            elif child4_education == "ابتدایی":
                child4_education = "elementary"
            elif child4_education == "متوسطه اول (سیکل)":
                child4_education = "middle_school"
            elif child4_education == "متوسطه دوم (دیپلم)":
                child4_education = "high_school"
            elif child4_education == "کاردانی (فوق دیپلم)":
                child4_education = "associate"
            elif child4_education == "کارشناسی (لیسانس)":
                child4_education = "bachelor"
            elif child4_education == "کارشناسی ارشد (فوق لیسانس)":
                child4_education = "master"
            elif child4_education == "دکترا":
                child4_education = "phd"
            elif child4_education == "فوق دکترا":
                child4_education = "post_doc"
            child4_description = row[72]
            if child4_description == "-----":
                child4_description = None
            child5_name = row[73]
            if child5_name == "-----":
                child5_first_name = None
                child5_last_name = None
            else:
                child_list = child5_name.split(" ")
                child5_first_name = child_list[0]
                if len(child_list) > 1:
                    child5_last_name = child_list[1]
            child5_national_id = row[74]
            if child5_national_id == "-----":
                child5_national_id = None
            child5_education = row[75]
            if child5_education == "-----":
                child5_education = None
            elif child5_education == "بی سواد":
                child5_education = "illiterate"
            elif child5_education == "ابتدایی":
                child5_education = "elementary"
            elif child5_education == "متوسطه اول (سیکل)":
                child5_education = "middle_school"
            elif child5_education == "متوسطه دوم (دیپلم)":
                child5_education = "high_school"
            elif child5_education == "کاردانی (فوق دیپلم)":
                child5_education = "associate"
            elif child5_education == "کارشناسی (لیسانس)":
                child5_education = "bachelor"
            elif child5_education == "کارشناسی ارشد (فوق لیسانس)":
                child5_education = "master"
            elif child5_education == "دکترا":
                child5_education = "phd"
            elif child5_education == "فوق دکترا":
                child5_education = "post_doc"
            child5_description = row[76]
            if child5_description == "-----":
                child5_description = None
            child6_name = row[77]
            if child6_name == "-----":
                child6_first_name = None
                child6_last_name = None
            else:
                child_list = child6_name.split(" ")
                child6_first_name = child_list[0]
                if len(child_list) > 1:
                    child6_last_name = child_list[1]
            child6_national_id = row[78]
            if child6_national_id == "-----":
                child6_national_id = None
            child6_education = row[79]
            if child6_education == "-----":
                child6_education = None
            elif child6_education == "بی سواد":
                child6_education = "illiterate"
            elif child6_education == "ابتدایی":
                child6_education = "elementary"
            elif child6_education == "متوسطه اول (سیکل)":
                child6_education = "middle_school"
            elif child6_education == "متوسطه دوم (دیپلم)":
                child6_education = "high_school"
            elif child6_education == "کاردانی (فوق دیپلم)":
                child6_education = "associate"
            elif child6_education == "کارشناسی (لیسانس)":
                child6_education = "bachelor"
            elif child6_education == "کارشناسی ارشد (فوق لیسانس)":
                child6_education = "master"
            elif child6_education == "دکترا":
                child6_education = "phd"
            elif child6_education == "فوق دکترا":
                child6_education = "post_doc"
            child6_description = row[80]
            if child6_description == "-----":
                child6_description = None
            child7_name = row[81]
            if child7_name == "-----":
                child7_first_name = None
                child7_last_name = None
            else:
                child_list = child7_name.split(" ")
                child7_first_name = child_list[0]
                if len(child_list) > 1:
                    child7_last_name = child_list[1]
            child7_national_id = row[82]
            if child7_national_id == "-----":
                child7_national_id = None
            child7_education = row[83]
            if child7_education == "-----":
                child7_education = None
            elif child7_education == "بی سواد":
                child7_education = "illiterate"
            elif child7_education == "ابتدایی":
                child7_education = "elementary"
            elif child7_education == "متوسطه اول (سیکل)":
                child7_education = "middle_school"
            elif child7_education == "متوسطه دوم (دیپلم)":
                child7_education = "high_school"
            elif child7_education == "کاردانی (فوق دیپلم)":
                child7_education = "associate"
            elif child7_education == "کارشناسی (لیسانس)":
                child7_education = "bachelor"
            elif child7_education == "کارشناسی ارشد (فوق لیسانس)":
                child7_education = "master"
            elif child7_education == "دکترا":
                child7_education = "phd"
            elif child7_education == "فوق دکترا":
                child7_education = "post_doc"
            child7_description = row[90]
            if child7_description == "-----":
                child7_description = None

            brothers_count = row[86]
            if brothers_count == '--':
                brothers_count = None
                
            sisters_count = row[88]
            if sisters_count == '--':
                sisters_count = None

            rehab_skills = row[89]
            if rehab_skills == "":
                rehab_skills = None

            rehab_insurance_type = row[90]
            if rehab_insurance_type == "-----":
                rehab_insurance_type = None
            elif rehab_insurance_type == "خویش فرمایی":
                rehab_insurance_type = 'self'

            work_experience = row[91]
            if work_experience == "":
                work_experience = None
            dependents_count = row[92]
            if dependents_count == '---':
                dependents_count = None
            try:
                dependents_count = int(dependents_count)
            except:
                dependents_count = None




            




            case = Case.objects.create(
                first_name=row[1],
                last_name=row[2],
                national_id=row[3],
                gender=gender,
                birth_certificate_number=shenasnameh,
                date_of_birth=birthdate,
                birth_place=birth_place,
                education=education,
                field_of_study=education_field,
                insurance=bime,
                job=job,
                military_serveice=military,
                case_type=case_type,
                pension_status=pension,
                marrige_status=marriage,
                residencial_area=residance_area,
                address=address,
                home_phone_number=home_phone_number,
                phone_number=phone_number,
                housing_status=live_situation,
                bank_card_number=bank_card_number,
                bank_account_number=bank_account_number,
                bank_shaba_number=bank_shaba_number,
                house_mortgage=morgage,
                house_rent=rent,
                children_count=children_count,
                brothers_count=brothers_count,
                sisters_count=sisters_count,
                dependents_count=dependents_count,

                
            )
            if father_name and father_last_name:
                father_model = CaseFamilyMembers.objects.create(
                    case=case,
                    relation="father",
                    first_name=father_name,
                    last_name=father_last_name,
                    national_id=father_national_id,
                    education=father_education,
                    job=father_job,
                )
            if mother_first_name and mother_last_name:
                mother_model = CaseFamilyMembers.objects.create(
                    case=case,
                    relation="mother",
                    first_name=mother_first_name,
                    last_name=mother_last_name,
                    national_id=mother_national_id,
                    education=mother_education,
                    job=mother_job,
                )
            if husband_first_name:
                husband_model = CaseFamilyMembers.objects.create(
                    case=case,
                    relation="husband",
                    first_name=husband_first_name,
                    last_name=husband_last_name,
                    national_id=husband_national_id,
                    education=husband_education,
                    job=husband_job,
                )
            if child1_first_name:
                child1_model = CaseFamilyMembers.objects.create(
                    case=case,
                    relation="son",
                    first_name=child1_first_name,
                    last_name=child1_last_name,
                    national_id=child1_national_id,
                    education=child1_education,
                    description=child1_description,
                )
            if child2_first_name:
                child2_model = CaseFamilyMembers.objects.create(
                    case=case,
                    relation="son",
                    first_name=child2_first_name,
                    last_name=child2_last_name,
                    national_id=child2_national_id,
                    education=child2_education,
                    description=child2_description,
                )
            if child3_first_name:
                child3_model = CaseFamilyMembers.objects.create(
                    case=case,
                    relation="son",
                    first_name=child3_first_name,
                    last_name=child3_last_name,
                    national_id=child3_national_id,
                    education=child3_education,
                    description=child3_description,
                )
            if child4_first_name:
                child4_model = CaseFamilyMembers.objects.create(
                    case=case,
                    relation="son",
                    first_name=child4_first_name,
                    last_name=child4_last_name,
                    national_id=child4_national_id,
                    education=child4_education,
                    description=child4_description,
                )
            if child5_first_name:
                child5_model = CaseFamilyMembers.objects.create(
                    case=case,
                    relation="son",
                    first_name=child5_first_name,
                    last_name=child5_last_name,
                    national_id=child5_national_id,
                    education=child5_education,
                    description=child5_description,
                )
            if child6_first_name:
                child6_model = CaseFamilyMembers.objects.create(
                    case=case,
                    relation="son",
                    first_name=child6_first_name,
                    last_name=child6_last_name,
                    national_id=child6_national_id,
                    education=child6_education,
                    description=child6_description,
                )
            if child7_first_name:
                child7_model = CaseFamilyMembers.objects.create(
                    case=case,
                    relation="son",
                    first_name=child7_first_name,
                    last_name=child7_last_name,
                    national_id=child7_national_id,
                    education=child7_education,
                    description=child7_description,
                )


            if ejtemaie_reson:
                social_model = ReasonCase.objects.create(
                    case=case,
                    reason=ejtemaie_reson,
                )
            if recovered_reason:
                recovered_model = RecoveredReasonCase.objects.create(
                    case=case,
                    reason=recovered_reason,
                    skill=rehab_skills,
                    work_experience=work_experience,
                    insurance_type=rehab_insurance_type,
                )
            if illness1 and level1:
                illness_model1 = Disability.objects.create(
                    case=case,
                    disability_type=illness1,
                    disability_level=level1,
                )
            if illness2 and level2:
                illness_model2 = Disability.objects.create(
                    case=case,
                    disability_type=illness2,
                    disability_level=level2,
                )
            if illness3 and level3:
                illness_model3 = Disability.objects.create(
                    case=case,
                    disability_type=illness3,
                    disability_level=level3,
                )
            if illness4 and level4:
                illness_model4 = Disability.objects.create(
                    case=case,
                    disability_type=illness4,
                    disability_level=level4,
                )
            if visit_day and visit_month and visit_year:
                visit_model = Visit.objects.create(
                    case=case,
                    visit_date=f"{visit_year}-{visit_month}-{visit_day}",
                )               
            if note:
                note_model = CaseNotes.objects.create(
                    case=case,
                    note=note,
                    added_by=None,
                )
            
                
        conn.close()


        print(f"An error occurred: ")


from django.core.files import File

def upload():
        import os
        import sqlite3
        CaseDocuments.objects.all().delete()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, 'db.sqlite3')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cases_cases_model;")
        rows = cursor.fetchall()
        counter = 0
        for row in rows:
            if row[2] == "":
                continue

            expire_day = row[4]
            expire_month = row[5]
            expire_year = row[7]
            if expire_year == 0:
                expire_date = None
            else:
                expire_date = f"{expire_year}-{expire_month}-{expire_day}"
            expire_duration = row[6]
            if expire_duration == 0:
                expire_duration = None
            else:
                expire_duration = float(expire_duration)
            national_id = row[3]
            try:
                case = Case.objects.get(national_id=national_id)
            except:
                print(f"case {national_id} not found")
                continue
            counter += 1
            file_path = os.path.join(base_dir,'media', row[1])
            print('uploading file {file_path}')
            doc_type = row[2]
            if doc_type == "کمیسیون":
                doc_type = "commition"
            elif doc_type == "تعیین نیاز":
                doc_type = "needs_form"
            elif doc_type == "1_شناسنامه" or doc_type == "شناسنامه":
                doc_type = "birt_certificat"
            elif doc_type == "کارت معلولیت":
                doc_type = "disabiliti_card"
            elif doc_type == "1_کارت ملی" or doc_type == "کارت ملی":
                doc_type = "national_id"
            elif doc_type == "مدارک بانکی":
                doc_type = "bank"
            elif doc_type == "کارت پایان خدمت":
                doc_type = "military_serveice"
            elif doc_type == "عکس 3x4":
                doc_type = "pic3x4"
            elif doc_type == "لوازم توانبخشی":
                doc_type = "rehab_tools"
            elif doc_type == "کارت معافيت از خدمت" or doc_type == "کارت معافیت از خدمت":
                doc_type = "military_exemtion"
            elif doc_type == "کارت اقامت اتباع خارجي":
                doc_type = "foreign_national_id"
            elif doc_type == "بيمه" or doc_type == "بیمه":
                doc_type = "insurance"
            elif doc_type == "2_طلاق نامه" or doc_type == "3_طلاق نامه" or doc_type == "طلاق نامه" or doc_type == '1_طلاق نامه':
                doc_type = "divorce_id"
            elif doc_type == "گواهي فوت":
                doc_type = "death_certificate"
            elif doc_type == "1_مدارک فرزندان" or doc_type == "مدارک فرزندان":
                doc_type = "children_docs"
            elif doc_type == "گواهي مهارت" or doc_type == "گواهی مهارت":
                doc_type = "skill_certificate"
            else:
                doc_type = "other"

            if counter > 300:
                break
            with open(file_path, 'rb') as f:
                print(f"uploading {file_path}")
                file = File(f)
                CaseDocuments.objects.create(
                    case=case,
                    picture=file,
                    doc_type=doc_type,
                    date=expire_date,
                    expiry_date=None,
                    expiry_diuration=expire_duration,
                )
                print(f"uploaded {file_path}")
 
        print("Done")

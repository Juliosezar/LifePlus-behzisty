import requests
from pathlib import Path
from langchain_openai import ChatOpenAI
from django.conf import settings


REPORT_GENERATION_PROMPT = """تو یک کارشناس امور اجتماعی سازمان بهزیستی هستی. وظیفه تو نوشتن گزارش بازدید منزل مددجو به صورت رسمی و اداری است.

گزارش باید دقیقاً طبق ساختار زیر نوشته شود و لحن آن رسمی، اداری و مطابق با استانداردهای گزارش‌نویسی مددکاری اجتماعی باشد.

ساختار گزارش - این عناوین را دقیقاً به همین شکل بنویس:

اطلاعات هویتی:
اطلاعات شخصی مددجو شامل نام، نام خانوادگی، نام پدر، شماره شناسنامه، کد ملی، تاریخ تولد، محل تولد، جنسیت، میزان تحصیلات، رشته تحصیلی، آدرس و شماره تماس را بنویس. این بخش را به صورت توصیفی و در قالب جملات بنویس نه لیست.

وضعیت اجتماعی:
وضعیت اجتماعی مددجو شامل وضعیت تاهل، نوع معلولیت (در صورت وجود)، سطح معلولیت، علت تشکیل پرونده، وضعیت مستمری و وضعیت سربازی را شرح بده.

وضعیت خانوادگی:
اطلاعات خانواده مددجو شامل تعداد فرزندان، تعداد افراد تحت تکفل، اعضای خانواده (پدر، مادر، همسر، فرزندان و...) با ذکر نام، تحصیلات و شغل هر کدام را بنویس.

وضعیت اقتصادی:
وضعیت اقتصادی مددجو شامل شغل، منبع درآمد، میزان درآمد، وضعیت بیمه را شرح بده. اگر شغل و درآمدی ندارد ذکر کن.

وضعیت مسکن:
وضعیت مسکن مددجو شامل نوع مسکن (شخصی، اجاره‌ای، پدری و...)، متراژ، تعداد اتاق، امکانات رفاهی و بهداشتی را شرح بده. اگر اجاره‌ای است مبلغ رهن و اجاره را ذکر کن.

اقدامات انجام شده:
خدماتی که قبلاً به مددجو ارائه شده را لیست کن (شماره‌گذاری کن: 1-، 2-، 3-).

مشکلات:
مشکلات اصلی مددجو و خانواده‌اش را لیست کن (شماره‌گذاری کن).

نقاط قوت:
نقاط قوت مددجو و خانواده‌اش را لیست کن (شماره‌گذاری کن).

نقاط ضعف:
نقاط ضعف و کمبودهای مددجو را لیست کن (شماره‌گذاری کن).

برنامه اقدام و پیشنهادات:
پیشنهادات و برنامه اقدام برای بهبود وضعیت مددجو را لیست کن (شماره‌گذاری کن).

نکات بسیار مهم:
- تمام متن باید به فارسی باشد
- از لحن رسمی و اداری استفاده کن
- از اعداد فارسی استفاده نکن، از اعداد انگلیسی استفاده کن
- اطلاعاتی که در پایگاه داده موجود نیست را حدس نزن، فقط از اطلاعات ارائه شده استفاده کن
- مشکلات، نقاط قوت، نقاط ضعف و پیشنهادات را از اطلاعاتی که کاربر وارد کرده استخراج کن
- بخش‌هایی که اطلاعاتی برایشان موجود نیست را حذف کن
- هرگز از "بخش اول" یا "بخش دوم" و امثال آن استفاده نکن، فقط عنوان بخش را بنویس (مثلاً فقط "اطلاعات هویتی:" نه "بخش اول - اطلاعات هویتی:")
- هرگز از علامت‌های markdown مثل ## یا ** یا ``` استفاده نکن
- بین بخش‌ها فقط یک خط خالی بگذار، نه بیشتر. از خطوط خالی متعدد پرهیز کن
- متن باید مستقیماً قابل کپی در فایل Word باشد"""


def generate_report(case_data: dict, user_input: str) -> str:
    """Generate a visit report by merging case data from DB with user observations."""
    llm = ChatOpenAI(
        model=settings.NINEROUTER_MODEL,
        openai_api_key=settings.NINEROUTER_API_KEY,
        openai_api_base=settings.NINEROUTER_BASE_URL,
        temperature=0.3,
        max_tokens=5000,
        request_timeout=120,
    )

    case_info = _format_case_data(case_data)
    
    prompt = f"""{REPORT_GENERATION_PROMPT}

=== اطلاعات مددجو از پایگاه داده ===
{case_info}

=== توضیحات و مشاهدات کارشناس (کاربر) ===
{user_input}

حالا گزارش بازدید منزل را بر اساس اطلاعات بالا بنویس:"""

    response = llm.invoke(prompt)
    
    if isinstance(response, str):
        return response.strip()
    elif hasattr(response, 'content'):
        return response.content.strip()
    else:
        return str(response).strip()


def _format_case_data(data: dict) -> str:
    """Convert case data dict into a readable Persian text block for the prompt."""
    lines = []
    
    # Identity
    lines.append(f"نام: {data.get('first_name', '')} {data.get('last_name', '')}")
    lines.append(f"نام پدر: {data.get('father_name', '-')}")
    lines.append(f"کد ملی: {data.get('national_id', '')}")
    lines.append(f"شماره شناسنامه: {data.get('birth_certificate_number', '-')}")
    lines.append(f"تاریخ تولد: {data.get('date_of_birth', '-')}")
    lines.append(f"محل تولد: {data.get('birth_place', '-')}")
    lines.append(f"جنسیت: {data.get('gender', '-')}")
    lines.append(f"تحصیلات: {data.get('education', '-')}")
    lines.append(f"رشته تحصیلی: {data.get('field_of_study', '-')}")
    lines.append(f"وضعیت تاهل: {data.get('marriage_status', '-')}")
    lines.append(f"وضعیت سربازی: {data.get('military_service', '-')}")
    lines.append(f"شغل: {data.get('job', '-')}")
    lines.append(f"شماره تماس: {data.get('phone_number', '-')}")
    lines.append(f"تلفن ثابت: {data.get('home_phone_number', '-')}")
    lines.append(f"نوع پرونده: {data.get('case_type', '-')}")
    lines.append(f"وضعیت مستمری: {data.get('pension_status', '-')}")
    
    # Housing
    lines.append(f"وضعیت مسکن: {data.get('housing_status', '-')}")
    if data.get('house_mortgage'):
        lines.append(f"مبلغ رهن: {data['house_mortgage']} تومان")
    if data.get('house_rent'):
        lines.append(f"مبلغ اجاره: {data['house_rent']} تومان")
    lines.append(f"منطقه مسکونی: {data.get('residential_area', '-')}")
    lines.append(f"آدرس: {data.get('address', '-')}")
    lines.append(f"متراژ آپارتمان: {data.get('apartment_area', '-')}")
    lines.append(f"نوع ساختمان: {data.get('building_type', '-')}")
    lines.append(f"تعداد اتاق: {data.get('room_count', '-')}")
    
    # Insurance
    lines.append(f"وضعیت بیمه: {data.get('insurance', '-')}")
    
    # Family counts
    lines.append(f"تعداد فرزندان: {data.get('children_count', '-')}")
    lines.append(f"تعداد افراد تحت تکفل: {data.get('dependents_count', '-')}")
    lines.append(f"تعداد برادران: {data.get('brothers_count', '-')}")
    lines.append(f"تعداد خواهران: {data.get('sisters_count', '-')}")
    
    # Disabilities
    disabilities = data.get('disabilities', [])
    if disabilities:
        lines.append("\nمعلولیت‌ها:")
        for d in disabilities:
            lines.append(f"  - {d['type']} ({d['level']})")
    
    # Reasons
    reasons = data.get('reasons', [])
    if reasons:
        lines.append(f"\nعلت تشکیل پرونده: {', '.join(reasons)}")
    
    # Recovered reasons
    recovered = data.get('recovered_reasons', [])
    if recovered:
        lines.append(f"\nاطلاعات بهبودی: {'، '.join(recovered)}")
    
    # Family members
    family = data.get('family_members', [])
    if family:
        lines.append("\nاعضای خانواده:")
        for m in family:
            desc = f"{m['relation']}: {m.get('name', '-')}"
            if m.get('education'):
                desc += f" | تحصیلات: {m['education']}"
            if m.get('job'):
                desc += f" | شغل: {m['job']}"
            if m.get('description'):
                desc += f" | توضیحات: {m['description']}"
            lines.append(f"  - {desc}")
    
    # Services provided
    services = data.get('services_provided', [])
    if services:
        lines.append("\nخدمات ارائه شده:")
        for s in services:
            lines.append(f"  - {s}")
    
    # Demands
    demands = data.get('demands', [])
    if demands:
        lines.append("\nدرخواست‌ها:")
        for d in demands:
            lines.append(f"  - {d}")
    
    # Notes
    notes = data.get('notes', [])
    if notes:
        lines.append("\nیادداشت‌های قبلی:")
        for n in notes:
            lines.append(f"  - {n}")

    return "\n".join(lines)


def transcribe_audio(file_path: str) -> str:
    """Transcribe audio via 9router Gemini STT with fallback."""
    API_URL = "https://9router.jsezar.ir/v1/audio/transcriptions"
    api_key = settings.NINEROUTER_API_KEY
    
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    models = ["gemini/gemini-2.5-flash", "gemini/gemini-2.5-flash-lite"]
    last_error = None

    for model in models:
        try:
            with open(path, "rb") as f:
                resp = requests.post(
                    API_URL,
                    headers={"Authorization": f"Bearer {api_key}"},
                    files={"file": (path.name, f)},
                    data={"model": model},
                    timeout=120,
                )
            resp.raise_for_status()
            return resp.json().get("text", "")
        except Exception as e:
            last_error = e
            continue

    raise last_error

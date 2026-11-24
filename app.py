import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go

# -------------------------------------------------
# تنظیمات صفحه
# -------------------------------------------------
st.set_page_config(
    page_title="خبر ماهور | دفتر فنی مهندسی و مشاوره کشاورزی ماهور",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# استایل سفارشی
# -------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #f4f6f5; }
    [data-testid="stSidebar"] {
        background-color: #1a3c34;
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    .main-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a3c34;
        margin-bottom: 0.3rem;
    }
    .sub-title {
        color: #555;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    .card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
        border-right: 4px solid #1a3c34;
    }
    .ad-official {
        border-right: 4px solid #c0392b;
        background: #fff5f5;
    }
    .ad-business {
        border-right: 4px solid #2980b9;
    }
    .ad-charity {
        border-right: 4px solid #27ae60;
        background: #f0fff4;
    }
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1a3c34;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #1a3c34;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# داده‌های نمونه (بعداً می‌توانید از دیتابیس یا گوگل شیت بخوانید)
# -------------------------------------------------
def get_weather():
    return {
        "temp": 12.1,
        "feels_like": 11.7,
        "humidity": 86,
        "et0": 2.7,
        "rain_prob": 0,
        "wind": 3,
        "wind_dir": "جنوب‌شرقی",
        "condition": "صاف و آفتابی",
        "min_temp": 9,
        "max_temp": 25,
        "location": "بابامنیر / ماهور",
        "date": "سه‌شنبه ۳ آذر ۱۴۰۵",
        "time": "۲۰:۱۵"
    }

def get_official_ads():
    return [
        {
            "title": "توزیع کود شیمیایی",
            "org": "جهاد کشاورزی ماهورمیلاتی",
            "text": "توزیع کود اوره و فسفات از روز شنبه به مدت ۵ روز در محل انبار جهاد انجام می‌شود. کشاورزان با کارت ملی مراجعه کنند.",
            "date": "۲ آذر ۱۴۰۵",
            "priority": 1
        },
        {
            "title": "پرداخت وام قرض‌الحسنه",
            "org": "کمیته امداد امام خمینی",
            "text": "ثبت‌نام وام‌های ضروری و اشتغال‌زایی از هفته آینده آغاز می‌شود. مدارک لازم: شناسنامه، کارت ملی و مدارک شغلی.",
            "date": "۱ آذر ۱۴۰۵",
            "priority": 1
        },
    ]

def get_business_ads():
    return [
        {
            "title": "قهوه‌چی ماهور",
            "text": "فروش قهوه تازه و دم‌کرده، صبحانه محلی و میان‌وعده. روبروی میدان اصلی بابامنیر. تخفیف ویژه کشاورزان.",
            "contact": "۰۹۱۷xxxxxxx",
            "date": "۳ آذر"
        },
        {
            "title": "فروشگاه نهاده‌های کشاورزی رضایی",
            "text": "کود، سم، بذر و قطعات تراکتور موجود است. قیمت مناسب و ارسال به روستاهای اطراف.",
            "contact": "۰۹۱۸xxxxxxx",
            "date": "۲ آذر"
        },
    ]

def get_charity_items():
    return [
        {
            "title": "لباس زمستانی بچه‌گانه",
            "text": "چند دست لباس گرم بچه‌گانه سایز ۶ تا ۱۰ سال آماده اهدا به نیازمندان.",
            "status": "آماده تحویل",
            "contact": "از طریق دفتر فنی"
        },
        {
            "title": "درخواست بخاری نفتی",
            "text": "یک خانواده نیازمند به بخاری نفتی سالم احتیاج دارد.",
            "status": "درخواست",
            "contact": "از طریق دفتر فنی"
        },
    ]

def get_local_jobs():
    return [
        {
            "title": "نیاز به تراکتور برای شخم",
            "type": "درخواست",
            "text": "حدود ۲ هکتار زمین آبی برای شخم پاییزه. محدوده بابامنیر.",
            "contact": "۰۹۱۷xxxxxxx"
        },
        {
            "title": "انجام خدمات اینترنتی و ثبت‌نام",
            "type": "پیشنهاد کار",
            "text": "انجام ثبت‌نام‌های اینترنتی، پیگیری وام، کار با سامانه‌های دولتی و طراحی ساده.",
            "contact": "۰۹۱۸xxxxxxx"
        },
        {
            "title": "کارگر فصلی برای برداشت",
            "type": "درخواست",
            "text": "نیاز به ۲ نفر کارگر برای چند روز کار در باغ.",
            "contact": "از طریق دفتر"
        },
    ]

# -------------------------------------------------
# صفحات مختلف
# -------------------------------------------------
def page_home(weather):
    st.markdown('<div class="main-title">دفتر فنی مهندسی و مشاوره کشاورزی ماهور</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">زیر نظر مهندس افشین دهقان | بابامنیر - ماهورمیلاتی</div>', unsafe_allow_html=True)

    # ردیف متریک‌های هواشناسی
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("ET₀", f"{weather['et0']} mm")
    c2.metric("احتمال بارش", f"{weather['rain_prob']}%")
    c3.metric("رطوبت", f"{weather['humidity']}%")
    c4.metric("حداقل / حداکثر", f"{weather['min_temp']} / {weather['max_temp']}°C")
    c5.metric("دمای فعلی", f"{weather['temp']}°C", delta=f"احساس {weather['feels_like']}°C")

    st.info(f"وضعیت فعلی: {weather['condition']} | باد: {weather['wind']} km/h از {weather['wind_dir']} | {weather['date']} - {weather['time']}")

    # سه ستون اصلی
    left, center, right = st.columns([1.1, 1.4, 1.1])

    # ---------- ستون راست: اطلاع‌رسانی و تبلیغات ----------
    with right:
        st.markdown('<div class="section-header">📢 اطلاع‌رسانی و تبلیغات</div>', unsafe_allow_html=True)

        st.markdown("#### اطلاعیه‌های رسمی")
        for ad in get_official_ads():
            st.markdown(f"""
            <div class="card ad-official">
                <strong>{ad['title']}</strong><br>
                <small>{ad['org']} | {ad['date']}</small>
                <p style="margin-top:8px; font-size:0.9rem;">{ad['text']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### تبلیغ کسب‌وکارهای محلی")
        for ad in get_business_ads():
            st.markdown(f"""
            <div class="card ad-business">
                <strong>{ad['title']}</strong><br>
                <small>{ad['date']}</small>
                <p style="margin-top:8px; font-size:0.9rem;">{ad['text']}</p>
                <small>تماس: {ad['contact']}</small>
            </div>
            """, unsafe_allow_html=True)

    # ---------- ستون وسط: دفتر فنی ----------
    with center:
        st.markdown('<div class="section-header">🏢 دفتر فنی مهندسی ماهور</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h4>خدمات دفتر فنی</h4>
            <ul>
                <li>مشاوره تخصصی کشاورزی و باغداری</li>
                <li>تهیه نقشه و طرح‌های فنی</li>
                <li>توصیه‌های کودی و آبیاری</li>
                <li>پیگیری مجوزها و تسهیلات</li>
                <li>آموزش‌های دوره‌ای کشاورزان</li>
            </ul>
            <p><strong>مهندس افشین دهقان</strong><br>
            تماس: ۰۹۱۷۴۸۰۸۷۵۵<br>
            ایتا و روبیکا: a.d3469@</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### آخرین توصیه‌های فنی")
        st.success("با توجه به ET₀ برابر ۲.۷ میلی‌متر و عدم بارش، آبیاری سبک باغات توصیه می‌شود.")
        st.warning("دمای شبانه به حدود ۹ درجه می‌رسد. مراقب سرمازدگی نهال‌های جوان باشید.")

        st.markdown("#### پیش‌بینی دمای ۷ روز آینده")
        days = ["۳ آذر", "۴ آذر", "۵ آذر", "۶ آذر", "۷ آذر", "۸ آذر", "۹ آذر"]
        max_t = [25, 25, 24, 25, 24, 23, 22]
        min_t = [9, 9, 8, 8, 8, 7, 10]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days, y=max_t, mode="lines+markers", name="حداکثر", line=dict(color="#e74c3c")))
        fig.add_trace(go.Scatter(x=days, y=min_t, mode="lines+markers", name="حداقل", line=dict(color="#3498db")))
        fig.update_layout(height=280, margin=dict(l=10, r=10, t=20, b=20), legend=dict(orientation="h"))
        st.plotly_chart(fig, use_container_width=True)

    # ---------- ستون چپ: خیریه + کاریابی ----------
    with left:
        st.markdown('<div class="section-header">🤝 صندوق خیریه و لوازم</div>', unsafe_allow_html=True)
        for item in get_charity_items():
            st.markdown(f"""
            <div class="card ad-charity">
                <strong>{item['title']}</strong><br>
                <small>{item['status']}</small>
                <p style="margin-top:6px; font-size:0.9rem;">{item['text']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">💼 کاریابی محلی</div>', unsafe_allow_html=True)
        for job in get_local_jobs():
            color = "#27ae60" if job["type"] == "پیشنهاد کار" else "#e67e22"
            st.markdown(f"""
            <div class="card" style="border-right:4px solid {color}">
                <strong>{job['title']}</strong><br>
                <small>{job['type']}</small>
                <p style="margin-top:6px; font-size:0.9rem;">{job['text']}</p>
                <small>{job['contact']}</small>
            </div>
            """, unsafe_allow_html=True)


def page_ads():
    st.header("📢 اطلاع‌رسانی و تبلیغات")
    st.info("در این بخش اطلاعیه‌های رسمی ارگان‌ها و تبلیغ کسب‌وکارهای محلی نمایش داده می‌شود. هر دو روز حداکثر ۲ تا ۳ آگهی جدید پذیرفته می‌شود.")
    
    tab1, tab2 = st.tabs(["اطلاعیه‌های رسمی", "تبلیغ کسب‌وکارها"])
    
    with tab1:
        for ad in get_official_ads():
            with st.expander(f"🔴 {ad['title']} — {ad['org']}", expanded=True):
                st.write(ad['text'])
                st.caption(f"تاریخ: {ad['date']}")
    
    with tab2:
        for ad in get_business_ads():
            with st.expander(f"🔵 {ad['title']}", expanded=True):
                st.write(ad['text'])
                st.caption(f"تماس: {ad['contact']} | {ad['date']}")


def page_charity():
    st.header("🤝 صندوق خیریه و لوازم")
    st.write("اگر وسیله، لباس یا کالایی برای اهدا دارید یا نیازمندی را می‌شناسید، از طریق دفتر فنی اطلاع دهید.")
    
    for item in get_charity_items():
        st.markdown(f"""
        <div class="card ad-charity">
            <strong>{item['title']}</strong> — {item['status']}<br>
            {item['text']}<br>
            <small>{item['contact']}</small>
        </div>
        """, unsafe_allow_html=True)


def page_jobs():
    st.header("💼 کاریابی محلی ماهور")
    st.write("درخواست کار، پیشنهاد خدمات و کارهای روستایی و اینترنتی در این بخش قرار می‌گیرد.")
    
    for job in get_local_jobs():
        st.markdown(f"""
        <div class="card">
            <strong>{job['title']}</strong> ({job['type']})<br>
            {job['text']}<br>
            <small>{job['contact']}</small>
        </div>
        """, unsafe_allow_html=True)


def page_weather(weather):
    st.header("🌤️ هواشناسی و توصیه‌های فنی")
    st.metric("دمای فعلی", f"{weather['temp']}°C")
    st.write(f"رطوبت: {weather['humidity']}% | ET₀: {weather['et0']} mm | باد: {weather['wind']} km/h")
    st.success("توصیه روز: با توجه به شرایط فعلی، آبیاری سبک و محافظت از نهال‌های جوان در برابر سرما پیشنهاد می‌شود.")


def page_about():
    st.header("🏢 درباره دفتر فنی ماهور")
    st.markdown("""
    **دفتر فنی مهندسی و مشاوره کشاورزی ماهور**  
    زیر نظر **مهندس افشین دهقان**

    این دفتر با هدف ارائه خدمات فنی، مشاوره‌ای و آموزشی به کشاورزان، باغداران و دامداران منطقه ماهورمیلاتی و بابامنیر راه‌اندازی شده است.

    **راه‌های ارتباطی:**
    - واتساپ: ۰۹۱۷۴۸۰۸۷۵۵
    - ایتا و روبیکا: a.d3469@
    """)

# -------------------------------------------------
# منوی کناری
# -------------------------------------------------
with st.sidebar:
    st.markdown("### 🌾 خبر ماهور")
    st.caption("دفتر فنی مهندسی و مشاوره کشاورزی ماهور")
    st.markdown("---")
    
    menu = st.radio(
        "منو",
        [
            "صفحه اصلی",
            "اطلاع‌رسانی و تبلیغات",
            "صندوق خیریه و لوازم",
            "کاریابی محلی",
            "هواشناسی و توصیه فنی",
            "درباره دفتر فنی"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.caption("تماس: ۰۹۱۷۴۸۰۸۷۵۵")
    st.caption("ایتا و روبیکا: a.d3469@")

# -------------------------------------------------
# مسیریابی
# -------------------------------------------------
weather = get_weather()

if menu == "صفحه اصلی":
    page_home(weather)
elif menu == "اطلاع‌رسانی و تبلیغات":
    page_ads()
elif menu == "صندوق خیریه و لوازم":
    page_charity()
elif menu == "کاریابی محلی":
    page_jobs()
elif menu == "هواشناسی و توصیه فنی":
    page_weather(weather)
elif menu == "درباره دفتر فنی":
    page_about()

import streamlit as st
import requests
import os
import streamlit as st

# إعداد السلة (سلة التسوق)
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'product_image' not in st.session_state:
    st.session_state.product_image = None

# --- واجهة الإدارة (للمشتري فقط) ---
st.sidebar.title("🛠️ لوحة تحكم المدير")
admin_pass = st.sidebar.text_input("كلمة السر", type="password")

if admin_pass == "1234":
    uploaded_file = st.sidebar.file_uploader("تغيير صورة المنتج", type=['jpg', 'png'])
    if uploaded_file:
        st.session_state.product_image = uploaded_file

# --- واجهة المتجر ---
st.title("🛒 متجر توفيق للخدمات")

# عرض الصورة إذا كانت موجودة
if st.session_state.product_image:
    st.image(st.session_state.product_image, use_container_width=True)
else:
    st.info("المدير لم يرفع صورة المنتج بعد")

# إضافة زر للسلة
if st.button("أضف إلى السلة 🛍️"):
    st.session_state.cart.append("منتج 1")
    st.success("تمت الإضافة للسلة!")

# عرض محتويات السلة
st.write(f"عدد المنتجات في السلة: {len(st.session_state.cart)}")
# --- إعدادات التليجرام ---
TELEGRAM_TOKEN = "8640762406:AAF540rnfipL54HSUIRZqODSsBcQjM2uybo"
CHAT_ID = "7055252264"

def send_telegram_msg(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def send_telegram_photo(photo_path, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(photo_path, 'rb') as photo:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"photo": photo})

st.set_page_config(page_title="متجر توفيق للخدمات", layout="centered")

st.markdown("<h1 style='text-align: center; color: #2E86C1;'>مرحبا بك في متجرك</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555;'>معاً لنطور التجارة في مدينتنا</h3>", unsafe_allow_html=True)
st.write("---")
st.write("---")
st.subheader("معرض المنتجات")

# --- قسم عرض المنتجات (الصور) ---
st.write("---")
st.subheader("معرض المنتجات")

# استخدم الرابط المباشر داخل st.image
st.image("https://i.ibb.co/27SxJFCY/IMG-20260621-230717-021.jpg", caption="منتج 1", use_container_width=True)

st.write("---")
with st.form("main_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("الاسم الكريم")
        phone = st.text_input("رقم الهاتف")
        insta = st.text_input("حساب الإنستغرام (اختياري)")
    with col2:
        wilaya = st.text_input("الولاية")
        trade_type = st.selectbox("نوع نشاطك", ["مواد غذائية", "حلويات ومملحات", "ألبسة", "أخرى"])
    
    payment_method = st.radio("وسيلة الدفع", ["بريدي موب (BaridiMob)", "الدفع عند الاستلام"])
    
    uploaded_file = None
    if payment_method == "بريدي موب (BaridiMob)":
        st.info("💡 قم بالتحويل إلى RIP: 007999999999999999 50")
        uploaded_file = st.file_uploader("ارفع صورة إيصال الدفع", type=['jpg', 'png'])
    else:
        st.success("سنتواصل معك لتأكيد الطلب والدفع عند الاستلام.")

    submit = st.form_submit_button("إطلاق المشروع")

    if submit:
        if not name or not phone:
            st.error("يرجى ملء الاسم ورقم الهاتف!")
        elif payment_method == "بريدي موب (BaridiMob)" and uploaded_file is None:
            st.error("يرجى رفع صورة إيصال الدفع!")
        else:
            with st.spinner('جاري إرسال طلبك...'):
                msg = (f"طلب جديد!\nالاسم: {name}\nالهاتف: {phone}\n"
                       f"الإنستغرام: {insta if insta else 'غير متوفر'}\n"
                       f"الولاية: {wilaya}\nالنشاط: {trade_type}\nالدفع: {payment_method}")
                send_telegram_msg(msg)
                
                if uploaded_file:
                    with open("receipt.jpg", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    send_telegram_photo("receipt.jpg", f"إيصال دفع من {name}")
                
                # الفقاعات عند النجاح
                st.balloons()
                st.success("تم إرسال طلبك بنجاح! شكراً لثقتكم.")

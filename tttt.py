import streamlit as st
import requests
import os

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

# نقسمو الصفحة لـ 3 أعمدة باش الصور يجيوا مرتبين
col_img1, col_img2, col_img3 = st.columns(3)

with col_img1:
    st.image("IMG_20260621_230717_810.jpg", caption="منتج 1")
with col_img2:
    st.image("MG_20260621_230717_810.jpg", caption="منتج 2")
with col_img3:
    st.image("MG_20260621_230717_810.jpg", caption="منتج 3")

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

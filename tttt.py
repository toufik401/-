import streamlit as st
import requests
from fpdf import FPDF
import os

# --- إعدادات التليجرام ---
TELEGRAM_TOKEN = "8640762406:AAF540rnfipL54HSUIRZqODSsBcQjM2uybo"
CHAT_ID = "7055252264" # أزلنا حرف "ا"

def send_telegram_msg(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def send_telegram_photo(photo_path, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(photo_path, 'rb') as photo:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"photo": photo})

st.set_page_config(page_title="متجر توفيق للخدمات", layout="centered")

st.markdown("<h1 style='text-align: center; color: #2E86C1;'>مرحبا بك في متجرك</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>معا لنطور التجارة في مدينتنا</p>", unsafe_allow_html=True)

with st.form("main_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("الاسم الكريم")
        phone = st.text_input("رقم الهاتف")
        insta = st.text_input("حساب الإنستغرام")
    with col2:
        wilaya = st.text_input("الولاية")
        trade_type = st.selectbox("نوع نشاطك", ["مواد غذائية", "حلويات ومملحات", "ألبسة", "أخرى"])
    
    payment_method = st.radio("وسيلة الدفع", ["بريدي موب (BaridiMob)", "الدفع عند الاستلام"])
    
    uploaded_file = None
    if payment_method == "بريدي موب (BaridiMob)":
        st.info("💡 تحويل المبلغ إلى RIP: 007999999999999999 50")
        uploaded_file = st.file_uploader("ارفع صورة إيصال الدفع", type=['jpg', 'png'])

    submit = st.form_submit_button("إطلاق المشروع")

    if submit:
        if not name or not phone or not insta:
            st.error("يرجى ملء جميع البيانات!")
        else:
            with st.spinner('جاري إرسال طلبك...'):
                msg = f"طلب جديد!\nالاسم: {name}\nالهاتف: {phone}\nInsta: {insta}\nالولاية: {wilaya}\nالنشاط: {trade_type}\nالدفع: {payment_method}"
                send_telegram_msg(msg)
                
                if uploaded_file:
                    with open("receipt.jpg", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    send_telegram_photo("receipt.jpg", f"إيصال دفع من {name}")
                
                # إنشاء فاتورة بسيطة (بالفرنسية لتجنب مشاكل الخطوط)
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, txt="Facture - Tawfiq Dev", ln=True, align='C')
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=f"Client: {name} | Tel: {phone}", ln=True)
                pdf.cell(200, 10, txt=f"Instagram: {insta} | Wilaya: {wilaya}", ln=True)
                pdf.cell(200, 10, txt=f"Service: {trade_type}", ln=True)
                pdf.output("invoice.pdf")
                
                st.balloons()
                st.success("تم إرسال طلبك بنجاح!")
                with open("invoice.pdf", "rb") as f:
                    st.download_button("تحميل الفاتورة", f, file_name="invoice.pdf")

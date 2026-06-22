import streamlit as st
import requests

# إعدادات الصفحة
st.set_page_config(page_title="متجر توفيق", layout="centered")

# --- CSS للعنوان الذهبي ---
st.markdown("""
    <style>
    .gold-title { text-align: center; color: #D4AF37; border: 3px solid #D4AF37; 
                  padding: 10px; border-radius: 15px; background: #000; }
    </style>
    <div class='gold-title'><h1>✨ متجر توفيق للخدمات ✨</h1></div>
""", unsafe_allow_html=True)

# --- إعداد الحالة (الحفظ المؤقت) ---
if 'img' not in st.session_state: st.session_state.img = "https://i.ibb.co/27SxJFCY/IMG-20260621-230717-021.jpg"
if 'price' not in st.session_state: st.session_state.price = "1000"
if 'promo' not in st.session_state: st.session_state.promo = "لا يوجد"

# --- لوحة تحكم المدير ---
st.sidebar.title("🛠️ لوحة تحكم المدير")
pwd = st.sidebar.text_input("كلمة السر", type="password")
if pwd == "1234":
    st.session_state.img = st.sidebar.text_input("رابط الصورة", st.session_state.img)
    st.session_state.price = st.sidebar.text_input("السعر", st.session_state.price)
    st.session_state.promo = st.sidebar.text_input("عرض بروموسيو", st.session_state.promo)

# --- الواجهة الرئيسية ---
st.image(st.session_state.img, use_container_width=True)
st.subheader(f"السعر: {st.session_state.price} دج")
st.warning(f"📢 العرض: {st.session_state.promo}")

# --- نظام الفاتورة (طلب الزبون) ---
st.write("---")
st.subheader("📝 طلب فاتورة جديدة")
with st.form("invoice_form"):
    name = st.text_input("الاسم الكامل")
    phone = st.text_input("رقم الهاتف")
    qty = st.number_input("الكمية", min_value=1)
    
    submit = st.form_submit_button("إرسال الطلب (تليجرام)")
    
    if submit:
        if name and phone:
            msg = f"فاتورة جديدة!\nالاسم: {name}\nالهاتف: {phone}\nالكمية: {qty}\nالسعر: {st.session_state.price}"
            # ربط التليجرام
            token = "8640762406:AAF540rnfipL54HSUIRZqODSsBcQjM2uybo"
            chat_id = "7055252264"
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": msg})
            
            st.balloons()
            st.success("تم إرسال فاتورتك للمدير بنجاح!")
        else:
            st.error("يرجى ملء البيانات")

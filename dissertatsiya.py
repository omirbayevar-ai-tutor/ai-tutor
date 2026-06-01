import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Adaptiv AI-Tutor", page_icon="🧠", layout="wide")

st.title("🧠 Adaptiv AI-Tutor")
st.caption("Test versiyasi")

# ================== API KEY (To'g'ridan-to'g'ri yozamiz) ==================
API_KEY = "AIzaSy..."   # ← BU YERGA O'ZINGIZNING YANGI API KEY'INGIZNI QO'YING

if not API_KEY or API_KEY == "AQ.Ab8RN6IIhLCy-rSh224WhfxOEEnoNVcXTiRdDMgQLOv-NNoqcQ":
    st.error("API Key ni kodga yozing!")
    st.stop()

genai.configure(api_key=API_KEY)

# System Instruction
system_instruction = """
Siz informatika fani bo'yicha yordamchi o'qituvchisiz.
"""

try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )
    st.success("✅ Model muvaffaqiyatli yaratildi!")
except Exception as e:
    st.error(f"Model xatosi: {e}")
    st.stop()

# Oddiy test
user_input = st.chat_input("Savolingizni yozing...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Javob berilyapti..."):
            try:
                response = model.generate_content(user_input)
                st.write(response.text)
            except Exception as e:
                st.error(f"Xatolik: {e}")

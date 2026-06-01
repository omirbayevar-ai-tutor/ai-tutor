import streamlit as st
import google.generativeai as genai

# Sahifa sozlamalari
st.set_page_config(
    page_title="Adaptiv AI-Tutor",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Informatika darslari uchun Adaptiv AI-Tutor")
st.caption("O'quvchining bilim darajasi va psixologik tayyorgarligini diagnostika qiluvchi sun'iy intellekt tizimi")

# ================== API KEY ==================
if "GEMINI_API_KEY" not in st.secrets:
    st.error("GEMINI_API_KEY .streamlit/secrets.toml faylida topilmadi!")
    st.stop()

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"API Key xatosi: {e}")
    st.stop()

# System Instruction
system_instruction = """
Siz maktab o'quvchilari uchun informatika fani bo'yicha super-adaptiv va psixolog-mentorsiz.

Sizning vazifangiz:
- O'quvchining bilim darajasini aniqlash.
- Javobni shu darajaga moslashtirish.

... (qolgan qismini o'zingiznikini qoldiring)
"""

# Model (Yaxshiroq model tanlash)
try:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",          # yoki "gemini-1.5-flash" sinab ko'ring
        system_instruction=system_instruction
    )
except Exception as e:
    st.error(f"Model yaratishda xatolik: {e}")
    st.stop()

# Chat tarixi
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

col1, col2 = st.columns([3, 1])

# ================== O'QUVCHI OYNASI ==================
with col1:
    st.subheader("🤖 O'quvchi platformasi")

    # Oldingi suhbatni ko'rsatish
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Foydalanuvchi inputi
    user_input = st.chat_input("Informatika yoki dasturlash bo'yicha savolingizni yozing...")

    if user_input:
        # User xabarini qo'shish
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)

        # Javob generatsiya qilish
        with st.chat_message("assistant"):
            with st.spinner("O'ylayapman..."):
                try:
                    response = model.generate_content(user_input)
                    ai_response = response.text
                    
                    st.markdown(ai_response)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                    
                except Exception as e:
                    st.error(f"Xatolik: {str(e)}")

# ================== O'QITUVCHI MONITORI ==================
with col2:
    st.subheader("📊 O'qituvchi uchun Monitor")
    
    if st.session_state.chat_history:
        # Oxirgi AI javobini topish
        last_ai = next((msg["content"] for msg in reversed(st.session_state.chat_history) if msg["role"] == "assistant"), "")
        
        if "Tashxis" in last_ai or "Tahlil" in last_ai:
            st.success("📋 So'nggi pedagogik tahlil")
            st.markdown(last_ai)
        else:
            st.info("O'quvchi yetarli savol bermaguncha tahlil ko'rinmaydi.")
    else:
        st.write("Hali suhbat boshlanmagan...")

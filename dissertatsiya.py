import streamlit as st
import google.generativeai as genai

# Sahifa sozlamalari
st.set_page_config(
    page_title="Adaptiv AI-Tutor",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Informatika darslari uchun Adaptiv AI-Tutor")
st.caption(
    "O'quvchining bilim darajasi va psixologik tayyorgarligini "
    "diagnostika qiluvchi sun'iy intellekt tizimi"
)

# API kaliti
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)

# System Instruction
system_instruction = """
Siz maktab o'quvchilari uchun informatika fani bo'yicha super-adaptiv va psixolog-mentorsiz.

Sizning vazifangiz:
- O'quvchining bilim darajasini aniqlash.
- Javobni shu darajaga moslashtirish.

Darajalar:

1. Daraja: Past
- Juda sodda tushuntiring.
- Hayotiy misollar keltiring.
- Kod yozmang.
- Ruhlantiring.

2. Daraja: O'rta
- To'g'ridan-to'g'ri xatoni aytmang.
- O'ylantiruvchi savollar bering.

3. Daraja: Yuqori
- Murakkabroq misollar bering.
- Optimallashtirish usullarini ko'rsating.

Har bir javob oxirida:

Tashxis:
- Bilim darajasi
- Faollik
- Tavsiya

ko'rinishida qisqa tahlil yozing.
"""

# Model


# Streamlit secrets'dan kalitni yuklab olish
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API kaliti topilmadi! .streamlit/secrets.toml faylini tekshiring.")

# Modelni sozlash (Eslatma: Gemini-1.5-Flash modelidan foydalaning)
model = genai.GenerativeModel('gemini-1.5-flash')
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# Chat tarixi
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

col1, col2 = st.columns([2, 1])

# ---------------- O'QUVCHI OYNASI ----------------
with col1:
    st.subheader("🤖 O'quvchi platformasi")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input(
        "Informatika yoki dasturlash bo'yicha savolingizni yozing..."
    )

    if user_input:

        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            response = model.generate_content(user_input)

            ai_response = response.text

            with st.chat_message("assistant"):
                st.markdown(ai_response)

            st.session_state.chat_history.append(
                {"role": "assistant", "content": ai_response}
            )

        except Exception as e:
            st.error(f"Xatolik yuz berdi: {e}")

# ---------------- O'QITUVCHI MONITORI ----------------
with col2:
    st.subheader("📊 O'qituvchi uchun Monitor")

    if st.session_state.chat_history:

        last_ai = ""

        for msg in reversed(st.session_state.chat_history):
            if msg["role"] == "assistant":
                last_ai = msg["content"]
                break

        if "Tashxis" in last_ai:
            st.success("So'nggi pedagogik tahlil")
            st.write(last_ai.split("Tashxis")[-1])
        else:
            st.info(
                "Tizim o'quvchi faoliyatini tahlil qilmoqda."
            )

    else:
        st.write(
            "O'quvchi savol bergandan so'ng "
            "tahlil shu yerda ko'rsatiladi."
        )

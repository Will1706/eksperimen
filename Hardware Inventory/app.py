import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi API (Dapatkan API Key di Google AI Studio)
genai.configure(api_key="AIzaSyAZsYoYZ4VIspeyjt2iFiRIsl1p2DMdQYg")
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Tampilan UI
st.set_page_config(page_title="AI Dictionary", page_icon="📖")
st.title("📖 Kamus AI Pintar")
st.write("Masukkan kata atau benda yang ingin kamu ketahui!")

# 3. Logika Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Pengguna
if prompt := st.chat_input("Apa itu..."):
    # Simpan input user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon AI
    with st.chat_message("assistant"):
        # Instruksi khusus agar AI menjawab seperti kamus
        full_prompt = f"Berikan definisi singkat, jelas, dan akurat untuk: {prompt}. Format seperti kamus."
        response = model.generate_content(full_prompt)
        
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
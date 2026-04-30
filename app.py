import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate  # <-- Ini yang kita ubah!

# Load API Key dari file .env
load_dotenv()

# Konfigurasi Halaman Streamlit untuk UI Modern
st.set_page_config(page_title="DevMate AI", page_icon="💻", layout="wide")

# Kustomisasi CSS untuk tampilan Dark Mode
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stChatInput input {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💻 DevMate AI")
st.caption("Asisten Produktivitas Developer: Solusi Cepat untuk Debugging & Best Practice Code")
st.divider()

# Inisialisasi LLM
# Inisialisasi LLM
# Inisialisasi LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# Inisialisasi Session State bawaan Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat pesan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kolom Input Chat
user_input = st.chat_input("Tanya seputar error kode, arsitektur aplikasi, atau best practice...")

if user_input:
    # 1. Tampilkan pesan user di UI dan simpan ke memory
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Susun Riwayat Percakapan
    chat_history = ""
    for msg in st.session_state.messages[:-1]:
        role = "Developer" if msg["role"] == "user" else "DevMate AI"
        chat_history += f"{role}: {msg['content']}\n"

    # 3. Merancang Prompt Template
    template = """
    Kamu adalah DevMate AI, seorang asisten produktivitas developer senior. 
    Kamu ahli dalam pengembangan Full-Stack Web dan Mobile Engineering, khususnya menggunakan Laravel, Flutter, Kotlin, PHP, Tailwind CSS, JavaScript, dan Python.
    Gaya bahasamu santai, praktis, langsung pada intinya (straight to the point), dan selalu memberikan contoh kode yang efisien dan modern.
    Jangan memberikan jawaban bertele-tele.
    
    Riwayat Percakapan Sebelumnya:
    {history}
    
    Pertanyaan Developer Saat Ini: {input}
    Jawaban DevMate AI:
    """
    
    # 4. Format prompt
    prompt = PromptTemplate(input_variables=["history", "input"], template=template)
    formatted_prompt = prompt.format(history=chat_history, input=user_input)

    # 5. Dapatkan respon dari LLM dengan Error Handling
    with st.spinner("Memproses kode..."):
        try:
            response = llm.invoke(formatted_prompt).content
            
            # 6. Tampilkan respon bot dan simpan ke memory (Jika sukses)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
                
        except Exception as e:
            # Jika server Google sedang penuh, tampilkan peringatan ini
            st.warning("⚠️ Server AI sedang penuh (High Demand). Tunggu beberapa detik dan coba kirim ulang pertanyaanmu, ya!")
            with st.expander("Detail Error (Untuk Developer)"):
                st.error(e)
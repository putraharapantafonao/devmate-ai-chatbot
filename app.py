import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Load API Key
load_dotenv()

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="DevMate AI", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

# Kustomisasi CSS untuk UI Premium
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Background gradient for the main app */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #1a1b26 100%);
        color: #f8fafc;
    }

    /* Style for the chat input */
    .stChatInputContainer {
        border-radius: 12px;
        background-color: #1f2937 !important;
        border: 1px solid #374151 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Chat bubbles styling */
    [data-testid="stChatMessage"] {
        background-color: rgba(31, 41, 55, 0.4);
        border-radius: 10px;
        padding: 10px 15px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Custom divider */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: rgba(17, 24, 39, 0.95);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2809/2809336.png", width=60)
    st.title("DevMate AI")
    st.markdown("---")
    st.markdown("🤖 **AI Model:** Gemini 2.5 Flash")
    st.markdown("👨‍💻 **Role:** Senior Full-Stack Engineer")
    st.markdown("🎯 **Focus:** Clean Code & Best Practices")
    st.markdown("---")
    if st.button("🗑️ Hapus Percakapan", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("© 2026 DevMate AI - Your Pair Programming Partner")

# Header Area
col1, col2 = st.columns([1, 8])
with col1:
    st.markdown("<h1 style='text-align: right; margin-top:-15px;'>🚀</h1>", unsafe_allow_html=True)
with col2:
    st.markdown("<h1 style='margin-bottom:-10px;'>DevMate AI</h1>", unsafe_allow_html=True)
    st.caption("Asisten Produktivitas Developer: Solusi Cepat untuk Debugging & Best Practice Code")

st.divider()

# Inisialisasi LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# Inisialisasi Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan ucapan selamat datang jika belum ada pesan
if len(st.session_state.messages) == 0:
    st.info("👋 Halo! Saya DevMate AI. Ada masalah kode yang ingin diselesaikan hari ini? Silakan ketikkan pertanyaan di bawah.", icon="💡")

# Tampilkan riwayat pesan
for message in st.session_state.messages:
    avatar = "👨‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Kolom Input Chat
user_input = st.chat_input("Tanya seputar error kode, arsitektur aplikasi, atau best practice...")

if user_input:
    # 1. Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(user_input)

    # 2. Susun Riwayat Percakapan (batasi 10 pesan terakhir)
    chat_history = ""
    for msg in st.session_state.messages[-11:-1]:
        role = "Developer" if msg["role"] == "user" else "DevMate AI"
        chat_history += f"{role}: {msg['content']}\n"

    # 3. Merancang Prompt Template
    template = """
    Kamu adalah DevMate AI, seorang asisten produktivitas developer senior. 
    Kamu ahli dalam pengembangan Full-Stack Web dan Mobile Engineering (Laravel, Flutter, Kotlin, PHP, JS, Python, dll).
    Gaya bahasamu profesional namun santai, praktis, langsung pada intinya, dan selalu memberikan contoh kode yang efisien dan modern.
    Format responsmu menggunakan Markdown yang rapi (bold, lists, code blocks).
    
    Riwayat Percakapan Sebelumnya:
    {history}
    
    Pertanyaan Developer Saat Ini: {input}
    Jawaban DevMate AI:
    """
    
    prompt = PromptTemplate(input_variables=["history", "input"], template=template)
    formatted_prompt = prompt.format(history=chat_history, input=user_input)

    # 4. Request ke LLM
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Menganalisa kode & meracik solusi... ☕"):
            try:
                response = llm.invoke(formatted_prompt).content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error("⚠️ Ups, terjadi kesalahan atau server AI sedang penuh. Silakan coba lagi.", icon="🚨")
                with st.expander("Detail Error (Untuk Developer)"):
                    st.code(str(e))
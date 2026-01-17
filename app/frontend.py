"""
Frontend Streamlit para o Email Intelligence Classifier.
Interface moderna que replica o design original.
"""

import streamlit as st
import requests
from datetime import datetime
import time

# ============== Configuração da Página ==============

st.set_page_config(
    page_title="Email Intelligence",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============== CSS Customizado ==============

st.markdown("""
<style>
    /* Importar fonte */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    
    /* Reset e base */
    * {
        font-family: 'DM Sans', sans-serif;
    }
    
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Esconder elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Header customizado */
    .custom-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px 0;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 32px;
        background: white;
        margin: -1rem -1rem 2rem -1rem;
        padding: 16px 24px;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .header-icon {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 20px;
    }
    
    .header-title {
        font-size: 18px;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
        line-height: 1.2;
    }
    
    .header-subtitle {
        font-size: 13px;
        color: #64748b;
        margin: 0;
    }
    
    .ia-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 14px;
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border: 1px solid #6ee7b7;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        color: #059669;
    }
    
    .ia-badge::before {
        content: "✦";
    }
    
    /* Título da seção */
    .section-title {
        font-size: 28px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 8px;
    }
    
    .section-subtitle {
        font-size: 15px;
        color: #64748b;
        margin-bottom: 24px;
    }
    
    /* Card principal */
    .main-card {
        background: white;
        border: 2px dashed #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
    }
    
    /* Text area customizado */
    .stTextArea textarea {
        border: none !important;
        resize: none !important;
        font-size: 14px !important;
        color: #64748b !important;
        background: transparent !important;
    }
    
    .stTextArea textarea:focus {
        box-shadow: none !important;
    }
    
    /* Contador de caracteres */
    .char-counter {
        font-size: 13px;
        color: #94a3b8;
    }
    
    /* Botões */
    .upload-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 16px;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        color: #475569;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .upload-btn:hover {
        background: #f8fafc;
        border-color: #cbd5e1;
    }
    
    .classify-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 12px 24px;
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        border: none;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 600;
        color: white;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .classify-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(249, 115, 22, 0.4);
    }
    
    /* Estilizar botões do Streamlit */
    .stButton > button {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(249, 115, 22, 0.4) !important;
    }
    
    /* Histórico card */
    .history-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        height: 100%;
    }
    
    .history-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .history-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 16px;
        font-weight: 600;
        color: #1e293b;
    }
    
    .history-count {
        background: #e0f2fe;
        color: #0284c7;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .history-item {
        padding: 12px 0;
        border-bottom: 1px solid #f1f5f9;
        cursor: pointer;
        transition: background 0.2s;
    }
    
    .history-item:last-child {
        border-bottom: none;
    }
    
    .history-item:hover {
        background: #f8fafc;
        margin: 0 -12px;
        padding-left: 12px;
        padding-right: 12px;
        border-radius: 8px;
    }
    
    .history-item-title {
        font-size: 14px;
        font-weight: 500;
        color: #334155;
        margin-bottom: 6px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .history-item-meta {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 12px;
    }
    
    .badge-produtivo {
        color: #0d9488;
        font-weight: 600;
    }
    
    .badge-improdutivo {
        color: #f59e0b;
        font-weight: 600;
    }
    
    .history-score {
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 3px;
    }
    
    .history-date {
        color: #94a3b8;
    }
    
    /* Indicador de status */
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    
    .status-produtivo {
        background: #0d9488;
    }
    
    .status-improdutivo {
        background: #f59e0b;
    }
    
    /* Footer */
    .custom-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 0;
        margin-top: 40px;
        border-top: 1px solid #e2e8f0;
        font-size: 13px;
        color: #94a3b8;
    }
    
    .footer-left {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Resultado da classificação */
    .result-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-left: 4px solid;
    }
    
    .result-produtivo {
        border-left-color: #0d9488;
    }
    
    .result-improdutivo {
        border-left-color: #f59e0b;
    }
    
    .result-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
    }
    
    .result-classification {
        font-size: 20px;
        font-weight: 700;
    }
    
    .result-score {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 24px;
        font-weight: 700;
        color: #1e293b;
    }
    
    .result-confidence {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 16px;
    }
    
    .result-reply {
        background: #f8fafc;
        border-radius: 12px;
        padding: 16px;
        font-size: 14px;
        color: #475569;
        line-height: 1.6;
    }
    
    .result-reply-title {
        font-size: 12px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    /* File uploader */
    .stFileUploader {
        padding: 0 !important;
    }
    
    .stFileUploader > div {
        padding: 0 !important;
    }
    
    .stFileUploader label {
        display: none !important;
    }
    
    [data-testid="stFileUploader"] {
        padding: 0 !important;
    }
    
    [data-testid="stFileUploader"] section {
        padding: 0 !important;
    }
    
    [data-testid="stFileUploader"] section > div {
        padding: 0 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #f97316 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============== Estado da Sessão ==============

if 'history' not in st.session_state:
    st.session_state.history = []

if 'email_content' not in st.session_state:
    st.session_state.email_content = ""

if 'result' not in st.session_state:
    st.session_state.result = None

# ============== Funções ==============

import os

# URL da API - usa variável de ambiente ou localhost
API_URL = os.environ.get("API_URL", "http://localhost:8000/api/v1")

def classify_email(content: str) -> dict:
    """Chama a API para classificar o email."""
    try:
        response = requests.post(
            f"{API_URL}/classify-email",
            json={"email_content": content},
            timeout=60
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro na API: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Não foi possível conectar ao servidor. Certifique-se de que o backend está rodando.")
        return None
    except Exception as e:
        st.error(f"Erro: {str(e)}")
        return None

def get_history() -> list:
    """Busca histórico da API."""
    try:
        response = requests.get(f"{API_URL}/history", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return st.session_state.history

def clear_history():
    """Limpa o histórico."""
    try:
        requests.delete(f"{API_URL}/history", timeout=10)
        st.session_state.history = []
    except:
        pass

# ============== Header ==============

st.markdown("""
<div class="custom-header">
    <div class="header-left">
        <div class="header-icon">📧</div>
        <div>
            <p class="header-title">Email Intelligence</p>
            <p class="header-subtitle">Classificador Inteligente</p>
        </div>
    </div>
    <div class="ia-badge">IA Ativa</div>
</div>
""", unsafe_allow_html=True)

# ============== Layout Principal ==============

col1, col2 = st.columns([2.5, 1])

with col1:
    st.markdown('<h1 class="section-title">Classificador de Emails</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Cole o conteúdo do email ou faça upload de um arquivo para classificação automática.</p>', unsafe_allow_html=True)
    
    # Card principal
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # Inicializa o session state do input se houver conteúdo de arquivo
    if 'email_content' in st.session_state and st.session_state.email_content:
        st.session_state.email_input = st.session_state.email_content
        st.session_state.email_content = ""  # Limpa após usar
    
    # Inicializa a key se não existir
    if 'email_input' not in st.session_state:
        st.session_state.email_input = ""
    
    # Text area
    email_text = st.text_area(
        "Email",
        placeholder="Cole o texto do email aqui ou arraste um arquivo .txt ou .pdf...",
        height=200,
        key="email_input",
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Linha de ações
    col_upload, col_counter, col_btn = st.columns([1, 1.5, 1])
    
    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload",
            type=['txt', 'pdf'],
            label_visibility="collapsed",
            key="file_uploader"
        )
        
        if uploaded_file is not None:
            try:
                file_extension = uploaded_file.name.split('.')[-1].lower()
                content = None
                
                if file_extension == 'txt':
                    # Tenta diferentes encodings para TXT
                    raw_bytes = uploaded_file.read()
                    for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
                        try:
                            content = raw_bytes.decode(encoding)
                            break
                        except UnicodeDecodeError:
                            continue
                    if content is None:
                        content = raw_bytes.decode('utf-8', errors='ignore')
                
                elif file_extension == 'pdf':
                    # Extrai texto do PDF
                    try:
                        from PyPDF2 import PdfReader
                        pdf_reader = PdfReader(uploaded_file)
                        content = ""
                        for page in pdf_reader.pages:
                            text = page.extract_text()
                            if text:
                                content += text + "\n"
                    except ImportError:
                        st.error("❌ Biblioteca PyPDF2 não instalada.")
                        content = None
                
                if content and content.strip():
                    # Atualiza o session state - será copiado para email_input no próximo rerun
                    st.session_state.email_content = content.strip()
                    st.success(f"✅ Arquivo '{uploaded_file.name}' carregado com {len(content.strip())} caracteres!")
                    st.rerun()
                else:
                    st.warning("⚠️ O arquivo está vazio ou não foi possível extrair texto.")
                    
            except Exception as e:
                st.warning(f"❌ Não foi possível ler o arquivo: {str(e)}")
    
    with col_counter:
        char_count = len(email_text) if email_text else 0
        st.markdown(f'<p class="char-counter">{char_count} / 10 000 caracteres</p>', unsafe_allow_html=True)
    
    with col_btn:
        if st.button("Classificar Email", key="classify_btn", use_container_width=True):
            if email_text and email_text.strip():
                with st.spinner("Analisando email..."):
                    result = classify_email(email_text)
                    if result:
                        st.session_state.result = result
                        # Adiciona ao histórico local
                        history_item = {
                            "content": email_text[:50] + "..." if len(email_text) > 50 else email_text,
                            "classification": result["classification"],
                            "pontuation": result["pontuation"],
                            "confidence": result["confidence"],
                            "suggested_reply": result["suggested_reply"],
                            "timestamp": datetime.now().strftime("%d %b, %H:%M")
                        }
                        st.session_state.history.insert(0, history_item)
                        st.rerun()
            else:
                st.warning("⚠️ Por favor, insira o conteúdo do email.")
    
    # Resultado da classificação
    if st.session_state.result:
        result = st.session_state.result
        is_produtivo = result["classification"] == "Produtivo"
        
        result_class = "result-produtivo" if is_produtivo else "result-improdutivo"
        badge_class = "badge-produtivo" if is_produtivo else "badge-improdutivo"
        
        st.markdown(f"""
        <div class="result-card {result_class}">
            <div class="result-header">
                <div>
                    <span class="status-dot {'status-produtivo' if is_produtivo else 'status-improdutivo'}"></span>
                    <span class="result-classification {badge_class}">{result['classification']}</span>
                </div>
                <div class="result-score">
                    <span>⭐</span>
                    <span>{result['pontuation']}</span>
                    <span style="font-size: 14px; color: #94a3b8; font-weight: 400;">/10</span>
                </div>
            </div>
            <p class="result-confidence">Confiança: {result['confidence']*100:.0f}%</p>
            <div class="result-reply">
                <p class="result-reply-title">Resposta Sugerida</p>
                <p>{result['suggested_reply']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    # Buscar histórico da API
    api_history = get_history()
    if api_history:
        display_history = api_history
    else:
        display_history = st.session_state.history
    
    history_count = len(display_history)
    
    st.markdown(f"""
    <div class="history-card">
        <div class="history-header">
            <div class="history-title">
                <span>🕐</span>
                <span>Histórico</span>
                <span class="history-count">{history_count}</span>
            </div>
            <span style="cursor: pointer; color: #94a3b8;">🗑️</span>
        </div>
    """, unsafe_allow_html=True)
    
    if display_history:
        for item in display_history[:10]:  # Mostra apenas os 10 mais recentes
            # Verifica se é do formato da API ou local
            if isinstance(item, dict):
                if 'email_content' in item:
                    # Formato da API
                    title = item['email_content'][:45] + "..." if len(item['email_content']) > 45 else item['email_content']
                    classification = item['classification']
                    pontuation = item['pontuation']
                    timestamp = item.get('created_at', '')[:16].replace('T', ' ') if 'created_at' in item else ''
                else:
                    # Formato local
                    title = item.get('content', '')[:45]
                    classification = item.get('classification', '')
                    pontuation = item.get('pontuation', 0)
                    timestamp = item.get('timestamp', '')
                
                badge_class = "badge-produtivo" if classification == "Produtivo" else "badge-improdutivo"
                status_class = "status-produtivo" if classification == "Produtivo" else "status-improdutivo"
                
                st.markdown(f"""
                <div class="history-item">
                    <div style="display: flex; align-items: center;">
                        <span class="status-dot {status_class}"></span>
                        <p class="history-item-title">{title}</p>
                    </div>
                    <div class="history-item-meta">
                        <span class="{badge_class}">{classification}</span>
                        <span class="history-score">☆ {pontuation}</span>
                        <span class="history-date">{timestamp}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <p style="color: #94a3b8; font-size: 13px; text-align: center; padding: 20px 0;">
            Nenhum email classificado ainda.
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botão para limpar histórico (pequeno)
    if display_history:
        if st.button("🗑️ Limpar Histórico", key="clear_history", use_container_width=True):
            clear_history()
            st.session_state.result = None
            st.rerun()

# ============== Footer ==============

st.markdown("""
<div class="custom-footer">
    <div class="footer-left">
        <span>○</span>
        <span>Dados processados com segurança</span>
    </div>
    <div>© 2026 Email Intelligence Classifier. Todos os direitos reservados.</div>
</div>
""", unsafe_allow_html=True)


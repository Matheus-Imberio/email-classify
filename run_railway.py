"""
Script para rodar no Railway.
Inicia o backend FastAPI e frontend Streamlit em paralelo.
"""

import subprocess
import sys
import os
import time
from threading import Thread

def run_backend():
    """Inicia o servidor FastAPI."""
    port = os.environ.get("PORT", "8000")
    print(f"🚀 Iniciando Backend na porta {port}...")
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", port
    ])

def run_frontend():
    """Inicia o frontend Streamlit."""
    time.sleep(5)  # Aguarda backend iniciar
    streamlit_port = os.environ.get("STREAMLIT_PORT", "8501")
    print(f"🎨 Iniciando Frontend na porta {streamlit_port}...")
    subprocess.run([
        sys.executable, "-m", "streamlit",
        "run", "app/frontend.py",
        "--server.port", streamlit_port,
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ])

def main():
    print("=" * 50)
    print("📧 Email Intelligence - Railway Deploy")
    print("=" * 50)
    
    # Verifica se deve rodar só o backend ou ambos
    mode = os.environ.get("SERVICE_MODE", "backend")
    
    if mode == "frontend":
        # Modo frontend apenas
        run_frontend()
    elif mode == "both":
        # Roda ambos
        backend_thread = Thread(target=run_backend, daemon=True)
        backend_thread.start()
        run_frontend()
    else:
        # Modo backend apenas (padrão)
        run_backend()

if __name__ == "__main__":
    main()


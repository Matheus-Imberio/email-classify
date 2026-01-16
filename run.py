"""
Script para rodar o backend e frontend simultaneamente.
"""

import subprocess
import sys
import time
import os
from threading import Thread

def run_backend():
    """Inicia o servidor FastAPI."""
    print("🚀 Iniciando Backend (FastAPI) na porta 8000...")
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])

def run_frontend():
    """Inicia o frontend Streamlit."""
    # Aguarda o backend iniciar
    time.sleep(3)
    print("🎨 Iniciando Frontend (Streamlit) na porta 8501...")
    subprocess.run([
        sys.executable, "-m", "streamlit",
        "run", "app/frontend.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--browser.gatherUsageStats", "false"
    ])

def main():
    print("=" * 50)
    print("📧 Email Intelligence Classifier")
    print("=" * 50)
    print()
    print("Iniciando serviços...")
    print()
    
    # Cria threads para rodar ambos os serviços
    backend_thread = Thread(target=run_backend, daemon=True)
    frontend_thread = Thread(target=run_frontend, daemon=True)
    
    backend_thread.start()
    frontend_thread.start()
    
    print()
    print("✅ Serviços iniciados!")
    print()
    print("📡 Backend API:  http://localhost:8000")
    print("🎨 Frontend:     http://localhost:8501")
    print("📚 API Docs:     http://localhost:8000/docs")
    print()
    print("Pressione Ctrl+C para encerrar...")
    print()
    
    try:
        # Mantém o script rodando
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Encerrando serviços...")

if __name__ == "__main__":
    main()


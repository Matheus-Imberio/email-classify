"""
Script para rodar apenas o frontend Streamlit.
Útil quando o backend já está rodando em outro terminal.
"""

import subprocess
import sys

def main():
    print("🎨 Iniciando Frontend Streamlit...")
    print("📡 Certifique-se de que o backend está rodando em http://localhost:8000")
    print()
    
    subprocess.run([
        sys.executable, "-m", "streamlit",
        "run", "app/frontend.py",
        "--server.port", "8501",
        "--server.address", "localhost",
        "--browser.gatherUsageStats", "false"
    ])

if __name__ == "__main__":
    main()


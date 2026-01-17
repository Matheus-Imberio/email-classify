#!/bin/bash
# Script para iniciar o frontend Streamlit no Railway

PORT=${PORT:-8080}
echo "🎨 Iniciando Streamlit na porta $PORT..."

streamlit run app/frontend.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false


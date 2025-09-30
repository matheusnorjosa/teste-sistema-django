#!/bin/bash
# ===========================================
# SCRIPT DE FORMATA��O - APRENDER SISTEMA
# ===========================================
# Executa formata��o de c�digo no container Docker

set -e

echo "<� Executando formata��o de c�digo..."

# Executar isort para organizar imports
echo "=� Organizando imports com isort..."
./scripts/docker-run.sh isort .

# Executar Black para formata��o
echo "=� Formatando c�digo com Black..."
./scripts/docker-run.sh black .

echo " Formata��o conclu�da!"
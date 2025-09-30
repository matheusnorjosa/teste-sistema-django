#!/bin/bash
# ===========================================
# SCRIPT DE MIGRA��O - APRENDER SISTEMA
# ===========================================
# Executa migra��es Django no container Docker

set -e

echo "=� Executando migra��es Django..."

# Criar migra��es se necess�rio
echo "=� Verificando se h� novas migra��es..."
./scripts/docker-run.sh python manage.py makemigrations

# Aplicar migra��es
echo " Aplicando migra��es..."
./scripts/docker-run.sh python manage.py migrate

# Mostrar status das migra��es
echo "=� Status das migra��es:"
./scripts/docker-run.sh python manage.py showmigrations

echo " Migra��es conclu�das!"
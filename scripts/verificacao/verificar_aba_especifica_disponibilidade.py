#!/usr/bin/env python
"""
Verifica a aba específica da planilha de Disponibilidade pelo GID
"""

import os
import sys
import django
import gspread
from google.oauth2.credentials import Credentials

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aprender_sistema.settings')
django.setup()

def verificar_aba_especifica_disponibilidade():
    """Verifica a aba específica da planilha de Disponibilidade"""
    
    print("🔍 Verificando aba específica da planilha de Disponibilidade...")
    print("URL fornecida: https://docs.google.com/spreadsheets/d/1fsCeGUzsNCv0SCiE6mcIvcCHsMbqNeyzANwdU_148Vw/edit?gid=1510755488#gid=1510755488")
    
    # ID da planilha de Disponibilidade
    PLANILHA_DISPONIBILIDADE_ID = "1fsCeGUzsNCv0SCiE6mcIvcCHsMbqNeyzANwdU_148Vw"
    GID_ESPECIFICO = "1510755488"
    
    # Carregar credenciais OAuth2
    token_file = "google_oauth_token.json"
    if not os.path.exists(token_file):
        print(f"❌ Token OAuth2 não encontrado: {token_file}")
        return False
    
    try:
        # Autenticar
        creds = Credentials.from_authorized_user_file(token_file)
        client = gspread.authorize(creds)
        print("✅ Autenticação realizada com sucesso!")
        
        # Abrir planilha de Disponibilidade
        print("📋 Conectando com planilha Disponibilidade...")
        sheet = client.open_by_key(PLANILHA_DISPONIBILIDADE_ID)
        print(f"✅ Planilha: {sheet.title}")
        
        # Listar todas as abas com seus GIDs
        abas = sheet.worksheets()
        print(f"\n📑 ABAS DISPONÍVEIS COM GIDs:")
        
        aba_especifica = None
        for i, aba in enumerate(abas, 1):
            gid = str(aba.id)
            print(f"   {i:2d}. {aba.title:20} | GID: {gid:10} | {aba.row_count:4} linhas x {aba.col_count:2} colunas")
            
            if gid == GID_ESPECIFICO:
                aba_especifica = aba
                print(f"      🎯 ESTA É A ABA ESPECÍFICA!")
        
        if aba_especifica:
            print(f"\n🔍 ANALISANDO ABA ESPECÍFICA: {aba_especifica.title}")
            print(f"   GID: {aba_especifica.id}")
            print(f"   Dimensões: {aba_especifica.row_count} linhas x {aba_especifica.col_count} colunas")
            
            # Obter cabeçalhos
            headers = aba_especifica.row_values(1)
            print(f"\n📝 CABEÇALHOS ({len(headers)}):")
            for i, header in enumerate(headers, 1):
                letra = chr(64+i) if i <= 26 else f"A{chr(64+i-26)}"
                print(f"   {letra} ({i:2d}): {header}")
            
            # Procurar por colunas de aprovação
            print(f"\n🔍 PROCURANDO COLUNAS DE APROVAÇÃO:")
            colunas_aprovacao = []
            
            for i, header in enumerate(headers, 1):
                if header and any(palavra in header.lower() for palavra in ['aprovação', 'aprovacao', 'status', 'sim', 'não', 'pendente']):
                    colunas_aprovacao.append(i)
                    letra = chr(64+i) if i <= 26 else f"A{chr(64+i-26)}"
                    print(f"   🎯 Coluna {letra} ({i}): '{header}'")
            
            if not colunas_aprovacao:
                print("   ⚠️ Nenhuma coluna de aprovação encontrada explicitamente")
                print("   📋 Analisando todas as colunas para encontrar padrões...")
                
                # Analisar todas as colunas
                for i, header in enumerate(headers, 1):
                    if header:
                        letra = chr(64+i) if i <= 26 else f"A{chr(64+i-26)}"
                        print(f"\n   📊 Analisando coluna {letra} ({i}): '{header}'")
                        
                        try:
                            valores = aba_especifica.col_values(i)[1:]  # Pular cabeçalho
                            from collections import Counter
                            contador = Counter(valores)
                            
                            # Mostrar valores únicos mais comuns
                            valores_unicos = [v for v, count in contador.most_common(10) if v.strip()]
                            if valores_unicos:
                                print(f"      Valores únicos: {valores_unicos}")
                                
                                # Verificar se há padrões de aprovação
                                if any(v.upper() in ['SIM', 'NÃO', 'APROVADO', 'PENDENTE', 'YES', 'NO'] for v in valores_unicos):
                                    print(f"      🎯 POSSÍVEL COLUNA DE APROVAÇÃO!")
                                    colunas_aprovacao.append(i)
                        except Exception as e:
                            print(f"      ❌ Erro ao analisar coluna: {e}")
            
            # Analisar colunas de aprovação encontradas
            if colunas_aprovacao:
                print(f"\n📊 ANÁLISE DAS COLUNAS DE APROVAÇÃO:")
                
                for col in colunas_aprovacao:
                    letra = chr(64+col) if col <= 26 else f"A{chr(64+col-26)}"
                    header = headers[col-1]
                    
                    print(f"\n   🎯 Coluna {letra} ({col}): '{header}'")
                    
                    try:
                        valores = aba_especifica.col_values(col)[1:]  # Pular cabeçalho
                        from collections import Counter
                        contador = Counter(valores)
                        
                        print(f"      📊 Distribuição dos valores:")
                        for valor, count in contador.most_common():
                            if valor.strip():
                                print(f"         '{valor}': {count} ocorrências")
                        
                        # Mostrar amostra
                        print(f"      📋 Amostra dos primeiros 20 valores:")
                        for i, valor in enumerate(valores[:20], 1):
                            print(f"         {i:2d}. '{valor}'")
                            
                    except Exception as e:
                        print(f"      ❌ Erro ao analisar coluna: {e}")
            
            # Obter amostra de dados completos
            print(f"\n📋 AMOSTRA DE DADOS COMPLETOS (primeiras 5 linhas):")
            try:
                dados_amostra = aba_especifica.get_values('A1:Z6')  # Primeiras 6 linhas, colunas A-Z
                
                for i, linha in enumerate(dados_amostra):
                    if i == 0:
                        print(f"   Cabeçalho: {linha}")
                    else:
                        print(f"   Linha {i+1}: {linha}")
                        
            except Exception as e:
                print(f"   ❌ Erro ao obter amostra: {e}")
        
        else:
            print(f"\n❌ Aba com GID {GID_ESPECIFICO} não encontrada!")
            print(f"📋 GIDs disponíveis: {[str(aba.id) for aba in abas]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

if __name__ == "__main__":
    verificar_aba_especifica_disponibilidade()

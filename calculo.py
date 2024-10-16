# -*- coding: utf-8 -*-
import pandas as pd
import os
import sys
from complementares.dicionarios import biomas

def calcular_VETP1(VET1, i, n1, p):
    """
    Calcula o Valor Econômico Total Presente 1 (VETP1).
    
    Parâmetros:
        VET1 (float): Valor Econômico Total para o período n1 (Int.$/ha/ano)
        i (float): Taxa de juros (em decimal, por exemplo, 0.12 para 12%)
        n1 (float): Tempo decorrido desde o dano até a data atual (anos)
        p (float): Tempo de formação de uma floresta primária (anos)
        
    Retorna:
        float: Valor de VETP1 em Int.$/ha
    """
    VETP1 = VET1 * (((1 + i) ** n1 - 1) / (2 * i)) * (n1 / p)
    return VETP1

def calcular_VETP2(VET2, i, n2, p):
    """
    Calcula o Valor Econômico Total Presente 2 (VETP2).
    
    Parâmetros:
        VET2 (float): Valor Econômico Total para o período n2 (Int.$/ha/ano)
        i (float): Taxa de juros (em decimal, por exemplo, 0.12 para 12%)
        n2 (float): Tempo necessário para regeneração (anos)
        p (float): Tempo de formação de uma floresta primária (anos)
        
    Retorna:
        float: Valor de VETP2 em Int.$/ha
    """
    VETP2 = VET2 * (((1 + i) ** n2 - 1) / (2 * i * (1 + i) ** n2)) * (n2 / p)
    return VETP2

def calcular_VETP_total(VETP1, VETP2):
    """
    Calcula o Valor Econômico Total Presente (VETP).
    
    Parâmetros:
        VETP1 (float): Valor de VETP1 em Int.$/ha
        VETP2 (float): Valor de VETP2 em Int.$/ha
        
    Retorna:
        float: Valor total de VETP em Int.$/ha
    """
    return VETP1 + VETP2

def calcular_valor_dano_reversivel(A, VETP_reais):
    """
    Calcula o Valor do Dano Reversível.
    
    Parâmetros:
        A (float): Área afetada em hectares (ha)
        VETP_reais (float): Valor de VETP em R$/ha
        
    Retorna:
        float: Valor do dano reversível em R$
    """
    valor_dano = A * VETP_reais
    return f'{valor_dano:,.2f}'

def caminho_absoluto(relativo):
    # Verifica se está rodando dentro de um executável criado pelo PyInstaller
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relativo)
    # Caso contrário, usa o diretório atual (desenvolvimento)
    return os.path.join(os.path.abspath("."), relativo)

# Função que extrai o valor do arquivo Excel
def extrair_valor_data(bioma, ano):
    # Aqui, usamos o caminho absoluto para o arquivo 'valores_2.xlsx'
    arquivo_excel = caminho_absoluto('valores_2.xlsx')
    
    # Verifica se o arquivo existe antes de tentar carregá-lo
    if not os.path.exists(arquivo_excel):
        print(f"Arquivo {arquivo_excel} não encontrado!")
        return None

    # Carrega o arquivo Excel
    tabela = pd.read_excel(arquivo_excel)
    
    # Extrai o valor com base no bioma e ano fornecidos
    valor = tabela.loc[tabela['Ano'] == ano, bioma].values
    if len(valor) > 0:
        return valor[0]
    else:
        return None

def realizar_calculo(bioma, area_afetada, tempo_n1, ano):
    # Obtenção dos parâmetros n2 e p do bioma

    n2, p = biomas[bioma]
    VET1 = VET2 = extrair_valor_data(bioma, ano)
    i = 0.12  # Taxa de juros (12% ao ano)
    
    # Cálculos intermediários
    VETP1 = calcular_VETP1(VET1, i, tempo_n1, p)
    VETP2 = calcular_VETP2(VET2, i, n2, p)
    
    # Cálculo do VETP total
    VETP = calcular_VETP_total(VETP1, VETP2)
    
    # Cálculo final do valor do dano reversível
    valor_dano_reversivel = calcular_valor_dano_reversivel(area_afetada, VETP)
    return valor_dano_reversivel



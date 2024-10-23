# -*- coding: utf-8 -*-
import pandas as pd
import re
import os
import sys
import datetime
from complementares.dicionarios import biomas
from pprint import pprint

def remover_sufixo_ha(valor_str):
    """
    Remove o sufixo 'ha' de uma string e converte para float.
    
    Parâmetros:
        valor_str (str): String que contém o valor com o sufixo 'ha'.
        
    Retorna:
        float: Valor numérico sem o sufixo.
    """
    # Usa regex para encontrar um número e remover 'ha' ou espaços ao redor
    valor_limpo = re.sub(r'[^\d.,]', '', valor_str)  # Remove tudo exceto dígitos, pontos e vírgulas
    try:
        # Substitui vírgula por ponto para garantir a conversão correta para float
        return float(valor_limpo.replace(',', '.'))
    except ValueError:
        raise ValueError(f"Não foi possível converter o valor '{valor_str}' em número.")
    
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
    # Certifique-se de que VET1, i, n1, e p sejam floats
    if not all(isinstance(var, (int, float)) for var in [VET1, i, n1, p]):
        raise ValueError("Um ou mais valores de entrada para calcular_VETP1 não são numéricos.")
    
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
    # Certifique-se de que VET2, i, n2, e p sejam floats
    if not all(isinstance(var, (int, float)) for var in [VET2, i, n2, p]):
        raise ValueError("Um ou mais valores de entrada para calcular_VETP2 não são numéricos.")
    
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
        A (str ou float): Área afetada em hectares (ha), pode ser uma string com 'ha'.
        VETP_reais (float): Valor de VETP em R$/ha.
        
    Retorna:
        float: Valor do dano reversível em R$.
    """
    # Se A for string, remove o sufixo e converte para float
    if isinstance(A, str):
        try:
            A = remover_sufixo_ha(A)
        except:
            A = 0
    
    # Verifica se A e VETP_reais são valores numéricos
    if not isinstance(A, (int, float)) or not isinstance(VETP_reais, (int, float)):
        raise ValueError("A ou VETP_reais não são numéricos.")
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
    # Caminho do arquivo Excel
    arquivo_excel = caminho_absoluto('complementares/valores_2.xlsx')
    
    if not os.path.exists(arquivo_excel):
        print(f"Arquivo {arquivo_excel} não encontrado!")
        return None

    tabela = pd.read_excel(arquivo_excel)
    valor = tabela.loc[tabela['Ano'] == ano, bioma].values
    
    if len(valor) > 0:
        try:
            return float(valor[0])  # Certifique-se de retornar um valor numérico
        except ValueError:
            print(f"Valor inválido encontrado para {bioma} no ano {ano}")
            return None
    else:
        return None

def realizar_calculo(bioma, area_afetada, tempo_n1, ano):
    n2, p = biomas[bioma]
    data_atual = datetime.date.today()
    ano_atual = data_atual.year

    VET1 = extrair_valor_data(bioma, ano)
    VET2 = extrair_valor_data(bioma, int(ano_atual))
    i = 0.12  # Taxa de juros (12% ao ano)

    # Verifica se VET1 ou VET2 são None
    if VET1 is None or VET2 is None:
        raise ValueError(f"Não foi possível extrair valores para o bioma {bioma} no ano {ano} ou {ano_atual}.")

    # Cálculos intermediários
    VETP1 = calcular_VETP1(VET1, i, tempo_n1, p)
    VETP2 = calcular_VETP2(VET2, i, n2, p)

    # Cálculo do VETP total
    VETP = calcular_VETP_total(VETP1, VETP2)

    # Cálculo final do valor do dano reversível
    valor_dano_reversivel = calcular_valor_dano_reversivel(area_afetada, VETP)
    # valores = {
    #     'Tempo de regeneracao (n2)': n2,
    #     'Tempo': p,
    #     'Bioma': bioma,
    #     'VETP': VETP,
    #     'VET1': VET1,
    #     'VET2': VET2,
    #     'VETP1': VETP1,
    #     'VETP2': VETP2,
    #     'Tempo entre dano e data atual (n1)': tempo_n1,
    #     'Area Afetada': area_afetada
    # }
    # pprint(valores)
    # print()
    # print()
    return valor_dano_reversivel

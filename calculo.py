# -*- coding: utf-8 -*-
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

def converter_para_reais(VETP, PPP):
    """
    Converte o VETP de Int.$ para Reais (R$) utilizando a Paridade de Poder de Compra (PPP).
    
    Parâmetros:
        VETP (float): Valor de VETP em Int.$/ha
        PPP (float): Paridade de Poder de Compra (R$/Int.$)
        
    Retorna:
        float: Valor de VETP em R$/ha
    """
    return VETP * PPP

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

def calcular_custo_restauracao(A, CURF):
    """
    Calcula o Custo de Restauração (CR).
    
    Parâmetros:
        A (float): Área afetada em hectares (ha)
        CURF (float): Custo Unitário de Restauração da Vegetação (R$/ha)
        
    Retorna:
        float: Custo de restauração em R$
    """
    return A * CURF

def calcular_valor_dano_irreversivel(valor_dano_reversivel, custo_restauracao):
    """
    Calcula o Valor do Dano Irreversível.
    
    Parâmetros:
        valor_dano_reversivel (float): Valor do dano reversível em R$
        custo_restauracao (float): Custo de restauração em R$
        
    Retorna:
        float: Valor do dano irreversível em R$
    """
    return valor_dano_reversivel + custo_restauracao

def realizar_calculo(bioma, area_afetada, tempo_n1):
    # Obtenção dos parâmetros n2 e p do bioma

    n2, p, VET1, VET2 = biomas[bioma]
    i = 0.12  # Taxa de juros (12% ao ano)
    PPP = 2.583  # Paridade de Poder de Compra (Int.$ para R$)
    
    # Cálculos intermediários
    VETP1 = calcular_VETP1(VET1, i, tempo_n1, p)
    VETP2 = calcular_VETP2(VET2, i, n2, p)
    
    # Cálculo do VETP total
    VETP = calcular_VETP_total(VETP1, VETP2)
    
    # Conversão do VETP para reais
    VETP_reais = VETP * PPP
    
    # Cálculo final do valor do dano reversível
    valor_dano_reversivel = calcular_valor_dano_reversivel(area_afetada, VETP_reais)
    print(valor_dano_reversivel)
    return valor_dano_reversivel

# Exemplo de uso da função
bioma = 'Caatinga'
area_afetada = 20.49  # em hectares
tempo_n1 = 2  # tempo desde o dano até a data atual em anos

valor_reversivel = realizar_calculo(bioma, area_afetada, tempo_n1)
print(f"Valor do Dano Reversível: R$ {valor_reversivel}")


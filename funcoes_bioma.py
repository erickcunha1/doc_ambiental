from dicionarios import biomas, tempo

def calcular_valor_dano_reversivel(A, VETP):
    valor_dano = A * VETP
    return f'{valor_dano:,.2f}'

def calcular_valor_dano_irreversivel(A, VETP, CR):
    return (A * VETP) + CR

def calcular_custo_restauracao(A, CURF):
    return A * CURF

def calcular_vetp(VET1, VET2, n1, n2, p, i=0.12):
    VETP1 = (VET1 * ((1 + i)**n1 - 1) * n1) / (2 * i * p)
    VETP2 = (VET2 * ((1 + i)**n2 - 1) * n2) / (2 * i * ((1 + i)**n2) * p)
    return VETP1 + VETP2

def realizar_calculo(bioma, area_afetada, n1):
    n2 = biomas[bioma]
    p = tempo[bioma.lower()]

    VET1 = 7237  
    VET2 = 7939  

    VETP = calcular_vetp(VET1, VET2, n1, n2, p)

    VETP_reais = VETP * 2.583

    valor_dano_reversivel = calcular_valor_dano_reversivel(area_afetada, VETP_reais)
    
    return valor_dano_reversivel
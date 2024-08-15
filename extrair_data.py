import re
import datetime
from extrair_bioma import extract_text_from_pdf

def extrair_data(texto):
    padrao = r"IMAGEM DEPOIS\s*(\d{2}/\d{2}/\d{4})"
    datas = re.findall(padrao, texto)
    
    return datas

def calcular_diferenca_anos(datas):
    diferencas = []
    data_atual = datetime.date.today()
    
    for data in datas:
        data_extraida = datetime.datetime.strptime(data, "%d/%m/%Y").date()
        diferenca_anos = data_atual.year - data_extraida.year
    
        if (data_atual.month, data_atual.day) < (data_extraida.month, data_extraida.day):
            diferenca_anos -= 1
        diferencas.append(diferenca_anos)

    return diferencas

def extracao_anos(pdf_path):
    texto = extract_text_from_pdf(pdf_path)
    datas_extraidas = extrair_data(texto)[0]
    datas_extraidas = datetime.datetime.strptime(datas_extraidas, '%d/%m/%Y').date()

    return datas_extraidas

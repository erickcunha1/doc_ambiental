import openai
import ast
import json
from complementares.extrair_bioma import extract_text_from_pdf
from dotenv import load_dotenv
import os
from pprint import pprint


# load_dotenv()
# openai.api_key = os.getenv('CHAVE_OPENAI')

def extract_data_from_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente que extrai informações específicas de documentos."},
            {"role": "user", "content": f'''
             Extraia as seguintes informações deste documento e apresente-as no formato de um dicionário Python: 
             município, área (em hectares), código CAR, valor (em reais), longitude e latitude, 
             o valor da reserva legal, CPF/CNPJ e Denominação do imóvel rural, area do imovel rural, 
             número do CEFIR, número do alerta e o nome da promotoria (item 1.3). 
             Certifique-se de que os valores estejam corretos e bem formatados 
             (o nome das chaves devem ser as seguintes: municipio, area, codigo_CAR, valor, longitude, latitude, reserva_legal, 
             cpf, denominacao e total_area, CEFIR, numero_alerta, promotoria):\n\n{text}'''}
        ]
    )
    return response.choices[0].message['content']

def clean_response(response):
    if response.startswith("```") and response.endswith("```"):
        response = response.strip("```").strip()
    response = response.replace("\n", "").replace("\r", "")
    return response

def substituicao_dict(cleaned_data_str, pdf_text):
    while True:
        try:
            extracted_data = ast.literal_eval(cleaned_data_str)
            if isinstance(extracted_data, dict):
                return extracted_data
        except (SyntaxError, ValueError):
            cleaned_data_str = extract_data_from_text(pdf_text)

def criar_documento(caminho):
    pdf_text = extract_text_from_pdf(caminho)
    extracted_data_str = extract_data_from_text(pdf_text)
    cleaned_data_str = clean_response(extracted_data_str)
    extracted_data = substituicao_dict(cleaned_data_str, pdf_text)

    substituicoes = {
        "$proprietario": None,
        "$municipio": extracted_data.get('municipio', ''),
        "$area": extracted_data.get('area', ''),
        "$car": extracted_data.get('codigo_CAR', ''),
        "$lat": extracted_data.get('latitude', ''),
        "$lon": extracted_data.get('longitude', ''),
        "$rl": extracted_data.get('reserva_legal', ''),
        "$app": extracted_data.get('area', ''),
        "$cpf": extracted_data.get('cpf', ''),
        "$compromitente": extracted_data.get('proprietario', ''),
        "$denominacao": extracted_data.get('denominacao', ''),
        "$total_area": extracted_data.get('total_area', ''),
        "$CEFIR": None,
        "$numero_alerta": extracted_data.get('numero_alerta', ''),
        "$promotoria": extracted_data.get('promotoria', ''),
        "$valor": None,
        "$extenso": None,
    }
    # pprint(substituicoes)
    return substituicoes

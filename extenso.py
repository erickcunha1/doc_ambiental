def numero_por_extenso(numero):
    unidades = ["", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove"]
    especiais = ["dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"]
    dezenas = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
    centenas = ["", "cem", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos", "setecentos", "oitocentos", "novecentos"]

    numero = int(numero)

    if numero == 0:
        return "zero"

    if numero < 0:
        return "menos " + numero_por_extenso(abs(numero))

    partes = []

    if numero >= 100:
        centena = numero // 100
        resto = numero % 100
        if centena == 1 and resto != 0:
            partes.append("cento")
        else:
            partes.append(centenas[centena])
        numero = resto

    if numero >= 10 and numero < 20:
        partes.append(especiais[numero - 10])
        numero = 0
    else:
        dezena = numero // 10
        if dezena > 1:
            partes.append(dezenas[dezena])
        numero = numero % 10

    if numero > 0:
        partes.append(unidades[numero])

    return " e ".join([parte for parte in partes if parte])

def numero_completo_por_extenso(numero):
    numero = numero.replace(',', '')
    if '.' in numero:
        inteiro, decimal = numero.split('.')
    else:
        inteiro = numero
        decimal = '0'
    
    inteiro = int(inteiro)
    
    decimal = int(decimal[:2].ljust(2, '0')) 
    
    partes = []

    milhao = inteiro // 1000000
    if milhao > 0:
        if milhao == 1:
            partes.append("um milhão")
        else:
            partes.append(numero_por_extenso(milhao) + " milhões")
        inteiro = inteiro % 1000000

    milhar = inteiro // 1000
    if milhar > 0:
        if milhar == 1:
            partes.append("mil")
        else:
            partes.append(numero_por_extenso(milhar) + " mil")
        inteiro = inteiro % 1000

    if inteiro > 0:
        partes.append(numero_por_extenso(inteiro))
    
    if decimal > 0:
        partes.append(f"{numero_por_extenso(decimal)} centavos")
    else:
        partes.append("reais")

    return " e ".join(partes) + " reais"
import pandas as pd
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext

def display_menu():
    msg = """
    Menu:
    (P)lot quotations 3x2
    (M)aximum and minimum of each quotation
    (V)alorization of each company
    (E)volution of a stock portfolio value
    (A)nalyse a company
    (T)erminate
    """
    print(msg)


def calcular_max_min_cotacao(data):
    max_min_resultado = {}

    # Configurar a precisão para 3 casas decimais
    getcontext().prec = 7

    for company_name, cotacoes_empresa in data.items():
        # Converter valores para Decimal
        cotacoes_numeric = cotacoes_empresa.apply(lambda x: Decimal(str(x).replace(',', '').replace('e', 'E')))

        # Se o valor for maior ou igual a 10, dividir por 10
        # if cotacoes_numeric.max() >= 10:
        #    cotacoes_numeric /= 10

        max_cotacao = max(cotacoes_numeric)
        min_cotacao = min(cotacoes_numeric)

        max_min_resultado[company_name] = {'Max Quote': max_cotacao, 'Min Quote': min_cotacao}

    return max_min_resultado
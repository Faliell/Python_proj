

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


def exportar_max_min(max_min_resultado):
    with open("maxmin.txt", "w") as file:
        file.write("Company\tMin Quote\tMax Quote\n")
        for company, quotes in max_min_resultado.items():
            file.write(f"{company}\t{float(quotes['Min Quote']):.3f}\t{float(quotes['Max Quote']):.3f}\n")


def apresentar_resultados():
    with open("maxmin.txt", "r") as file:
        content = file.read()
        print(content)


def calcular_valorizacao(data_frame):
    valorizacoes = []

    for col in data_frame.columns:
        # Obter os valores antes de "e" convertidos para Decimal
        valores = data_frame[col].apply(lambda x: Decimal(str(x).split('e')[0]))

        # Calcular a valorização diretamente com Decimal
        valor_inicial = valores.iloc[0]
        valor_final = valores.iloc[-1]

        # Tratar caso específico da empresa F
        if col == 'F':
            valor_inicial = valor_inicial * Decimal('1e1')
            valor_final = valor_final * Decimal('1e1')

        # Calcular a valorização considerando 7 casas decimais
        valorizacao = valor_final - valor_inicial
        valorizacoes.append(valorizacao)

    return valorizacoes

def plot_grafico_barras(siglas, valorizacoes):
    fig, ax = plt.subplots()
    ax.barh(siglas, valorizacoes, color='blue')
    ax.set_xlabel('Valorização')
    ax.set_ylabel('Siglas')
    ax.set_title('Valorização de cada Empresa')
    plt.show()
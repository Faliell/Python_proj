import pandas as pd
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext

# Importações de Arquivos ###############################################
bolsa_file_path = "bolsa.txt"
siglas_file_path = "siglas.txt"

with open(siglas_file_path, 'r') as arquivo:
    siglas = arquivo.read()
    empresas = siglas.split('\n')

# Read the data from the "bolsa.txt" file into a DataFrame
df = pd.read_csv(bolsa_file_path, header=None, delim_whitespace=True)

# Funções #########################################################


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
        valorizacao = ((valor_final - valor_inicial) / abs(valor_inicial)) * 100

        valorizacoes.append(valorizacao)

    return valorizacoes




def plot_grafico_barras(siglas, valorizacoes):
    fig, ax = plt.subplots()
    ax.barh(siglas, valorizacoes, color='blue')
    ax.set_xlabel('Valorização')
    ax.set_ylabel('Siglas')
    ax.set_title('Valorização de cada Empresa')
    plt.show()


# Funções do MENU ###################################################################

def option_1():
    print("Selecionou a evolução das cotações das várias empresas")

    def plot_stock_prices(data_frame, companies_names):
        # Get the number of companies and columns
        num_companies, num_columns = data_frame.shape

        # Create a 3x2 subplot grid
        fig, axs = plt.subplots(3, 2, figsize=(12, 12))

        # Flatten the axs array for easier iteration
        axs = axs.flatten()

        # Plot the stock prices for each company
        for i in range(num_columns):
            ax = axs[i]
            ax.plot(data_frame.index, data_frame[i], label=f'Company {i + 1} - {companies_names[i]}')
            ax.set_title(f'')
            ax.set_xlabel('Row Number')
            ax.set_ylabel('Stock Price')
            ax.grid(True)
            ax.legend()

        # Adjust layout
        plt.tight_layout()
        plt.show()

    # Plot stock prices
    df.index = range(1, len(df) + 1)  # Add a numerical index starting from 1
    plot_stock_prices(df, empresas)


def option_2():
    print("Selecionou a opção para calcular a cotação máxima e mínima de cada um dos títulos no período em análise.")

    # Create a dictionary with company names as keys and their respective quotes as values
    data = {company_name: df[i] for i, company_name in enumerate(empresas)}

    # Calculate maximum and minimum quotations
    max_min_resultado = calcular_max_min_cotacao(data)

    # Export results to maxmin.txt
    exportar_max_min(max_min_resultado)

    print("Results exported to maxmin.txt.")

    # Present results
    apresentar_resultados()


def option_3():
    print("Selecionou a valorização (valor atual menos o valor inicial) de cada empresa.")

    # Calcular as valorizações considerando apenas os valores antes de "e"
    valorizacoes = calcular_valorizacao(df)

    # Exibir os valores de valorização em um gráfico de barras horizontais

    plt.barh(empresas, valorizacoes)
    plt.xlabel('Valorização %')
    plt.ylabel('Siglas das Empresas')
    plt.title('Valorização de cada Empresa')
    plt.show()

def option_4():
    print("Selecionou o valor da carteira ao longo do tempo e a sua evolução")

    # Supondo que 'df' é o DataFrame e 'empresas' é uma lista de nomes de colunas
    dic_empresas = {}
    count = 1
    c = 0
    # Preenchendo o dicionário de empresas
    for i in empresas:
        dic_empresas[count] = i
        count += 1

    # Exibindo as opções para o usuário
    for v, k in dic_empresas.items():
        print(f"{v} - {k}")

    # Obtendo a resposta do usuário
    resposta = input(f"Qual dessas empresas (1 a {len(empresas)}), escreva separado por ','? ")

    # Convertendo a resposta do usuário para uma lista de inteiros
    carteira = [int(x) - 1 for x in resposta.split(",")]

    n_acoes = []
    for i in carteira:
        x = int(input(f"quantas açoes de {i+1}: "))
        n_acoes.append(x)

    print(n_acoes)

    # Verificando se os índices fornecidos são válidos
    if any(i < 0 or i > len(empresas) for i in carteira):
        print("Índices inválidos. Por favor, forneça índices dentro do intervalo permitido.")
    else:
        # Criando uma máscara boolean para filtrar as empresas desejadas
        mask = [i in carteira for i in range(len(empresas))]

        # Selecionando as empresas com base na máscara
        empresas_selecionadas = df.loc[:, mask]
        print(empresas_selecionadas)

        c = empresas_selecionadas.sum(axis=1)

        print(c)

    # Criando uma máscara boolean para filtrar as empresas desejadas
    mask = [i in carteira for i in range(len(empresas))]

    # Selecionando as empresas com base na máscara
    empresas_selecionadas = df.loc[:, mask]
    print(empresas_selecionadas)

    valor_por_acao = empresas_selecionadas.multiply(n_acoes, axis=1)

    # Somando os valores para obter o valor total da carteira para cada período
    c = valor_por_acao.sum(axis=1)

    print(c)

    # Criando o gráfico
    plt.plot(c.index, c.values, label='Evolução da Carteira', color='blue')
    plt.scatter(c.idxmax(), c.max(), color='green', label='Máximo', marker='o')
    plt.scatter(c.idxmin(), c.min(), color='red', label='Mínimo', marker='o')

    plt.xlabel('Tempo')
    plt.ylabel('Valor da Carteira')
    plt.title('Evolução da Carteira ao Longo do Tempo')
    plt.legend()
    plt.show()


def option_5():
    print("Selecionou visualizar e apresentar a evolução das cotações dessa empresa.")

    dic_empresas = {}
    count = 1
    for i in empresas:
        dic_empresas[count] = i
        count += 1

    print(dic_empresas)

    resposta = int(input("Qual dessas empresas (1 a 6)? "))-1

    coluna = 0
    if 0 <= resposta < 7:
        coluna = df[resposta]
    else:
        print("Essa empresa não existe")

    m_dias = int(input("Quantos dias para calcular a média móvel? "))


    # Calcula a média móvel (por exemplo, com uma janela de 3 dias)
    media_movel = coluna.rolling(window=m_dias).mean()

    # Criar um gráfico de linha para a coluna
    plt.plot(coluna, label='Cotação diária')

    # Adicionar linha de média móvel
    plt.plot(media_movel, label='Média Móvel', linestyle='--', color='orange')

    # Adicionar rótulos e título
    plt.xlabel('Índice')
    plt.ylabel('Valores')
    plt.title('Gráfico da Coluna com Mínimo, Máximo e Média Móvel')

    # Adicionar legenda
    plt.legend()

    # Exibir o gráfico
    plt.show()

def option_6():
    print("Selecionou Terminar o Programa")


# Execução do Programa ########################################

program_on = True
while program_on:
    display_menu()
    choice = input("Enter your choice: ").upper()
    if choice == "P":
        option_1()
    elif choice == "M":
        option_2()
    elif choice == "V":
        option_3()
    elif choice == "E":
        option_4()
    elif choice == "A":
        option_5()
    elif choice == "T":
        print("Terminating the program. Goodbye!")
        program_on = False
    else:
        print("Invalid choice. Please enter the letter that corresponds to your choice")


import pandas as pd
import matplotlib.pyplot as plt
import funcoes.funcoes as f
from decimal import Decimal, getcontext

bolsa_file_path = "bolsa.txt"
siglas_file_path = "siglas.txt"

with open(siglas_file_path, 'r') as arquivo:
    siglas = arquivo.read()
    empresas = siglas.split('\n')

with open(bolsa_file_path, 'r') as arquivo2:
    bolsa = arquivo2.read()
    bolsalist = bolsa.split('\n')

# Read the data from the "bolsa.txt" file into a DataFrame
df = pd.read_csv(bolsa_file_path, header=None, delim_whitespace=True)

# Dividir por 10 apenas para a última coluna
df.iloc[:, -1] /= 10




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

    # Read the data from the "bolsa.txt" file into a DataFrame
    df = pd.read_csv(bolsa_file_path, header=None, delim_whitespace=True)

    # Read the company names from the "siglas.txt" file
    with open(siglas_file_path, 'r') as file:
        companies_names = [line.strip() for line in file]

    # Plot stock prices
    df.index = range(1, len(df) + 1)  # Add a numerical index starting from 1
    plot_stock_prices(df, companies_names)


def option_2():
    print("Selecionou a opção para calcular a cotação máxima e mínima de cada um dos títulos no período em análise.")

    # Read the data from the "bolsa.txt" file into a DataFrame
    df = pd.read_csv(bolsa_file_path, header=None, delim_whitespace=True)

    # Read the company names from the "siglas.txt" file
    with open(siglas_file_path, 'r') as file:
        companies_names = [line.strip() for line in file]

    # Dividir por 10 antes de calcular max quote e min quote
    df[df >= 10] /= 10

    # Create a dictionary with company names as keys and their respective quotes as values
    data = {company_name: df[i] for i, company_name in enumerate(companies_names)}

    # Calculate maximum and minimum quotations
    max_min_resultado = calcular_max_min_cotacao(data)

    # Export results to maxmin.txt
    exportar_max_min(max_min_resultado)

    print("Results exported to maxmin.txt.")

    # Present results
    apresentar_resultados()


def option_3():
    print("Selecionou a valorização (valor atual menos o valor inicial) de cada empresa.")

    # Read the company names from the "siglas.txt" file
    with open(siglas_file_path, 'r') as file:
        companies_names = [line.strip() for line in file]


    # Calcular as valorizações considerando apenas os valores antes de "e"
    valorizacoes = calcular_valorizacao(df)

    # Exibir os valores de valorização em um gráfico de barras horizontais

    plt.barh(empresas, valorizacoes)
    plt.xlabel('Valorização')
    plt.ylabel('Siglas das Empresas')
    plt.title('Valorização de cada Empresa')
    plt.show()
def option_4():
    print("Selecionou o valor da carteira ao longo do tempo e a sua evolução")


def option_5():
    print("Selecionou visualizar e apresentar a evolução das cotações dessa empresa.")


def option_6():
    print("Selecionou Terminar o Programa")


# Main program
### nunca usar while True

program_on = True
while program_on:
    f.display_menu()
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


import matplotlib.pyplot as plt
import pandas as pd

def analisar_empresa(cotacoes, media_movel_dias):
    empresa_escolhida = input("Digite o nome da empresa: ")
    cotacoes_empresa = cotacoes[empresa_escolhida]

    # Calcular a média móvel
    media_movel = []
    for i in range(len(cotacoes_empresa) - media_movel_dias + 1):
        media_movel.append(sum(cotacoes_empresa[i:i+media_movel_dias]) / media_movel_dias)

    # Plotar o gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(cotacoes_empresa, color='blue', label='Cotações')
    plt.plot(range(media_movel_dias - 1, len(cotacoes_empresa)), media_movel, color='orange', label='Média Móvel')
    plt.xlabel('Dias')
    plt.ylabel('Cotação')
    plt.title(f'Evolução das Cotações da Empresa {empresa_escolhida} e Média Móvel de {media_movel_dias} dias')
    plt.legend()
    plt.show()
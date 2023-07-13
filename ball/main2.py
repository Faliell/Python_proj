import tkinter as tk


# Função para calcular a velocidade, a aceleração e a energia cinética


def calcular():
    # Obtenção dos dados inseridos pelo usuário
    massa = float(massa_entry.get())
    forca = float(forca_entry.get())
    tempo = float(tempo_entry.get())
    fad = float(fad_entry.get())
    fae = float(fae_entry.get())

    # Cálculo da aceleração, da velocidade e da energia cinética

    if forca > 0:
        if fae >= forca:
            aceleracao = 0
        else:
            aceleracao = (forca - fae) / massa

    # Se forca for menor que zero e fae menor que zero e menor que forca
    else:
        if fae >= forca:
            aceleracao = 0
        else:
            # "- fae" para andar para a esquerda
            aceleracao = (forca + fae) / massa

    velocidade = aceleracao * tempo
    energia_cinetica = 0.5 * massa * (velocidade ** 2)

    # Atualização dos valores nos widgets correspondentes
    aceleracao_label.configure(text=f"Aceleração: {aceleracao:.2f} m/s²")
    velocidade_label.configure(text=f"Velocidade: {velocidade:.2f} m/s")
    energia_cinetica_label.configure(text=f"Energia Cinética: {energia_cinetica:.2f} J")
    fad_label.configure(text=f"Força de Atrito Dinâmico: {fad:.2f} N")
    fae_label.configure(text=f"Força de Atrito Estático: {fae:.2f} N")

    # Desenho da bola
    raio = 20
    x = raio + 300
    y = altura_canvas - raio - 3
    bola = canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill="red")

    # Movimento da bola
    x_inicial = x
    y_inicial = y
    tempo_total = 0
    while x < largura_canvas - raio:
        # Cálculo da nova posição da bola
        delta_t = 0.1
        if forca > 0:
            x = x_inicial + velocidade * tempo_total + 0.5 * aceleracao * (tempo_total ** 2)
        else:
            x = x_inicial - velocidade * tempo_total + 0.5 * aceleracao * (tempo_total ** 2)
        tempo_total += delta_t

        # Atualização da posição da bola no canvas
        canvas.move(bola, x - x_inicial, y - y_inicial)
        x_inicial = x
        canvas.update()


# Criação da janela

root = tk.Tk()
root.title("Calculadora de Movimento")

# Criação dos widgets para inserção dos dados
massa_label = tk.Label(root, text="Massa (kg): ")
massa_label.grid(row=0, column=0, padx=10, pady=5, sticky="W")
massa_entry = tk.Entry(root)
massa_entry.grid(row=0, column=1, padx=10, pady=5)
forca_label = tk.Label(root, text="Força (N): ")
forca_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
forca_entry = tk.Entry(root)
forca_entry.grid(row=1, column=1, padx=10, pady=5)
tempo_label = tk.Label(root, text="Tempo (s): ")
tempo_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
tempo_entry = tk.Entry(root)
tempo_entry.grid(row=2, column=1, padx=10, pady=5)
fad_label = tk.Label(root, text="Força de Atrito Dinâmico: ")
fad_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
fad_entry = tk.Entry(root)
fad_entry.grid(row=3, column=1, padx=10, pady=5)
fae_label = tk.Label(root, text="Força de Atrito Estático: ")
fae_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
fae_entry = tk.Entry(root)
fae_entry.grid(row=4, column=1, padx=10, pady=5)

# Criação do botão de cálculo
calcular_button = tk.Button(root, text="Calcular", command=calcular)
calcular_button.grid(row=5, column=1, padx=10, pady=10)

# Criação dos widgets para exibição

aceleracao_label = tk.Label(root, text="Aceleração: ")
aceleracao_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
velocidade_label = tk.Label(root, text="Velocidade: ")
velocidade_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
energia_cinetica_label = tk.Label(root, text="Energia Cinética: ")
energia_cinetica_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")

# Criação do canvas para desenho da bola
largura_canvas = 800
altura_canvas = 100
canvas = tk.Canvas(root, width=largura_canvas, height=altura_canvas)
canvas.grid(row=1, column=5, rowspan=9, padx=50, pady=50)

root.mainloop()

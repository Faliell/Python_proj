from tkinter import *
import math

root = Tk()
root.configure(bg="black")
root.title("Cálculo de Aceleração")

lbl_massa = Label(root, text="Digite a massa em kg: ", bg="black", fg="white", font=("Arial", 20))
lbl_massa.pack()

lbl_Forca_aplicada = Label(root, text="Digite a força aplicada em N: ", bg="black", fg="white", font=("Arial", 20))
lbl_Forca_aplicada.pack()

lbl_Forca_de_atrito_dinamica = Label(root, text="Digite a força de atrito dinâmica em N: ", bg="black", fg="white",
                                     font=("Arial", 20))
lbl_Forca_de_atrito_dinamica.pack()

lbl_Forca_de_atrito_estatica = Label(root, text="Digite a força de atrito estática em N: ", bg="black", fg="white",
                                     font=("Arial", 20))
lbl_Forca_de_atrito_estatica.pack()

lbl_tempo = Label(root, text="Digite o tempo da força aplicada em segundos: ", bg="black", fg="white",
                  font=("Arial", 20))
lbl_tempo.pack()

campo_massa = Entry(root)
campo_massa.pack()

campo_Forca_aplicada = Entry(root)
campo_Forca_aplicada.pack()

campo_Forca_de_atrito_dinamica = Entry(root)
campo_Forca_de_atrito_dinamica.pack()

campo_Forca_de_atrito_estatica = Entry(root)
campo_Forca_de_atrito_estatica.pack()

campo_tempo = Entry(root)
campo_tempo.pack()


def calcular_aceleracao():
    massa = float(campo_massa.get())
    Forca_aplicada = float(campo_Forca_aplicada.get())
    Forca_de_atrito_dinamica = float(campo_Forca_de_atrito_dinamica.get())
    Forca_de_atrito_estatica = float(campo_Forca_de_atrito_estatica.get())
    tempo = float(campo_tempo.get())

    modulo_Forca_aplicada = abs(Forca_aplicada)
    modulo_Forca_de_atrito_dinamica = abs(Forca_de_atrito_dinamica)
    modulo_Forca_de_atrito_estatica = abs(Forca_de_atrito_estatica)

    if modulo_Forca_aplicada - modulo_Forca_de_atrito_estatica <= 0:
        aceleracao = 0
    else:
        aceleracao = (modulo_Forca_aplicada - modulo_Forca_de_atrito_dinamica) / massa

    aceleracao = round(aceleracao, 5)

    lbl_aceleracao = Label(root, text="A aceleração é: " + str(aceleracao) + " m/s^2", bg="black", fg="white",
                           font=("Arial", 20))
    lbl_aceleracao.pack()

    velocidade = aceleracao * tempo
    velocidade = round(velocidade, 5)
    lbl_velocidade = Label(root, text="A velocidade é: " + str(velocidade) + " m/s", bg="black", fg="white",
                           font=("Arial", 20))
    lbl_velocidade.pack()

    energia_cinetica = 0.5 * massa * velocidade ** 2
    energia_cinetica = round(energia_cinetica, 5)


# Define a função para calcular a aceleração, velocidade e energia cinética
def calcular_aceleracao():
    # Obtendo os valores inseridos pelo usuário nos campos de entrada
    massa = float(campo_massa.get())
    Forca_aplicada = float(campo_Forca_aplicada.get())
    Forca_de_atrito_dinamica = float(campo_Forca_de_atrito_dinamica.get())
    Forca_de_atrito_estatica = float(campo_Forca_de_atrito_estatica.get())
    tempo = float(campo_tempo.get())

    # Calculando o módulo das forças
    modulo_Forca_aplicada = abs(Forca_aplicada)
    modulo_Forca_de_atrito_dinamica = abs(Forca_de_atrito_dinamica)
    modulo_Forca_de_atrito_estatica = abs(Forca_de_atrito_estatica)

    # Calculando a aceleração, se a força resultante for maior que zero
    if modulo_Forca_aplicada - modulo_Forca_de_atrito_estatica <= 0:
        aceleracao = 0
    else:
        aceleracao = (modulo_Forca_aplicada - modulo_Forca_de_atrito_dinamica) / massa

    # Cria os widgets para mostrar as saídas
    aceleracao_str = "{:.5f}".format(aceleracao)
    lbl_aceleracao = Label(root, text="A aceleração é: " + aceleracao_str + " m/s^2", bg="black", fg="white",
                           font=("Arial", 20))
    lbl_aceleracao.pack()

    velocidade = aceleracao * tempo
    velocidade_str = "{:.5f}".format(velocidade)
    lbl_velocidade = Label(root, text="A velocidade é: " + velocidade_str + " m/s", bg="black", fg="white",
                           font=("Arial", 20))
    lbl_velocidade.pack()

    energia_cinetica = 0.5 * massa * velocidade ** 2
    energia_cinetica_str = "{:.5f}".format(energia_cinetica)
    lbl_energia_cinetica = Label(root, text="A energia cinética é: " + energia_cinetica_str + " J", bg="black",
                                 fg="white", font=("Arial", 20))
    lbl_energia_cinetica.pack()


btn_calcular = Button(root, text="Calcular Aceleração, Velocidade e Energia Cinética", command=calcular_aceleracao,
                      bg="white", fg="black", font=("Arial", 20))
btn_calcular.pack()

root.mainloop()
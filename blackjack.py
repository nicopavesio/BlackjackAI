import numpy as np
import random
import pickle
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

baraja_poker = {
    'As de Corazones': [1, 11], '2 de Corazones': 2, '3 de Corazones': 3, '4 de Corazones': 4, '5 de Corazones': 5, 
    '6 de Corazones': 6, '7 de Corazones': 7, '8 de Corazones': 8, '9 de Corazones': 9, '10 de Corazones': 10, 
    'J de Corazones': 10, 'Q de Corazones': 10, 'K de Corazones': 10,
    'As de Diamantes': [1, 11], '2 de Diamantes': 2, '3 de Diamantes': 3, '4 de Diamantes': 4, '5 de Diamantes': 5, 
    '6 de Diamantes': 6, '7 de Diamantes': 7, '8 de Diamantes': 8, '9 de Diamantes': 9, '10 de Diamantes': 10, 
    'J de Diamantes': 10, 'Q de Diamantes': 10, 'K de Diamantes': 10,
    'As de Tréboles': [1, 11], '2 de Tréboles': 2, '3 de Tréboles': 3, '4 de Tréboles': 4, '5 de Tréboles': 5, 
    '6 de Tréboles': 6, '7 de Tréboles': 7, '8 de Tréboles': 8, '9 de Tréboles': 9, '10 de Tréboles': 10, 
    'J de Tréboles': 10, 'Q de Tréboles': 10, 'K de Tréboles': 10,
    'As de Picas': [1, 11], '2 de Picas': 2, '3 de Picas': 3, '4 de Picas': 4, '5 de Picas': 5, 
    '6 de Picas': 6, '7 de Picas': 7, '8 de Picas': 8, '9 de Picas': 9, '10 de Picas': 10, 
    'J de Picas': 10, 'Q de Picas': 10, 'K de Picas': 10
}

baraja_imagenes = {
    'As de Corazones': "Cartas/1.png", '2 de Corazones': "Cartas/2.png", '3 de Corazones': "Cartas/3.png", '4 de Corazones': "Cartas/4.png", '5 de Corazones': "Cartas/5.png", 
    '6 de Corazones': "Cartas/6.png", '7 de Corazones': "Cartas/7.png", '8 de Corazones': "Cartas/8.png", '9 de Corazones': "Cartas/9.png", '10 de Corazones': "Cartas/10.png", 
    'J de Corazones': "Cartas/j.png", 'Q de Corazones': "Cartas/q.png", 'K de Corazones': "Cartas/k.png",
    'As de Diamantes': "Cartas/1.png", '2 de Diamantes': "Cartas/2.png", '3 de Diamantes': "Cartas/3.png", '4 de Diamantes': "Cartas/4.png", '5 de Diamantes': "Cartas/5.png", 
    '6 de Diamantes': "Cartas/6.png", '7 de Diamantes': "Cartas/7.png", '8 de Diamantes': "Cartas/8.png", '9 de Diamantes': "Cartas/9.png", '10 de Diamantes': "Cartas/10.png", 
    'J de Diamantes': "Cartas/j.png", 'Q de Diamantes': "Cartas/q.png", 'K de Diamantes': "Cartas/k.png",
    'As de Tréboles': "Cartas/1.png", '2 de Tréboles': "Cartas/2.png", '3 de Tréboles': "Cartas/3.png", '4 de Tréboles': "Cartas/4.png", '5 de Tréboles': "Cartas/5.png", 
    '6 de Tréboles': "Cartas/6.png", '7 de Tréboles': "Cartas/7.png", '8 de Tréboles': "Cartas/8.png", '9 de Tréboles': "Cartas/9.png", '10 de Tréboles': "Cartas/10.png", 
    'J de Tréboles': "Cartas/j.png", 'Q de Tréboles': "Cartas/q.png", 'K de Tréboles': "Cartas/k.png",
    'As de Picas': "Cartas/1.png", '2 de Picas': "Cartas/2.png", '3 de Picas': "Cartas/3.png", '4 de Picas': "Cartas/4.png", '5 de Picas': "Cartas/5.png", 
    '6 de Picas': "Cartas/6.png", '7 de Picas': "Cartas/7.png", '8 de Picas': "Cartas/8.png", '9 de Picas': "Cartas/9.png", '10 de Picas': "Cartas/10.png", 
    'J de Picas': "Cartas/j.png", 'Q de Picas': "Cartas/q.png", 'K de Picas': "Cartas/k.png"
}

acciones = ['Coger carta','Cerrar']
valor = [0]
ALPHA = 0.05
GAMMA = 0.98
episodios = 10000
epsilon = 0.1

Q_table = np.zeros((100, len(acciones)))

def recibirCarta(baraja):
    carta = random.choice(list(baraja.keys()))
    del baraja[carta]
    return carta


def actualizarMano(carta, mano):
    mano.append(carta)

def calcularMano(mano):
    valor_total = 0
    valor_total2 = 0
    for carta in mano:
        if carta.startswith('As'):
            valor_total += 1
            valor_total2 += 11
        else:
            valor_total += baraja_poker[carta]
            valor_total2 += baraja_poker[carta] if isinstance(baraja_poker[carta], int) else baraja_poker[carta][1]
    return valor_total, valor_total2

def elegirAccion(estado,epsilon):
    if random.uniform(0, 1) < epsilon: 
        return random.choice(acciones)
    else:  
        return acciones[np.argmax(Q_table[estado])]


def recibirRecompensa(valor1, valor2, tamañoMano):
    recompensa1 = calcularRecompensa(valor1, tamañoMano)
    recompensa2 = calcularRecompensa(valor2, tamañoMano)
    return max(recompensa1, recompensa2)

def mejorValor(valor1, valor2, tamañoMano):
    recompensa1 = calcularRecompensa(valor1, tamañoMano)
    recompensa2 = calcularRecompensa(valor2, tamañoMano)
    if recompensa1 > recompensa2:
        return valor1
    else:
        return valor2

def calcularRecompensa(valor, tamañoMano):
    if valor > 21:
        return -1
    elif valor == 21:
        if tamañoMano == 2:
            return 6
        else:
            return 5
    elif valor == 20:
        return 4
    elif valor == 19:
        return 3
    elif valor == 18:
        return 2
    elif valor == 17:
        return 1
    else:
        return 0
    
def manoCrupier(baraja):
    manoCrupier = []
    while True:
        carta = recibirCarta(baraja)
        actualizarMano(carta,manoCrupier)
        valor1, valor2 = calcularMano(manoCrupier)
        valor = mejorValor(valor1, valor2, len(manoCrupier))
        if valor>=17:
            break
    
    return manoCrupier


def visualizarManos(mano, manoCrup,valor,valor2):
    num_imagenes1 = len(mano)
    num_imagenes2 = len(manoCrup)
    fig, axs = plt.subplots(2, max(num_imagenes1, num_imagenes2), figsize=(6, 6),
                            gridspec_kw={'hspace': 0.5, 'wspace': 0.5})
    fig.suptitle('Blackjack')

    # Mano jugador
    for i, carta in enumerate(mano):
        img = mpimg.imread(baraja_imagenes[carta])
        axs[0,i].imshow(img, extent=[0, 100, 0, 150])
        axs[0,i].set_title(f"Tu mano: {carta}",fontsize=6)
        axs[0,i].axis('off')
   
    # Mano crupier
    for i, carta in enumerate(manoCrup):
        img = mpimg.imread(baraja_imagenes[carta])
        axs[1,i].imshow(img, extent=[0, 100, 0, 150])
        axs[1,i].set_title(f"Crupier: {carta}",fontsize=6)
        axs[1,i].axis('off')
    
    for ax_row in axs:
        for ax in ax_row:
            if not ax.get_title():
                ax.axis('off')

    if valor2 > valor and valor2<22:
        resultado = 'pierdes'
    elif valor==valor2:
        resultado = 'empate'
    elif valor > 21:
        resultado = 'pierdes'
    else:
        resultado = 'ganas'
    if valor>21:
        plt.figtext(0.5, 0.02, f'Tu mano suma {valor} por lo que {resultado}', ha='center', fontsize=10)
    else:
        plt.figtext(0.5, 0.02, f'Tu mano suma {valor}, la del crupier suma {valor2} por lo que {resultado}', ha='center', fontsize=10)


    plt.show()

def visualizarEstadisticas(victorias,empates,derrotas):
    labels = ['Victorias', 'Derrotas', 'Empates']
    sizes = [victorias, derrotas, empates]
    colors = ['green', 'red', 'gray']

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('Porcentajes')
    plt.axis('equal')
    plt.show()
    

victorias = 0
empates = 0
derrotas = 0
for episodio in range(episodios):
    victoria = False
    recompensa_total = 0
    estado = 0
    baraja = baraja_poker.copy()
    mano = []
    manoCrup = []
    for partida in range(21):
        accion = elegirAccion(estado,epsilon)
        if accion == 'Cerrar':
            break
        else:
            carta = recibirCarta(baraja)
            actualizarMano(carta,mano)
            valor1, valor2 = calcularMano(mano)
            recompensa = recibirRecompensa(valor1,valor2, len(mano))
            recompensa_total += recompensa
            nuevo_estado = mejorValor(valor1,valor2,len(mano))
            accion_indice = acciones.index(accion)
            Q_table[estado, accion_indice] += ALPHA * (recompensa + GAMMA * np.max(Q_table[nuevo_estado]) - Q_table[estado, accion_indice])
            estado = mejorValor(valor1,valor2,len(mano))
        if estado > 21:
            break
        
    if estado < 22:
        manoCrup = manoCrupier(baraja)
        v1Crup, v2Crup = calcularMano(manoCrup)
        vtotalCrup = mejorValor(v1Crup,v2Crup,len(manoCrup))
        if vtotalCrup > 21 and estado <= 21:
            recompensa_total += 1
            victoria = True
        elif estado > 21:
            victoria = False
        elif vtotalCrup > estado:
            recompensa_total -= 4
            victoria = False
        elif vtotalCrup == estado:
            victoria = False
        else:
            victoria = True

        if victoria == True:
            victorias += 1
        elif vtotalCrup==estado:
            empates += 1
        elif vtotalCrup>21 and estado>21:
            empates += 1
        else:
            derrotas += 1
    else:
        derrotas += 1
    
    print(f"Episodio {episodio + 1}, Recompensa total: {recompensa_total}, Mejor Q-valor: {np.max(Q_table)}")
    if episodio == episodios-1:
        visualizarManos(mano,manoCrup,estado,vtotalCrup)

    
print("Victorias: ",victorias)
print("Porcentaje de victorias: ", victorias/episodios*100)
visualizarEstadisticas(victorias,empates,derrotas)




        


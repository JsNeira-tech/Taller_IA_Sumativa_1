import numpy as np
from logica_juego import soltar_pieza, nodo_terminal, obtener_pos_valida, jugada_ganadora, caida_fila

# Evalúa una ventana específica del tablero y asigna un puntaje.
def evaluar_ventana(ventana, pieza):
    puntaje = 0
    pieza_oponente = 1 if pieza == 2 else 2
    if ventana.count(pieza) == 4:
        puntaje += 100
    elif ventana.count(pieza) == 3 and ventana.count(0) == 1:
        puntaje += 5
    elif ventana.count(pieza) == 2 and ventana.count(0) == 2:
        puntaje += 2
    if ventana.count(pieza_oponente) == 3 and ventana.count(0) == 1:
        puntaje -= 4
    return puntaje

# Calcula el puntaje de la posición actual del tablero.
def posicion_puntaje(tabla_juego, pieza, num_filas, num_columnas):
    puntaje = 0

    # Puntuar columna central
    arreglo_central = [int(i) for i in list(tabla_juego[:, num_columnas // 2])]
    contador = arreglo_central.count(pieza)
    puntaje += contador * 3

    # Puntuar horizontal
    for r in range(num_filas):
        arreglo_fila = [int(i) for i in list(tabla_juego[r, :])]
        for c in range(num_columnas-3):
            ventana = arreglo_fila[c:c + 4]
            puntaje += evaluar_ventana(ventana, pieza)

    # Puntuar vertical
    for c in range(num_columnas):
        arreglo_columna = [int(i) for i in list(tabla_juego[:, c])]
        for r in range(num_filas-3):
            ventana = arreglo_columna[r:r + 4]
            puntaje += evaluar_ventana(ventana, pieza)

    # Puntuar diagonal positiva
    for r in range(num_filas-3):
        for c in range(num_columnas-3):
            ventana = [tabla_juego[r + i][c + i] for i in range(4)]
            puntaje += evaluar_ventana(ventana, pieza)

    # Puntuar diagonal negativa
    for r in range(num_filas-3):
        for c in range(num_columnas-3):
            ventana = [tabla_juego[r + 3 - i][c + i] for i in range(4)]
            puntaje += evaluar_ventana(ventana, pieza)

    return puntaje

# Implementa el algoritmo minimax con poda alfa-beta para determinar la mejor jugada.
def minimax(tabla_juego, prof, max_jugador, num_filas, num_columnas, alpha=-np.inf, beta=np.inf, nodos_explorados=0):
    nodos_explorados += 1
    pos_valida = obtener_pos_valida(tabla_juego, num_filas, num_columnas)
    es_final = nodo_terminal(tabla_juego, num_filas, num_columnas)
    if prof == 0 or es_final:
        if es_final:
            if jugada_ganadora(tabla_juego, 2, num_filas, num_columnas):
                return (None, 100000000000000, nodos_explorados)
            elif jugada_ganadora(tabla_juego, 1, num_filas, num_columnas):
                return (None, -10000000000000, nodos_explorados)
            else:
                return (None, 0, nodos_explorados)
        else:
            return (None, posicion_puntaje(tabla_juego, 2, num_filas, num_columnas), nodos_explorados)
    if max_jugador:
        valor = -np.inf
        columna = np.random.choice(pos_valida)
        for col in pos_valida:
            fila = caida_fila(tabla_juego, col, num_filas)
            temp_tabla_juego = tabla_juego.copy()
            soltar_pieza(temp_tabla_juego, fila, col, 2)
            _, nuevo_puntaje, nodos_explorados = minimax(temp_tabla_juego, prof - 1, False, num_filas, num_columnas, alpha, beta, nodos_explorados)
            if nuevo_puntaje > valor:
                valor = nuevo_puntaje
                columna = col
            alpha = max(alpha, valor)
            if alpha >= beta:
                break
        return columna, valor, nodos_explorados
    else:
        valor = np.inf
        columna = np.random.choice(pos_valida)
        for col in pos_valida:
            fila = caida_fila(tabla_juego, col, num_filas)
            temp_tabla_juego = tabla_juego.copy()
            soltar_pieza(temp_tabla_juego, fila, col, 1)
            _, nuevo_puntaje, nodos_explorados = minimax(temp_tabla_juego, prof - 1, True, num_filas, num_columnas, alpha, beta, nodos_explorados)
            if nuevo_puntaje < valor:
                valor = nuevo_puntaje
                columna = col
            beta = min(beta, valor)
            if alpha >= beta:
                break
        return columna, valor, nodos_explorados

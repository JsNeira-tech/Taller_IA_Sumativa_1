import numpy as np

# Crea y devuelve una tabla vacía para el juego.
def crear_tabla(num_filas, num_columnas):
    tabla = np.zeros((num_filas, num_columnas))
    return tabla

# Coloca una pieza en el tablero en la posición especificada.
def soltar_pieza(tabla, fila, columna, pieza):
    tabla[fila][columna] = pieza

# Verifica si una columna específica tiene espacio para una nueva pieza.
def ubicacion_valida(tabla, columna, num_filas):
    return tabla[num_filas-1][columna] == 0

# Encuentra la fila más baja disponible en una columna específica.
def caida_fila(tabla, columna, num_filas):
    for fila in range(num_filas):
        if tabla[fila][columna] == 0:
            return fila

# Verifica si la última jugada fue una jugada ganadora.
def jugada_ganadora(tabla, pieza, num_filas, num_columnas):
    # Comprobación horizontal
    for c in range(num_columnas-3):
        for r in range(num_filas):
            if tabla[r][c] == pieza and tabla[r][c+1] == pieza and tabla[r][c+2] == pieza and tabla[r][c+3] == pieza:
                return True

    # Comprobación vertical
    for c in range(num_columnas):
        for r in range(num_filas-3):
            if tabla[r][c] == pieza and tabla[r+1][c] == pieza and tabla[r+2][c] == pieza and tabla[r+3][c] == pieza:
                return True

    # Comprobación diagonal positiva
    for c in range(num_columnas-3):
        for r in range(num_filas-3):
            if tabla[r][c] == pieza and tabla[r+1][c+1] == pieza and tabla[r+2][c+2] == pieza and tabla[r+3][c+3] == pieza:
                return True

    # Comprobación diagonal negativa
    for c in range(num_columnas-3):
        for r in range(3, num_filas):
            if tabla[r][c] == pieza and tabla[r-1][c+1] == pieza and tabla[r-2][c+2] == pieza and tabla[r-3][c+3] == pieza:
                return True

    return False

# Verifica si el nodo actual es un nodo terminal (estado final del juego).
def nodo_terminal(tabla, num_filas, num_columnas):
    return jugada_ganadora(tabla, 1, num_filas, num_columnas) or jugada_ganadora(tabla, 2, num_filas, num_columnas) or tablero_lleno(tabla, num_filas, num_columnas)

# Obtiene una lista de columnas válidas donde se puede colocar una pieza.
def obtener_pos_valida(tabla, num_filas, num_columnas):
    pos_validas = []
    for columna in range(num_columnas):
        if ubicacion_valida(tabla, columna, num_filas):
            pos_validas.append(columna)
    return pos_validas

# Verifica si el tablero está lleno.
def tablero_lleno(tabla, num_filas, num_columnas):
    for columna in range(num_columnas):
        if tabla[num_filas-1][columna] == 0:
            return False
    return True

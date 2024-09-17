import pygame
import sys
import os
import numpy as np
import time
from logica_juego import soltar_pieza, nodo_terminal, obtener_pos_valida, jugada_ganadora, crear_tabla, ubicacion_valida, caida_fila, tablero_lleno
from minimax_1 import minimax as minimax_1
from minimax_a_b import minimax as minimax_a_b
from interfaz import pantalla_seleccion, dibujar_tablero, dibujar_info, mostrar_resultado, esperar_jugada_usuario, dibujar_texto_pequeno

# Inicializar Pygame
pygame.init()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Tamaño de celda y fuente
TAMANO_CELDA = 100

# Es el archivo principal que coordina el juego.
def main():
    tamano, dificultad, algoritmo = pantalla_seleccion()
    num_filas, num_columnas = tamano

    ancho_tablero = num_columnas * TAMANO_CELDA
    ancho_info = 400
    alto = (num_filas + 1) * TAMANO_CELDA + 50
    pantalla = pygame.display.set_mode((ancho_tablero + ancho_info, alto))
    pygame.display.set_caption('Connect 4')
    
    ficha_roja = pygame.image.load('ficha_roja.png')
    ficha_amarilla = pygame.image.load('ficha_amarilla.png')
    ficha_roja = pygame.transform.scale(ficha_roja, (TAMANO_CELDA, TAMANO_CELDA))
    ficha_amarilla = pygame.transform.scale(ficha_amarilla, (TAMANO_CELDA, TAMANO_CELDA))
    
    tablero = crear_tabla(num_filas, num_columnas)
    juego_terminado = False
    info_text = []
    jugada_count = 0
    sugerencia = None
    
    while not juego_terminado:
        pantalla.fill(BLANCO)
        dibujar_tablero(pantalla, tablero, num_filas, num_columnas, ficha_roja, ficha_amarilla)
        dibujar_info(pantalla, info_text, ancho_tablero, num_columnas)
        dibujar_texto_pequeno(pantalla, "Presiona S para una sugerencia de jugada", ancho_tablero // 2 - 150, 10, NEGRO)
        if sugerencia is not None:
            dibujar_texto_pequeno(pantalla, sugerencia, ancho_tablero // 2 - 100, 50, NEGRO)
        pygame.display.update()
        
        # Turno del usuario
        col_usuario, sugerencia = esperar_jugada_usuario(pantalla, tablero, num_filas, num_columnas, ficha_roja, ficha_amarilla, info_text, ancho_tablero, sugerencia, dificultad, algoritmo)
        jugada_count += 1
        
        if jugada_ganadora(tablero, 1, num_filas, num_columnas):
            info_text.append(f"Jugada {jugada_count}:\n¡Humano gana!")
            pantalla.fill(BLANCO)
            dibujar_tablero(pantalla, tablero, num_filas, num_columnas, ficha_roja, ficha_amarilla)
            dibujar_info(pantalla, info_text, ancho_tablero, num_columnas)
            mostrar_resultado(pantalla, "¡Humano gana!", ancho_tablero)
            juego_terminado = True
            break
        
        if tablero_lleno(tablero, num_filas, num_columnas):
            info_text.append(f"Jugada {jugada_count}:\n¡Empate!")
            pantalla.fill(BLANCO)
            dibujar_tablero(pantalla, tablero, num_filas, num_columnas, ficha_roja, ficha_amarilla)
            dibujar_info(pantalla, info_text, ancho_tablero, num_columnas)
            mostrar_resultado(pantalla, "¡Empate!", ancho_tablero)
            juego_terminado = True
            break
        
        pantalla.fill(BLANCO)
        dibujar_tablero(pantalla, tablero, num_filas, num_columnas, ficha_roja, ficha_amarilla)
        dibujar_info(pantalla, info_text, ancho_tablero, num_columnas)
        dibujar_texto_pequeno(pantalla, "Presiona S para una sugerencia de jugada", ancho_tablero // 2 - 150, 10, NEGRO)
        if sugerencia is not None:
            dibujar_texto_pequeno(pantalla, sugerencia, ancho_tablero // 2 - 100, 50, NEGRO)
        pygame.display.update()
        
        # Turno de la IA
        start_time = time.time()
        col, minimax_score, nodos_explorados = algoritmo(tablero, dificultad, True, num_filas, num_columnas)
        end_time = time.time()
        
        tiempo_usado = (end_time - start_time) * 1000
        
        # Agregar información de la jugada
        info_jugada = f"Jugada {jugada_count}:\n"
        info_jugada += f"Nodos explorados: {nodos_explorados}\n"
        info_jugada += f"Tiempo utilizado: {tiempo_usado:.2f} ms"
        
        info_text.append(info_jugada)
        
        # Mantener solo las últimas 10 jugadas
        if len(info_text) > 10:
            info_text = info_text[-10:]
        
        fila = caida_fila(tablero, col, num_filas)
        soltar_pieza(tablero, fila, col, 2)
        
        if jugada_ganadora(tablero, 2, num_filas, num_columnas):
            info_text.append(f"Jugada {jugada_count}:\n¡La IA gana!")
            pantalla.fill(BLANCO)
            dibujar_tablero(pantalla, tablero, num_filas, num_columnas, ficha_roja, ficha_amarilla)
            dibujar_info(pantalla, info_text, ancho_tablero, num_columnas)
            mostrar_resultado(pantalla, "¡La IA gana!", ancho_tablero)
            juego_terminado = True
            break
        
        if tablero_lleno(tablero, num_filas, num_columnas):
            info_text.append(f"Jugada {jugada_count}:\n¡Empate!")
            pantalla.fill(BLANCO)
            dibujar_tablero(pantalla, tablero, num_filas, num_columnas, ficha_roja, ficha_amarilla)
            dibujar_info(pantalla, info_text, ancho_tablero, num_columnas)
            mostrar_resultado(pantalla, "¡Empate!", ancho_tablero)
            juego_terminado = True
            break

    print("FIN DEL JUEGO")
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.wait(100)

if __name__ == "__main__":
    main()

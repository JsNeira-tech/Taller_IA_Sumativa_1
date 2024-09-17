import numpy as np
import pygame
import sys
import os
from minimax_1 import minimax as minimax_1
from minimax_a_b import minimax as minimax_a_b
from logica_juego import soltar_pieza, caida_fila, ubicacion_valida

# Inicializar Pygame
pygame.init()

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
TAMANO_CELDA = 100
FUENTE = pygame.font.Font(None, 36)
FUENTE_PEQUENA = pygame.font.Font(None, 24)
FUENTE_CONFIG_TITULO = pygame.font.Font(None, 28)
FUENTE_CONFIG_OPCIONES = pygame.font.Font(None, 24)

#Centra la ventana del juego en la pantalla del usuario
def centrar_ventana():
    pantalla_info = pygame.display.Info()
    pantalla_ancho = pantalla_info.current_w
    pantalla_alto = pantalla_info.current_h
    ventana_ancho = 400
    ventana_alto = 550
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((pantalla_ancho - ventana_ancho) // 2, (pantalla_alto - ventana_alto) // 2)

# Dibuja texto en la pantalla en la posición especificada.
def dibujar_texto(pantalla, texto, x, y, color=NEGRO, fuente=FUENTE):
    superficie_texto = fuente.render(texto, True, color)
    pantalla.blit(superficie_texto, (x, y))

# Muestra una pantalla de configuración donde el usuario puede seleccionar el tamaño del tablero, la dificultad y el algoritmo de la IA.
def pantalla_seleccion():
    centrar_ventana()
    pantalla = pygame.display.set_mode((400, 550))
    pygame.display.set_caption('Configuración de Connect 4')
    
    opciones_tamano = ["6 x 7", "4 x 5"]
    opciones_dificultad = ["Fácil", "Normal", "Difícil"]
    opciones_algoritmo = ["Minimax", "Minimax con poda alfa-beta"]
    
    seleccion_tamano = 1  # Predeterminado a "4 x 5"
    seleccion_dificultad = 1  # Predeterminado a "Normal"
    seleccion_algoritmo = 1  # Predeterminado a "Minimax con poda alfa-beta"
    
    clock = pygame.time.Clock()
    
    while True:
        pantalla.fill(BLANCO)
        
        # Título y opciones de tamaño
        dibujar_texto(pantalla, "¿De qué tamaño será el juego?", 20, 30, fuente=FUENTE_CONFIG_TITULO)
        for i, opcion in enumerate(opciones_tamano):
            color = NEGRO if i == seleccion_tamano else (200, 200, 200)
            pygame.draw.circle(pantalla, color, (30, 80 + i * 40), 10, 2)
            if i == seleccion_tamano:
                pygame.draw.circle(pantalla, color, (30, 80 + i * 40), 5)
            dibujar_texto(pantalla, opcion, 50, 70 + i * 40, color, fuente=FUENTE_CONFIG_OPCIONES)
        
        # Dificultad de IA
        dibujar_texto(pantalla, "Seleccione la dificultad de IA", 20, 160, fuente=FUENTE_CONFIG_TITULO)
        for i, opcion in enumerate(opciones_dificultad):
            color = NEGRO if i == seleccion_dificultad else (200, 200, 200)
            pygame.draw.circle(pantalla, color, (30, 210 + i * 40), 10, 2)
            if i == seleccion_dificultad:
                pygame.draw.circle(pantalla, color, (30, 210 + i * 40), 5)
            dibujar_texto(pantalla, opcion, 50, 200 + i * 40, color, fuente=FUENTE_CONFIG_OPCIONES)
        
        # Algoritmo IA
        dibujar_texto(pantalla, "Selecciona el Algoritmo IA", 20, 330, fuente=FUENTE_CONFIG_TITULO)
        for i, opcion in enumerate(opciones_algoritmo):
            color = NEGRO if i == seleccion_algoritmo else (200, 200, 200)
            pygame.draw.circle(pantalla, color, (30, 380 + i * 40), 10, 2)
            if i == seleccion_algoritmo:
                pygame.draw.circle(pantalla, color, (30, 380 + i * 40), 5)
            dibujar_texto(pantalla, opcion, 50, 370 + i * 40, color, fuente=FUENTE_CONFIG_OPCIONES)
        
        # Botón de ingresar
        pygame.draw.rect(pantalla, NEGRO, (150, 480, 100, 40), 2)
        dibujar_texto(pantalla, "INGRESAR", 160, 485, fuente=FUENTE_PEQUENA)
        
        pygame.display.update()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if 150 <= x <= 250 and 480 <= y <= 520:
                    tamano = (6, 7) if seleccion_tamano == 0 else (4, 5)
                    dificultad = 1 if seleccion_dificultad == 0 else (3 if seleccion_dificultad == 1 else 5)
                    algoritmo = minimax_1 if seleccion_algoritmo == 0 else minimax_a_b
                    return tamano, dificultad, algoritmo
                
                # Check if click was inside any radio button
                for i in range(len(opciones_tamano)):
                    if 20 <= x <= 40 and 70 + i * 40 <= y <= 90 + i * 40:
                        seleccion_tamano = i
                
                for i in range(len(opciones_dificultad)):
                    if 20 <= x <= 40 and 200 + i * 40 <= y <= 220 + i * 40:
                        seleccion_dificultad = i
                
                for i in range(len(opciones_algoritmo)):
                    if 20 <= x <= 40 and 370 + i * 40 <= y <= 390 + i * 40:
                        seleccion_algoritmo = i
        
        clock.tick(60)

# Dibuja el tablero del juego y las piezas en la pantalla.
def dibujar_tablero(pantalla, tablero, num_filas, num_columnas, ficha_roja, ficha_amarilla):
    for c in range(num_columnas):
        for r in range(num_filas):
            pygame.draw.rect(pantalla, (0, 0, 255), (c*TAMANO_CELDA, (r+1)*TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
            pygame.draw.circle(pantalla, BLANCO, (int(c*TAMANO_CELDA+TAMANO_CELDA/2), int((r+1)*TAMANO_CELDA+TAMANO_CELDA/2)), int(TAMANO_CELDA/2 - 5))
    
    for c in range(num_columnas):
        for r in range(num_filas):
            if tablero[r][c] == 1:
                pantalla.blit(ficha_roja, (c*TAMANO_CELDA, (num_filas-r)*TAMANO_CELDA))
            elif tablero[r][c] == 2:
                pantalla.blit(ficha_amarilla, (c*TAMANO_CELDA, (num_filas-r)*TAMANO_CELDA))

# Dibuja texto pequeño en la pantalla en la posición especificada.
def dibujar_texto_pequeno(pantalla, texto, x, y, color=BLANCO):
    superficie_texto = pygame.font.Font(None, 24).render(texto, True, color)
    pantalla.blit(superficie_texto, (x, y))

# Dibuja nodos explorados y tiempo utilizado
def dibujar_info(pantalla, info_text, ancho_tablero, num_columnas):
    x_offset = ancho_tablero + 20
    y_offset = 20
    line_height = 20
    jugada_height = 80  # Altura para cada registro de jugada, incluyendo espacio
    
    for i, jugada in enumerate(reversed(info_text)):
        lines = jugada.split('\n')
        for j, line in enumerate(lines):
            dibujar_texto_pequeno(pantalla, line, x_offset, y_offset + (i*jugada_height + j*line_height), NEGRO)

# Muestra el resultado del juego (quién ganó o si hubo empate) en la pantalla.
def mostrar_resultado(pantalla, mensaje, ancho_tablero):
    dibujar_texto_pequeno(pantalla, mensaje, ancho_tablero // 2 - 100, 10, NEGRO)
    pygame.display.update()

# Espera y maneja la jugada del usuario, incluyendo la opción de pedir una sugerencia.
def esperar_jugada_usuario(pantalla, tablero, num_filas, num_columnas, ficha_roja, ficha_amarilla, info_text, ancho_tablero, sugerencia, profundidad, algoritmo):
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:
                    sugerencia = sugerir_jugada(pantalla, tablero, num_filas, num_columnas, ficha_roja, ficha_amarilla, info_text, ancho_tablero, profundidad, algoritmo)
            if evento.type == pygame.MOUSEBUTTONDOWN:
                posx = evento.pos[0]
                col = int(posx // TAMANO_CELDA)
                if col >= 0 and col < num_columnas:  # Verificar que col esté dentro de los límites
                    if ubicacion_valida(tablero, col, num_filas):
                        fila = caida_fila(tablero, col, num_filas)
                        soltar_pieza(tablero, fila, col, 1)
                        return col, None  # Borrar la sugerencia después de la jugada
                else:
                    print(f"Columna {col} fuera de los límites")

        pantalla.fill(BLANCO)
        dibujar_tablero(pantalla, tablero, num_filas, num_columnas, ficha_roja, ficha_amarilla)
        dibujar_info(pantalla, info_text, ancho_tablero, num_columnas)
        dibujar_texto_pequeno(pantalla, "Presiona S para una sugerencia de jugada", ancho_tablero // 2 - 150, 10, NEGRO)
        if sugerencia is not None:
            dibujar_texto_pequeno(pantalla, sugerencia, ancho_tablero // 2 - 100, 50, NEGRO)
        pygame.display.update()

# Utiliza el algoritmo de la IA para sugerir una jugada al usuario.
def sugerir_jugada(pantalla, tablero, num_filas, num_columnas, ficha_roja, ficha_amarilla, info_text, ancho_tablero, profundidad, algoritmo):
    col, _, _ = algoritmo(tablero, profundidad, True, num_filas, num_columnas)
    return f"Sugerencia: Columna {col + 1}"

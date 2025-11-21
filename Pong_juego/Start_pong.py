"""Orquestador modular del juego Pong.

Este archivo solo expone una función `main()` que carga recursos, muestra
la presentación/menú y arranca el juego usando los módulos
`resources`, `menu` y `pong_game`.
"""

import pygame

from resources import load_resources
from menu import show_presentation, show_menu, show_help_screen
from pong_game import run_game


def main():
    pygame.init()
    pygame.mouse.set_visible(True)

    # Cargar recursos (sonidos, imágenes, constantes)
    tmp_tamano = (800, 600)
    resources = load_resources(tmp_tamano)

    Tamano = resources['consts']['Tamano']
    Ventana = pygame.display.set_mode(Tamano)
    clock = pygame.time.Clock()

    # Mostrar presentación y menú
    try:
        show_presentation(Ventana, clock, resources['images'].get('presentacion'), duration_ms=2000)
    except SystemExit:
        pygame.quit()
        return

    try:
        choice = show_menu(Ventana, clock, resources['images'].get('menu'), {**resources['consts'], 'Tamano': Tamano})
    except SystemExit:
        pygame.quit()
        return

    if choice == 'salir':
        pygame.quit()
        return
    if choice == 'ayuda':
        try:
            show_help_screen(Ventana, clock, resources['images'].get('ayuda'), resources['consts'])
            # volver al menu
            choice = show_menu(Ventana, clock, resources['images'].get('menu'), {**resources['consts'], 'Tamano': Tamano})
        except SystemExit:
            pygame.quit()
            return

    if choice == 'jugar':
        run_game(Ventana, clock, resources)


if __name__ == '__main__':
    main()
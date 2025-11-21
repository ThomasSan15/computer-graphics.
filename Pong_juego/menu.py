import pygame


def show_presentation(ventana, clock, image, duration_ms=2000):
    if image is None:
        # si no hay imagen, simplemente esperar
        start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start < duration_ms:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            clock.tick(30)
        return

    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < duration_ms:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        ventana.blit(image, (0, 0))
        pygame.display.flip()
        clock.tick(30)


def show_help_screen(ventana, clock, image, colors):
    Negro, Blanco = colors['Negro'], colors['Blanco']
    showing = True
    while showing:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN:
                showing = False
        ventana.fill(Negro)
        if image:
            ventana.blit(image, (0, 0))
        else:
            font = pygame.font.SysFont(None, 36)
            text = font.render('Ayuda - pulsa cualquier tecla o click para volver', True, Blanco)
            ventana.blit(text, (50, 280))
        pygame.display.flip()
        clock.tick(30)


def show_menu(ventana, clock, image, colors, offset=(-50,60)):
    """Muestra el menú.

    offset: tupla (offset_x, offset_y) para mover las cajas de los botones
    hacia la derecha (offset_x) y hacia abajo (offset_y).
    """
    # Definimos 3 rectángulos aproximados donde están las opciones en Menu.jpg
    Tamano = colors.get('Tamano', (800, 600))
    Negro, Blanco = colors['Negro'], colors['Blanco']
    btn_w, btn_h = 400, 100
    offset_x, offset_y = offset
    # Centrar horizontalmente y aplicar desplazamiento
    btn_x = (Tamano[0] - btn_w) // 2 + offset_x
    # Posición vertical inicial + desplazamiento
    first_y = 140 + offset_y
    spacing = 10
    btns = {
        'jugar': pygame.Rect(btn_x, first_y, btn_w, btn_h),
        'ayuda': pygame.Rect(btn_x, first_y + (btn_h + spacing), btn_w, btn_h),
        'salir': pygame.Rect(btn_x, first_y + 2 * (btn_h + spacing), btn_w, btn_h),
    }

    while True:
        mx, my = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for name, rect in btns.items():
                    if rect.collidepoint((mx, my)):
                        return name
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return 'salir'

        if image:
            ventana.blit(image, (0, 0))
        else:
            ventana.fill(Negro)

        for name, rect in btns.items():
            if rect.collidepoint((mx, my)):
                pygame.draw.rect(ventana, (200, 200, 200), rect, 4)
            if not image:
                pygame.draw.rect(ventana, (50, 50, 50), rect)
                font = pygame.font.SysFont(None, 48)
                label = 'Jugar Pong' if name == 'jugar' else ('Ayuda' if name == 'ayuda' else 'Salir')
                txt = font.render(label, True, Blanco)
                tx = rect.x + (rect.w - txt.get_width()) // 2
                ty = rect.y + (rect.h - txt.get_height()) // 2
                ventana.blit(txt, (tx, ty))

        pygame.display.flip()
        clock.tick(60)
        
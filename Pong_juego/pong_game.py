import pygame


def run_game(ventana, clock, resources):
    sounds = resources['sounds']
    images = resources['images']
    consts = resources['consts']

    COOLDOWN_MS = consts.get('COOLDOWN_MS', 120)
    last_play = {'raqueta': 0, 'rebote': 0, 'gol': 0}
    Negro = consts['Negro']
    Blanco = consts['Blanco']
    Tamano = consts['Tamano']
    PlayerAncho = consts['PlayerAncho']
    PlayerAlto = consts['PlayerAlto']

    # Coordenadas y velocidad del jugador 1
    CoorPlayer1_X = 50
    CoorPlayer1_Y = 300 - 45
    player1Vel_Y = 0

    # Coordenadas y velocidad del jugador 2
    CoorPlayer2_X = 750 - PlayerAncho
    CoorPlayer2_Y = 300 - 45
    Player2Vel_Y = 0

    # Coordenadas de la pelota
    Pelota_X = 400
    Pelota_Y = 300
    PelotaVel_X = 3
    PelotaVel_Y = 3

    # puntuaciones de los dos jugadores
    score_left = 0
    score_right = 0

    font = pygame.font.SysFont(None, 48)

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Jugador 1
                if event.key == pygame.K_w:
                    player1Vel_Y = -3
                if event.key == pygame.K_s:
                    player1Vel_Y = 3
                # Jugador 2
                if event.key == pygame.K_UP:
                    Player2Vel_Y = -3
                if event.key == pygame.K_DOWN:
                    Player2Vel_Y = 3

            if event.type == pygame.KEYUP:
                # Jugador 1
                if event.key == pygame.K_w:
                    player1Vel_Y = 0
                if event.key == pygame.K_s:
                    player1Vel_Y = 0
                # Jugador 2
                if event.key == pygame.K_UP:
                    Player2Vel_Y = 0
                if event.key == pygame.K_DOWN:
                    Player2Vel_Y = 0

        if Pelota_Y > 590 or Pelota_Y < 10:
            PelotaVel_Y *= -1
            # sonido de rebote en borde superior/inferior
            try:
                now = pygame.time.get_ticks()
                if sounds.get('rebote') and now - last_play['rebote'] > COOLDOWN_MS:
                    sounds['rebote'].play()
                    last_play['rebote'] = now
            except Exception:
                pass

        # Revisa si la pelota sale del lado derecho -> punto para el jugador izquierdo
        if Pelota_X > 800:
            # incrementar marcador izquierdo
            score_left += 1
            # sonido de gol
            try:
                now = pygame.time.get_ticks()
                if sounds.get('gol') and now - last_play['gol'] > COOLDOWN_MS:
                    sounds['gol'].play()
                    last_play['gol'] = now
            except Exception:
                pass
            
            if score_left >= 5 or score_right >= 5:
                winner = "Jugador 1" if score_left > score_right else "Jugador 2"
                fin = font.render(f"{winner} gana!", True, Blanco)
                ventana.blit(fin, (Tamano[0]//2 - fin.get_width()//2, 250))
                pygame.display.flip()
                pygame.time.wait(2000)
                game_over = True


            # reset pelota al centro
            Pelota_X = 400
            Pelota_Y = 300
            PelotaVel_X *= -1
            PelotaVel_Y *= -1
            # breve pausa mostrando marcador
            pause_start = pygame.time.get_ticks()
            while pygame.time.get_ticks() - pause_start < 800:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        raise SystemExit
                ventana.fill(Negro)
                # dibujar marcador
                left_surf = font.render(str(score_left), True, Blanco)
                right_surf = font.render(str(score_right), True, Blanco)
                ventana.blit(left_surf, (Tamano[0] // 4 - left_surf.get_width() // 2, 20))
                ventana.blit(right_surf, (3 * Tamano[0] // 4 - right_surf.get_width() // 2, 20))
                pygame.display.flip()
                clock.tick(30)

        # Revisa si la pelota sale del lado izquierdo -> punto para el jugador derecho
        if Pelota_X < 0:
            # incrementar marcador derecho
            score_right += 1
            # sonido de gol
            try:
                now = pygame.time.get_ticks()
                if sounds.get('gol') and now - last_play['gol'] > COOLDOWN_MS:
                    sounds['gol'].play()
                    last_play['gol'] = now
                    
            except Exception:
                pass
            if score_left >= 5 or score_right >= 5:
                winner = "Jugador 1" if score_left > score_right else "Jugador 2"
                fin = font.render(f"{winner} gana!", True, Blanco)
                ventana.blit(fin, (Tamano[0]//2 - fin.get_width()//2, 250))
                pygame.display.flip()
                pygame.time.wait(2000)
                game_over = True


            Pelota_X = 400
            Pelota_Y = 300
            PelotaVel_X *= -1
            PelotaVel_Y *= -1
            # breve pausa mostrando marcador
            pause_start = pygame.time.get_ticks()
            while pygame.time.get_ticks() - pause_start < 800:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        raise SystemExit
                ventana.fill(Negro)
                # dibujar marcador
                left_surf = font.render(str(score_left), True, Blanco)
                right_surf = font.render(str(score_right), True, Blanco)
                ventana.blit(left_surf, (Tamano[0] // 4 - left_surf.get_width() // 2, 20))
                ventana.blit(right_surf, (3 * Tamano[0] // 4 - right_surf.get_width() // 2, 20))
                pygame.display.flip()
                clock.tick(30)
        # Actualizar posiciones verticales de cada jugador según la tecla presionada
        CoorPlayer1_Y += player1Vel_Y
        CoorPlayer2_Y += Player2Vel_Y

        # Mantener las raquetas dentro del área jugable (límite superior e inferior)
        if CoorPlayer1_Y < 0:
            CoorPlayer1_Y = 0
        if CoorPlayer1_Y + PlayerAlto > Tamano[1]:
            CoorPlayer1_Y = Tamano[1] - PlayerAlto

        if CoorPlayer2_Y < 0:
            CoorPlayer2_Y = 0
        if CoorPlayer2_Y + PlayerAlto > Tamano[1]:
            CoorPlayer2_Y = Tamano[1] - PlayerAlto

        # Movimiento de la pelota con su velocidad actual
        Pelota_X += PelotaVel_X
        Pelota_Y += PelotaVel_Y

        ventana.fill(Negro)
        # Zona de dibujo
        jugador1 = pygame.draw.rect(ventana, Blanco, (CoorPlayer1_X, CoorPlayer1_Y, PlayerAncho, PlayerAlto))
        jugador2 = pygame.draw.rect(ventana, Blanco, (CoorPlayer2_X, CoorPlayer2_Y, PlayerAncho, PlayerAlto))
        pelota = pygame.draw.circle(ventana, Blanco, (Pelota_X, Pelota_Y), 10)

        # dibujar marcador en la parte superior
        score_font = pygame.font.SysFont(None, 60)

        # Render de ambos marcadores
        left_surf = score_font.render(str(score_left), True, Blanco)
        right_surf = score_font.render(str(score_right), True, Blanco)

        # Posición centrada sin fondo ni barra
        ventana.blit(left_surf, (Tamano[0] // 4 - left_surf.get_width() // 2, 15))
        ventana.blit(right_surf, (3 * Tamano[0] // 4 - right_surf.get_width() // 2, 15))

        # Separador central (delgado, no estorba la pelota)
        pygame.draw.rect(ventana, Blanco, (Tamano[0] // 2 - 3, 15, 6, 30))


        # Colisiones
        if pelota.colliderect(jugador1) or pelota.colliderect(jugador2):
            PelotaVel_X *= -1
            # sonido de impacto con la raqueta
            try:
                now = pygame.time.get_ticks()
                if sounds.get('raqueta') and now - last_play['raqueta'] > COOLDOWN_MS:
                    sounds['raqueta'].play()
                    last_play['raqueta'] = now
            except Exception:
                pass

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
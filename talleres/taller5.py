import pygame

#Ejercicio 1

def ejercicio_1():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Ejercicio 1 - Cambiar fondo con teclado")

    color = (255, 255, 255)  # blanco
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_SPACE:
                    color = (255, 255, 255)

        screen.fill(color)
        pygame.display.flip()

    pygame.quit()




# EJERCICIO 2


def ejercicio_2():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Ejercicio 2 - Formas con Mouse")

    shapes = []  

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if event.button == 1:  
                    shapes.append(("circle", x, y))
                elif event.button == 3:  
                    shapes.append(("square", x, y))
                elif event.button == 2:  
                    shapes.append(("triangle", x, y))

        screen.fill((255, 255, 255))

        for shape, x, y in shapes:
            if shape == "circle":
                pygame.draw.circle(screen, (0, 0, 255), (x, y), 20)
            elif shape == "square":
                pygame.draw.rect(screen, (255, 0, 0), (x - 20, y - 20, 40, 40))
            elif shape == "triangle":
                pygame.draw.polygon(screen, (0, 255, 0),
                                    [(x, y - 20), (x - 20, y + 20), (x + 20, y + 20)])

        pygame.display.flip()

    pygame.quit()

#Ejercicio3
def ejercicio_3():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Ejercicio 3 - Mini Paint")

    color = (0, 0, 0)
    size = 20
    shapes = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_c:
                    shapes.clear()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    size += 5
                elif event.key == pygame.K_MINUS:
                    size = max(5, size - 5)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if event.button == 1:
                    shapes.append(("circle", x, y, color, size))
                elif event.button == 3:
                    shapes.append(("square", x, y, color, size))

        screen.fill((255, 255, 255))

        for shape, x, y, c, s in shapes:
            if shape == "circle":
                pygame.draw.circle(screen, c, (x, y), s)
            elif shape == "square":
                pygame.draw.rect(screen, c, (x - s, y - s, s * 2, s * 2))

        pygame.display.flip()

    pygame.quit()



#Ejercicio4

def ejercicio_4():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Ejercicio 4 - Pincel Libre")

    drawing = False
    brush_size = 5
    color = (0, 0, 0)
    points = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    points.clear()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    brush_size += 1
                elif event.key == pygame.K_MINUS:
                    brush_size = max(1, brush_size - 1)

        if drawing:
            points.append((pygame.mouse.get_pos(), brush_size))

        screen.fill((255, 255, 255))

        for (x, y), s in points:
            pygame.draw.circle(screen, color, (x, y), s)

        pygame.display.flip()

    pygame.quit()


def main():
    print("Taller 5 - Pygame")
    print("1. Ejercicio 1 (Teclado)")
    print("2. Ejercicio 2 (Mouse)")
    print("3. Ejercicio 3 (Paint)")
    print("4. Ejercicio 4 (Pincel libre)")
    choice = input("Elige el ejercicio (1-4): ")

    if choice == "1":
        ejercicio_1()
    elif choice == "2":
        ejercicio_2()
    elif choice == "3":
        ejercicio_3()
    elif choice == "4":
        ejercicio_4()
    else:
        print("Opción inválida.")


if __name__ == "__main__":
    main()

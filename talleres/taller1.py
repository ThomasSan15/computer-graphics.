'''
Ejercicio 1: Variables y operadores
Crea un programa que pida al usuario dos números y muestre:
- La suma de los dos números.
- La multiplicación de los dos números.
- Si el primer número es mayor que el segundo.
'''
def ejercicio_1():
    print("Ingrese un número")
    numero1 = int(input())  # Sin argumento o con mensaje entre comillas
    print("Ingrese el segundo número")
    numero2 = int(input())

    print("Su suma es:", numero1 + numero2)
    print("Su multiplicación es:", numero1 * numero2)

    if numero1 > numero2:
        print("El primer número es mayor al segundo número")
    else:
        print("No es mayor el primer número al segundo número")

def ejercicio_2():
    print("Ingrese su edad:")
    edad = int(input())
    if edad <= 13:
        print("Usted es un niño")
    elif  13 < edad < 18:
        print("Usted es un adolescente")
    elif edad >= 18:
        print("Usted es un adulto")
    
def ejercicio_3():
    
    for i in range(1 , 20):
        if i % 3 == 0:
            continue
        else:
            print(i)
            
def ejercicio_4():
    print("Ingrese su nombre:")
    nombre = str(input())
    print("Ingrese su edad:")
    edad = int(input())
    print(f"hola {nombre}, tu edad en 5 años será {edad + 5}")

def problema_1():
    print("Ingrese el primer número:")
    num1 = float(input())

    print("Ingrese el segundo número:")
    num2 = float(input())

    print("¿Qué operación desea realizar? (+, -, *, /)")
    operacion = input()

    if operacion == "+":
        resultado = num1 + num2
    elif operacion == "-":
        resultado = num1 - num2
    elif operacion == "*":
        resultado = num1 * num2
    elif operacion == "/":
        if num2 != 0:
            resultado = num1 / num2
        else:
            print("Error: No se puede dividir entre cero.")
            return
    else:
        print("Operación no válida.")
        return

    print("El resultado es:", resultado)
    
def problema_2():
    tareas = []
    print("Ingresa tus tareas. Escribe 'salir' para terminar.")

    while True:
        tarea = input("Nueva tarea: ")
        if tarea.lower() == "salir":
            break
        tareas.append(tarea)

    print("\nTus tareas son:")
    for i, t in enumerate(tareas, 1):
        print(f"{i}. {t}")
        
def problema_3():
    
    print("Escribe una frase: ")
    frase = input()

    palabras = frase.split()
    total_palabras = len(palabras)
    total_letras = sum(len(palabra) for palabra in palabras if palabra.isalpha())
    palabra_mas_larga = max(palabras, key=len)

    print("Número total de palabras:", total_palabras)
    print("Número total de letras:", total_letras)
    print("Palabra más larga:", palabra_mas_larga)
    
def problema_4():
    print("Ingresa un número para mostrar su tabla de multiplicar: ")
    numero = int(input())
    print(f"Tabla del {numero}:")

    for i in range(1, 11):
        print(f"{numero} x {i} = {numero * i}")
        
def problema_5():
    frase = input("Escribe una frase: ").lower()

    vocales = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}
    total_vocales = 0

    for letra in frase:
        if letra in vocales:
            vocales[letra] += 1
            total_vocales += 1

    print("Total de vocales:", total_vocales)
    for vocal, cantidad in vocales.items():
        print(f"{vocal}: {cantidad}") 
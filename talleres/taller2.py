import numpy as np

"""Ejercicio 1: Creación de arrays
Crea un array 1D con los valores [12, 45, 78, 34, 56] y:
1. Muestra el array.
2. Muestra su tipo de datos (dtype).
3. Muestra el número de dimensiones (ndim) y su forma (shape)."""

def ejercicio1():
    array = np.array([12,45,78,34,56])
    print(array)
    print(array.dtype)
    print(array.ndim)
    print(array.shape)
    

"""Ejercicio 2: Arrays 2D y propiedades
Crea un array 2D con la siguiente lista de listas:
[[1, 2, 3],
[4, 5, 6],
[7, 8, 9]]
Luego:
1. Muestra el número de elementos (size).
2. Cambia el tipo de datos a float32.
3. Muestra el nuevo array."""

def ejercicio2():
    matriz = np.array([
        [1,2,3], 
        [4,5,6],
        [7,8,9]
    ])
    
    print(matriz.size)
    matriz = matriz.astype(np.float32)
    print(matriz)

"""
Usa funciones de NumPy para:
1. Crear un array de ceros de tamaño (2, 4).
2. Crear un array de unos de tamaño (3, 3).
3. Crear un array con valores del 10 al 50, con paso de 5.
4. Crear un array con 8 valores equidistantes entre 0 y 1."""

def ejercicio3():
    zeros = np.zeros((2,4))
    unos = np.ones((3,3))
    array = np.arange(10,51,5)
    array2 = np.linspace(0,1,8)

    print("array de ceros (2,4):")
    print(zeros)
    print("\narray de unos (3,3):")
    print(unos)
    print("\narray del 10 al 50 con paso 5:")
    print(array)
    print("\narray con 8 valores entre 0 y 1:")
    print(array2)

"""Crea dos arrays 1D:
- a con valores [2, 4, 6, 8, 10]
- b con valores [1, 3, 5, 7, 9]
Realiza y muestra:
1. Suma
2. Resta
3. Multiplicación elemento a elemento
4. División elemento a elemento"""
def ejercicio4():
    a = np.array([2,4,6,8,10])
    b = np.array([1,3,5,7,9])
    
    suma = a + b
    print("suma:", suma)
    resta = a - b
    print("resta:", resta)
    multiplicacion = a * b
    print("multiplicacion:", multiplicacion)
    division = a / b
    print("division:", division)
    
    """Crea un array con valores enteros del 1 al 20 y calcula:
1. La suma total.
2. El valor máximo y mínimo.
3. El promedio.
4. La desviación estándar (np.std())."""
def ejercicio5():
    array = np.arange(1,21)
    suma = np.sum(array)
    print("suma total:", suma)
    maximo = np.max(array)
    minimo = np.min(array)
    print("maximo:", maximo)
    print("minimo:", minimo)
    promedio = np.mean(array)
    print("promedio:", promedio)
    desviacion = np.std(array)
    print("desviacion estandar:", desviacion)
        
"""Dado el array:
[[5, 10, 15],
[20, 25, 30],
[35, 40, 45],
[50, 55, 60]]
Realiza:
1. Extrae la primera columna.
2. Extrae la tercera fila.
3. Obtén una submatriz de las últimas dos filas y las últimas dos columnas."""
def ejercicio6():
    array = np.array([[5, 10, 15],
    [20, 25, 30],
    [35, 40, 45],
    [50, 55, 60]])
    columna = array[:,0]
    print("primera columna:",columna)
    fila3 = array[2,:]
    print("tercera fila",fila3)
    sub = array[2:,1:]
    print("submatriz:", sub)
    
"""Usa np.random para:
1. Generar 10 números aleatorios entre 0 y 1.
2. Generar una matriz 4x4 con enteros aleatorios entre 50 y 100.
3. Generar 1000 valores con distribución normal y mostrar su promedio y desviación
estándar."""

def ejercicio7():
    rand_nums = np.random.rand(10)
    print("10 numeros aleatorios entre 0 y 1:")
    print(rand_nums)
    matriz = np.random.randint(50, 101, size=(4, 4))
    print("matriz 4x4 con enteros entre 50 y 100:")
    print(matriz)

    # 3. Generar 1000 valores con distribución normal
    valores_norm = np.random.randn(1000)
    promedio = np.mean(valores_norm)
    desviacion = np.std(valores_norm)
    print("promedio:", promedio)
    print("desviacion estandar:", desviacion)

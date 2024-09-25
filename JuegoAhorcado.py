import random
import time

# Definir los niveles de dificultad
NIVELES_DIFICULTAD = {
    'fácil': 8,
    'medio': 6,
    'difícil': 4
}

# Dibujos del ahorcado en ASCII
DIBUJOS_AHORCADO = [
    '''
     +---+
     |   |
         |
         |
         |
         |
    =========''', '''
     +---+
     |   |
     O   |
         |
         |
         |
    =========''', '''
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========''', '''
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========''', '''
     +---+
     |   |
     O   |1
    /|\\  |
         |
         |
    =========''', '''
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========''', '''
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    ========='''
]

# Cargar palabras desde un archivo para diferentes idiomas
def cargar_palabras(idioma):
    try:
        with open(f'palabras_{idioma}.txt', 'r', encoding='utf-8') as archivo:
            return archivo.read().splitlines()
    except FileNotFoundError:
        print(f"Archivo palabras_{idioma}.txt no encontrado. Verifica que esté en la misma carpeta que el script.")
        return []
    except UnicodeDecodeError:
        print(f"Error de codificación al leer el archivo palabras_{idioma}.txt. Asegúrate de que esté en UTF-8.")
        return []

# Seleccionar una palabra aleatoria
def seleccionar_palabra(palabras):
    return random.choice(palabras).lower()

# Juego principal con cuenta regresiva y manejo de puntajes
def jugar(partida, max_intentos):
    palabra_adivinada = "_" * len(partida)
    intentos = 0
    letras_adivinadas = []
    puntaje = 0
    tiempo_inicio = time.time()
    
    while intentos < max_intentos and "_" in palabra_adivinada:
        print(DIBUJOS_AHORCADO[intentos])
        print(f"Palabra: {palabra_adivinada}")
        print(f"Letras adivinadas: {', '.join(letras_adivinadas)}")
        print(f"Intentos restantes: {max_intentos - intentos}")
        
        # Tiempo restante (cuenta regresiva)
        tiempo_transcurrido = time.time() - tiempo_inicio
        tiempo_restante = max(0, 50 - int(tiempo_transcurrido))
        print(f"Tiempo restante: {tiempo_restante} segundos")
        
        if tiempo_restante == 0:
            print("¡Se acabó el tiempo!")
            break
        
        letra = input("Adivina una letra: ").lower()
        
        if letra in letras_adivinadas:
            print("Ya has adivinado esa letra. Intenta de nuevo.")
            continue
        
        letras_adivinadas.append(letra)
        
        if letra in partida:
            palabra_adivinada = ''.join([letra if partida[i] == letra else palabra_adivinada[i] for i in range(len(partida))])
            print("¡Correcto!")
        else:
            intentos += 1
            print("Incorrecto.")
    
    # Resultado al final del tiempo o intentos
    if "_" not in palabra_adivinada:
        puntaje += 10 * (max_intentos - intentos)  # Puntaje basado en los intentos restantes
        print(f"¡Ganaste! La palabra era '{partida}'. Tu puntaje: {puntaje}")
    else:
        print(DIBUJOS_AHORCADO[-1])
        print(f"¡Perdiste! La palabra era '{partida}'.")

    return puntaje

# Seleccionar nivel de dificultad
def elegir_dificultad():
    print("Selecciona un nivel de dificultad:")
    for nivel in NIVELES_DIFICULTAD:
        print(f"- {nivel}")
    
    dificultad = input().lower()
    return NIVELES_DIFICULTAD.get(dificultad, NIVELES_DIFICULTAD['fácil'])

# Seleccionar idioma
def elegir_idioma():
    idiomas = ['español', 'ingles', 'frances', 'aleman']
    print("Selecciona un idioma:")
    for idioma in idiomas:
        print(f"- {idioma}")
    
    idioma_seleccionado = input().lower()
    return idioma_seleccionado if idioma_seleccionado in idiomas else 'español'

# Manejo de jugadores (multijugador)
def juego_multijugador():
    jugadores = ['Jugador 1', 'Jugador 2']
    puntajes = {jugador: 0 for jugador in jugadores}
    rondas = 3

    idioma = elegir_idioma()
    palabras = cargar_palabras(idioma)
    
    if not palabras:
        print("No se encontraron palabras para el idioma seleccionado. Finalizando juego.")
        return

    for _ in range(rondas):
        for jugador in jugadores:
            print(f"\nTurno de {jugador}")
            palabra = seleccionar_palabra(palabras)
            max_intentos = elegir_dificultad()
            puntajes[jugador] += jugar(palabra, max_intentos)
    
    # Resultados finales
    print("\nResultados finales:")
    for jugador, puntaje in puntajes.items():
        print(f"{jugador}: {puntaje} puntos")

# Manejo de un jugador
def juego_un_jugador():
    idioma = elegir_idioma()
    palabras = cargar_palabras(idioma)

    if not palabras:
        print("No se encontraron palabras para el idioma seleccionado. Finalizando juego.")
        return

    palabra = seleccionar_palabra(palabras)
    max_intentos = elegir_dificultad()
    jugar(palabra, max_intentos)

# Menú principal
def menu_principal():
    print("¡Bienvenido al juego del Ahorcado!")
    print("Selecciona una opción:")
    print("1. Un jugador")
    print("2. Dos jugadores")
    
    opcion = input("Opción: ")
    if opcion == '1':
        juego_un_jugador()
    elif opcion == '2':
        juego_multijugador()
    else:
        print("Opción no válida. Por favor, elige 1 o 2.")

if __name__ == "__main__":
    menu_principal()

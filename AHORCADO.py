import random
import time

# Definir los niveles de dificultad
DIFFICULTY_LEVELS = {
    'facil': 8,
    'medio': 6,
    'dificil': 4
}

# Dibujos del ahorcado en ASCII
HANGMAN_PICS = [
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
def load_words(language):
    try:
        with open(f'words_{language}.txt', 'r', encoding='utf-8') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f"Archivo words_{language}.txt no encontrado. Verifica que esté en la misma carpeta que el script.")
        return []
    except UnicodeDecodeError:
        print(f"Error de codificación al leer el archivo words_{language}.txt. Asegúrate de que esté en UTF-8.")
        return []

# Seleccionar una palabra aleatoria
def select_word(words):
    return random.choice(words).lower()

# Juego principal con cuenta regresiva y manejo de puntajes
def play_game(word, max_attempts):
    guessed = "_" * len(word)
    attempts = 0
    guessed_letters = []
    score = 0
    start_time = time.time()
    
    while attempts < max_attempts and "_" in guessed:
        print(HANGMAN_PICS[attempts])
        print(f"Palabra: {guessed}")
        print(f"Letras adivinadas: {', '.join(guessed_letters)}")
        print(f"Intentos restantes: {max_attempts - attempts}")
        
        # Tiempo restante (cuenta regresiva)
        elapsed_time = time.time() - start_time
        time_left = max(0, 50 - int(elapsed_time))
        print(f"Tiempo restante: {time_left} segundos")
        
        if time_left == 0:
            print("¡Se acabó el tiempo!")
            break
        
        guess = input("Adivina una letra: ").lower()
        
        if guess in guessed_letters:
            print("Ya has adivinado esa letra. Intenta de nuevo.")
            continue
        
        guessed_letters.append(guess)
        
        if guess in word:
            guessed = ''.join([guess if word[i] == guess else guessed[i] for i in range(len(word))])
            print("¡Correcto!")
        else:
            attempts += 1
            print("Incorrecto.")
    
    # Resultado al final del tiempo o intentos
    if "_" not in guessed:
        score += 10 * (max_attempts - attempts)  # Puntaje basado en los intentos restantes
        print(f"¡Ganaste! La palabra era '{word}'. Tu puntaje: {score}")
    else:
        print(HANGMAN_PICS[-1])
        print(f"¡Perdiste! La palabra era '{word}'.")

    return score

# Seleccionar nivel de dificultad
def choose_difficulty():
    print("Selecciona un nivel de dificultad:")
    for level in DIFFICULTY_LEVELS:
        print(f"- {level}")
    
    difficulty = input().lower()
    return DIFFICULTY_LEVELS.get(difficulty, DIFFICULTY_LEVELS['fácil'])

# Seleccionar idioma
def choose_language():
    languages = ['español', 'ingles', 'frances', 'aleman']
    print("Selecciona un idioma:")
    for lang in languages:
        print(f"- {lang}")
    
    language = input().lower()
    return language if language in languages else 'español'

# Manejo de jugadores (multijugador)
def multiplayer_game():
    players = ['Jugador 1', 'Jugador 2']
    scores = {player: 0 for player in players}
    rounds = 3

    language = choose_language()
    words = load_words(language)
    
    if not words:
        print("No se encontraron palabras para el idioma seleccionado. Finalizando juego.")
        return

    for _ in range(rounds):
        for player in players:
            print(f"\nTurno de {player}")
            word = select_word(words)
            max_attempts = choose_difficulty()
            scores[player] += play_game(word, max_attempts)
    
    # Resultados finales
    print("\nResultados finales:")
    for player, score in scores.items():
        print(f"{player}: {score} puntos")

# Manejo de un jugador
def single_player_game():
    language = choose_language()
    words = load_words(language)

    if not words:
        print("No se encontraron palabras para el idioma seleccionado. Finalizando juego.")
        return

    word = select_word(words)
    max_attempts = choose_difficulty()
    play_game(word, max_attempts)

# Menú principal
def main_menu():
    print("¡Bienvenido al juego del Ahorcado!")
    print("Selecciona una opción:")
    print("1. Un jugador")
    print("2. Dos jugadores")
    
    choice = input("Opción: ")
    if choice == '1':
        single_player_game()
    elif choice == '2':
        multiplayer_game()
    else:
        print("Opción no válida. Por favor, elige 1 o 2.")

if __name__ == "__main__":
    main_menu()

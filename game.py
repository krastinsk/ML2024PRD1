import random

def generate_numbers():
    valid_numbers = []
    while len(valid_numbers) < 5:
        num = random.randint(10000, 20000)
        if num % 2 == 0 and num % 3 == 0:
            valid_numbers.append(num)
    return valid_numbers


def player_choice(numbers):
    print("Izvēlies skaitli, ar kuru vēlies sākt spēli:")
    for i, num in enumerate(numbers):
        print(f"{i + 1}. {num}")
    choice = int(input("Tava izvēle (1-5): ")) - 1
    return numbers[choice]

def determine_first_player():
    player_input = int(input("Izvēlieties, kurš sāks spēli (0 - Spēlētājs 1, 1 - Bots): "))
    if player_input == 0:
        return "player"
    elif player_input == 1:
        return "bot"
    else:
        print("Nepareiza izvēle. Mēģiniet vēlreiz.")
        return determine_first_player()

def bot_choice(current_number):
    if current_number % 2 == 0:
        return 2
    else:
        return 3

def select_ai_algorithm():
    ai_input = int(input("Izvēlieties botu algoritmu (0 - Alpha-Beta, 1 - Min-Max): "))
    if ai_input == 0:
        return "Alpha-Beta"
    elif ai_input == 1:
        return "Min-Max"
    else:
        print("Nepareiza izvēle. Mēģiniet vēlreiz.")
        return select_ai_algorithm()

def play_game(starting_number, first_player):
    player1_points = 0
    player2_points = 0
    current_number = starting_number
    player_turn = first_player
    while current_number > 10:
        if player_turn == "player":
            divisor = int(input(f"Izvēlies, ar ko dalīt skaitli {current_number} (2 vai 3): "))
        else:
            divisor = bot_choice(current_number)
            print(f"Bot chooses to divide {current_number} by {divisor}")
        if divisor not in (2, 3):
            print("Var dalīt tikai ar 2 vai 3!")
            continue
        if current_number % divisor == 0:
            if divisor == 2:
                player2_points += 2
            else:
                player1_points += 3
            current_number //= divisor
            print(f"Punkti: Spēlētājs 1 - {player1_points}, Spēlētājs 2 - {player2_points}")
        else:
            print("Nederīga izvēle, mēģini vēlreiz.")
            break  # End the game if the number cannot be divided evenly
        if player_turn == "player":
            player_turn = "bot"
        else:
            player_turn = "player"
    print("Spēle beigusies!")
    print(f"Galīgais rezultāts: Spēlētājs 1 - {player1_points}, Spēlētājs 2 - {player2_points}")
    if player1_points == player2_points:
        print(f"{current_number} Spēles beigu skaitlis!")
        print("Neizšķirts!")
    else:
        print(f"{current_number} Spēles beigu skaitlis!")
        winner = "Spēlētājs 1" if player1_points > player2_points else "Spēlētājs 2"
        print(f"{winner} uzvar ar rezultātu: {max(player1_points, player2_points)}")

def main():
    print("Sveiki! Šī ir spēle, kurā jums jāizdala skaitlis ar 2 vai 3, kamēr tas ir lielāks par vai vienāds ar 10.")

    while True:

        numbers = generate_numbers()
        starting_number = player_choice(numbers)
        first_player = determine_first_player()
        ai_algorithm = select_ai_algorithm()
        print(f"{first_player.capitalize()} starts the game.")
        play_game(starting_number, first_player)
    
        play_again = input("Vai vēlaties sākt spēli no jauna? (0 - Jā, 1 - Nē): ")
        if play_again == "1":
            break  # Exit the loop if the player chooses not to play again
        elif play_again == "0":
            continue  # Continue to the next iteration of the loop to start a new game

if __name__ == "__main__":
    main()

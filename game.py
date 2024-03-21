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

def play_game(starting_number):
    player1_points = 0
    player2_points = 0
    current_number = starting_number
    while current_number >= 10:
        divisor = int(input(f"Izvēlies, ar ko dalīt skaitli {current_number} (2 vai 3): "))
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
    numbers = generate_numbers()
    starting_number = player_choice(numbers)
    play_game(starting_number)

if __name__ == "__main__":
    main()
import ui_gui
import game

class GameNode:
  def __init__(self, number, player1_score, player2_score):
      self.number = number
      self.player1_score = player1_score
      self.player2_score = player2_score

  def is_terminal(self):
      return self.number <= 10

  def evaluate(self, move):
    if self.is_terminal():  #Koku galotņu novērtējumu atšķirība no tā vai tie ved uz 3 vai 2
        if move == 3:
            multiplier = 1.3  
            result = (self.player1_score - self.player2_score) * multiplier
            print(f"Multiplying by {multiplier}, resulting in {result}")
            return result
        elif move == 2:
            multiplier = 0.7
            result = (self.player1_score - self.player2_score) * multiplier
            print(f"Multiplying by {multiplier}, resulting in {result}")
            return result
    else:
        if move == 3:   #Gadījums kad tu piespied pretiniekam izvēlēties 2 nākošajā gājienā
            verygoodmove = round(self.number + 1 / 3)
            #print("very good move", verygoodmove)
            if verygoodmove % 2 == 0 and verygoodmove % 3 != 0:
                multiplier = 1.5
                result = (self.player1_score - self.player2_score) * multiplier
                print(f"Multiplying by {multiplier}, resulting in {result}")
            else: 
                multiplier = 1.3
                result = (self.player1_score - self.player2_score) * multiplier
                print(f"Multiplying by {multiplier}, resulting in {result}")
        elif move == 2:
            multiplier = 0.7
            result = (self.player1_score - self.player2_score) * multiplier
            print(f"Multiplying by {multiplier}, resulting in {result}")
            return result
        

  def get_possible_moves(self):
      moves = []
      if self.number % 2 == 0:
          moves.append(2)
      if self.number % 3 == 0:
          moves.append(3)
      return moves

  def make_move(self, move, current_player):
      new_number = self.number // move
      new_player1_score = self.player1_score
      new_player2_score = self.player2_score
      if move == 2:
          if current_player == 1:
              new_player2_score += 2
          else:
              new_player1_score += 2
      elif move == 3:
          if current_player == 1:
              new_player1_score += 3
          else:
              new_player2_score += 3
      return GameNode(new_number, new_player1_score, new_player2_score)

def make_best_move(node, depth, current_player):
  if current_player == 1:
    _, best_move, _ = alpha_beta(node, depth, float('-inf'), float('inf'), True)
  else:
    _, best_move, _ = alpha_beta(node, depth, float('-inf'), float('inf'), False)
  return node


## Словарь для хранения предыдущих эвристических оценок
previous_evaluations = {}

def alpha_beta(node, depth, alpha, beta, maximizing_player):
  if depth == 0 or node.is_terminal():
      return node.evaluate(), None, []

  # Пункт 3: Проверка наличии предыдущей эвристической оценки для этого узла
  if node in previous_evaluations:
      return previous_evaluations[node], None, []

  if maximizing_player:
      max_eval = float('-inf')
      best_move = None
      best_path = []
      for move in node.get_possible_moves():
          child_node = node.make_move(move, 2)
          eval, _, path = alpha_beta(child_node, depth - 1, alpha, beta, False)
          path = [move] + path
          if eval > max_eval:
              max_eval = eval
              best_move = move
              best_path = path
          alpha = max(alpha, eval)
          if beta <= alpha:
              break
      if max_eval >= beta:
          return float('inf'), best_move, best_path
      # Пункт 4 и 5: Сохранение эвристической оценки для этого узла
      previous_evaluations[node] = max_eval
      return max_eval, best_move, best_path
  else:
      min_eval = float('inf')
      best_move = None
      best_path = []
      for move in node.get_possible_moves():
          child_node = node.make_move(move, 1)
          eval, _, path = alpha_beta(child_node, depth - 1, alpha, beta, True)
          path = [move] + path
          if eval < min_eval:
              min_eval = eval
              best_move = move
              best_path = path
          beta = min(beta, eval)
          if beta <= alpha:
              break
      if min_eval <= alpha:
          return float('-inf'), best_move, best_path
      # Пункт 4 и 5: Сохранение эвристической оценки для этого узла
      previous_evaluations[node] = min_eval
      return min_eval, best_move, best_path

def generate_game_tree(starting_number):
    node = GameNode(starting_number, 0, 0)
    game_tree = {}

    def build_tree(current_node, level):
        if current_node.is_terminal():
            return

        possible_moves = current_node.get_possible_moves()
        for move in possible_moves:
            new_node = current_node.make_move(move, 1)
            game_tree[(current_node.number, move)] = (new_node, level)
            build_tree(new_node, level + 1)

    build_tree(node, 0)
    return game_tree


def print_game_tree(game_tree):
    print("Game Tree:")
    for key, value in game_tree.items():
        parent = key
        child, level = value
        print(f"Level {level}: Parent: {parent}, Child: {child.number}")


def choose_starter():
    while True:
        choice = input("Who starts the game? Enter 'user' for user or 'ai' for AI: ").lower()
        if choice == 'user':
            return 1
        elif choice == 'ai':
            return 2
        else:
            print("Invalid choice! Please enter 'user' or 'ai'.")


def generate_numbers():
    valid_numbers = []
    num1 = 15552
    num2 = 14244
    num3 = 12000
    num4 = 16836
    num5 = 18006
    valid_numbers.append(num1)
    valid_numbers.append(num2)
    valid_numbers.append(num3)
    valid_numbers.append(num4)
    valid_numbers.append(num5)
    return valid_numbers


def player_choice(numbers):
    print("Choose one of the following numbers to start the game:")
    for i, num in enumerate(numbers):
        print(f"{i + 1}. {num}")
    choice = int(input("Enter the number of your choice: ")) - 1
    while choice not in range(5):
        print("Invalid choice! Choose from the given options.")
        choice = int(input("Enter the number of your choice: ")) - 1
    return numbers[choice]

## print эвристической оценки
def print_evaluation(node):
  eval = node.evaluate()
  print("Evaluation result:", eval)


def play_game(starting_number, depth, starting_player, game_tree):
    node = GameNode(starting_number, 0, 0)
    current_player = starting_player

    # Generate and print initial subtree
    print("Initial Subtree:")
    initial_subtree = generate_subtree(node, depth)
    print_subtree(initial_subtree)

    while not node.is_terminal():
        print("Current number:", node.number)
        print("Current player 1 (YOU) score:", node.player1_score)
        print("Current player 2 (AI) score:", node.player2_score)
        print("Player", current_player, "'s turn")

        possible_moves = node.get_possible_moves()
        if not possible_moves:
            break

        if current_player == 1:
            print("Possible moves:", possible_moves)
            chosen_move = int(input("Choose a move: "))
            while chosen_move not in possible_moves:
                print("Invalid move! Choose from possible moves.")
                chosen_move = int(input("Choose a move: "))
        else: 
            if (node.number, 3) in game_tree:
                chosen_move = 3 # PASAKA AR KURU KUSTĪBU VAJAG SĀKT KOKA NOVĒRTĒŠANUUUUUUUUUU
            else:
                print("Invalid starting number")

            print("AI chooses move:", chosen_move)

        node = node.make_move(chosen_move, current_player)
        current_player = 2 if current_player == 1 else 1

        # Pass chosen move to evaluate method
        evaluation = node.evaluate(chosen_move)
        print("Evaluation result:", evaluation)

        # Generate and print subtree from the current node onwards for both players
        subtree = generate_subtree(node, depth)
        print_subtree(subtree)

    print("Game Over")
    print("Final number:", node.number)
    print("Final player 1 (YOU) score:", node.player1_score)
    print("Final player 2 (AI) score:", node.player2_score)
    print("Evaluation result:", eval)


    if node.is_terminal():
        if node.player1_score > node.player2_score:
            print("You win!")
        elif node.player1_score < node.player2_score:
            print("AI wins!")
        else:
            print("It's a draw!")
    else:
        if node.player1_score > node.player2_score:
            print("You win! (No possible moves left)")
        elif node.player1_score < node.player2_score:
            print("AI wins! (No possible moves left)")
        else:
            print("It's a draw! (No possible moves left)")



def generate_subtree(node, depth):
    subtree = {}
    build_tree(node, 0, subtree, depth)
    return subtree


def build_tree(current_node, level, subtree, depth):
    if level > depth or current_node.is_terminal():
        return

    possible_moves = current_node.get_possible_moves()
    for move in possible_moves:
        new_node = current_node.make_move(move, 1)
        subtree[(current_node.number, move)] = (new_node, level)
        build_tree(new_node, level + 1, subtree, depth)

    # Also build subtree for AI player
    for move in possible_moves:
        new_node = current_node.make_move(move, 2)
        subtree[(current_node.number, move)] = (new_node, level)
        build_tree(new_node, level + 1, subtree, depth)


def print_subtree(subtree):
    print("Subtree:")
    for key, value in subtree.items():
        parent = key
        child, level = value
        print(f"Level {level}: Parent: {parent}, Child: {child.number}")


def main():
    print("Sveiki! Šī ir spēle, kurā jums jāizdala skaitlis ar 2 vai 3, kamēr tas ir lielāks par vai vienāds ar 10.")
    numbers = generate_numbers()
    starting_player = choose_starter()
    if starting_player == 1:
        starting_number = player_choice(numbers)
    else:
        starting_number = player_choice(numbers)
        print("You have chosen the starting number:", starting_number)
    depth = 5

    # Generate the game tree at the start of the game
    game_tree = generate_game_tree(starting_number)

    play_game(starting_number, depth, starting_player, game_tree)


if __name__ == "__main__":
    main()

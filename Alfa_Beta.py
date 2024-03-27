import random
#--------------------------------------------------------------
class GameNode:
    def __init__(self, number, player1_score, player2_score): # inicialization of attributes
        self.number = number 
        self.player1_score = player1_score  #user
        self.player2_score = player2_score  #ai

    def is_terminal(self): # if game number is less or equal to 10, than game cannot continue
        return self.number <= 10 # true when game cannot continue, otherwise false

    def evaluate(self): 
        if self.player1_score > self.player2_score: 
            return float('inf') # float('inf') because Python's built-in support for floating-point is highly optimized and will work faster
        elif self.player1_score < self.player2_score: 
            return float('-inf') # instead we can use here just integers with maximal or minimal value
        else: 
            return 0 

    def get_possible_moves(self):  # check for possible moves
        moves = [] 
        if self.number % 2 == 0:  
            moves.append(2)  
        if self.number % 3 == 0:  
            moves.append(3)  
        return moves 

    def make_move(self, move, current_player):  # number division and boint adding
        new_number = self.number // move  # ensure that the number is always integer
        new_player1_score = self.player1_score  
        new_player2_score = self.player2_score  
        if move == 2:  
            if current_player == 1: 
                new_player1_score += 2 
            else:  
                new_player2_score += 2 
        elif move == 3: 
            if current_player == 1:  
                new_player1_score += 3 
            else:  
                new_player2_score += 3  
        return GameNode(new_number, new_player1_score, new_player2_score)  
#--------------------------------------------------------------
#--------------------------------------------------------------
def alpha_beta(node, depth, alpha, beta, maximizing_player):  
    #stops game when no moves can be made 
    if depth == 0 or node.is_terminal():  
        return node.evaluate(), None  

    if maximizing_player: 
        max_eval = float('-inf')  
        best_move = None  
        for move in node.get_possible_moves():  # iterates over all possible moves
            child_node = node.make_move(move, 2)  # new game node made by ai (maximizing player))
            eval = alpha_beta(child_node, depth - 1, alpha, beta, False)[0] # function call 
            if eval > max_eval: 
                max_eval = eval  
                best_move = move  # move that leads to the best score
                alpha = max(alpha, eval) # updates alpha with max value between alpha and eval
        return max_eval, best_move  
      
    else:  
        min_eval = float('inf')  
        best_move = None  
        for move in node.get_possible_moves():  
            child_node = node.make_move(move, 1)  
            eval = alpha_beta(child_node, depth - 1, alpha, beta, True)[0]  
            if eval < min_eval:  
                min_eval = eval 
                best_move = move  
                beta = min(beta, eval)  
        return min_eval, best_move  
#--------------------------------------------------------------
def generate_numbers(): # X
    valid_numbers = []
    while len(valid_numbers) < 5:
        num = random.randint(10000, 20000)
        if num % 2 == 0 and num % 3 == 0:
            valid_numbers.append(num)
    return valid_numbers

def player_choice(numbers): # X
    print("Choose one of the following numbers to start the game:")
    for i, num in enumerate(numbers):
        print(f"{i+1}. {num}") 
    choice = int(input("Enter the number of your choice: ")) - 1
    while choice not in range(5):
        print("Invalid choice! Choose from the given options.")
        choice = int(input("Enter the number of your choice: ")) - 1
    return numbers[choice]

def play_game(starting_number, depth): 
    node = GameNode(starting_number, 0, 0) # starting points - 0 : 0 
    current_player = 1  # user starts

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
            evaluation_result = alpha_beta(node, depth, float('-inf'), float('inf'), True)
            chosen_move = evaluation_result[1] 
            if chosen_move is None:  
                chosen_move = possible_moves[0]  
            print("AI chooses move:", chosen_move)  

        node = node.make_move(chosen_move, current_player)  
        current_player = 2 if current_player == 1 else 1  
        print()

    print("Game Over") 
    print("Final number:", node.number) 
    print("Final player 1 (YOU) score:", node.player1_score) 
    print("Final player 2 (AI) score:", node.player2_score) 

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

def main(): # X
    print("Sveiki! Šī ir spēle, kurā jums jāizdala skaitlis ar 2 vai 3, kamēr tas ir lielāks par vai vienāds ar 10.")
    numbers = generate_numbers()
    starting_number = player_choice(numbers)
    depth = 5  
    play_game(starting_number, depth)

if __name__ == "__main__":
    main()

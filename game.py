import random
import sys
import Alfa_Beta
import minimax
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

def generate_numbers():
    valid_numbers = []
    while len(valid_numbers) < 5:
        num = random.randint(10000, 20000)
        if num % 2 == 0 and num % 3 == 0:
            valid_numbers.append(num)
    return valid_numbers
    
def dividesByTwo(number: int):
    if number % 2 == 0:
        return True
    else:
        return False
    
def dividesByThree(number: int):
    if number % 3 == 0:
        return True
    else:
        return False
    
def dividesAtAll(number: int):
    if number % 2 == 0 or number % 3 == 0:
        return True
    else:
        return False
    
# datu drošība nav aktuāla problēma
class dataCollect():
    def __init__(self, algorithm: str = None, startingPlayer: str = None, startingNumber: int = None):
        self.algorithm = algorithm
        self.startingPlayer = startingPlayer
        self.startingNumber = startingNumber
        
#globālie minimax
globalDataCollector = dataCollect()
minimaxAIMoveset = None
minimaxCompleteMoveset = None
globalminmaxGameTree = None
list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42 = []

#globālie alfabeta
# alfabetaGameTree = {}
# alfabetaNode = None

def parseAndRunAlgo(globalDataCollector: dataCollect):
    """
    input: object
    output: list, list, list

    Funkcija izvelk gājienus balstoties uz minimax algoritmu.
    """
    match globalDataCollector.algorithm:
        case "minimax":
            match globalDataCollector.startingPlayer:
                case "human":
                    game_tree = minimax.generateGameTree(globalDataCollector.startingNumber, 1)
                    minimax_result = minimax.minimax(game_tree, 0, 1)
                    return [minimax.filterAIMoves(minimax_result[1], 1), minimax_result[1], minimax_result[2]]
                case "ai":
                    game_tree = minimax.generateGameTree(globalDataCollector.startingNumber, -1)
                    minimax_result = minimax.minimax(game_tree, 0, -1)
                    return [minimax.filterAIMoves(minimax_result[1], -1), minimax_result[1], minimax_result[2]]
        case "alfabeta":
            return [[],[],[]]

def minimaxSoWhoIsThePlayer(player: str):
    if player == "human":
        return 1
    elif player == "ai":
        return -1
    else:
        return 42 #joks

def alfabetaSoWhoIsThePlayer(player: str):
    if player == "human":
        return 1
    elif player == "ai":
        return 2
    else:
        return 42 #joks

"""
TODO: MAKE UI FOR THE GAME
ko vajag: 
4. play game:
        skaitlis (1 QLabel/ 1 QSpinBox)
        speletaju punkti (2 QLCDNumber)
        2 buttons (2 QPushButton)
        teksts kas pasaka kas ir noticis (1 QLabel)
5. end game if no moves left
6. button for playing again (change settings)
"""
        
class ChooseAI(QWidget):
    def __init__(self, processStack: QStackedWidget):
        super().__init__()
        
        self.index = 0
        self.processStack = processStack
        
        # Layout for selecting algorithm
        self.selectAI_layout = QVBoxLayout()
        self.setLayout(self.selectAI_layout)
        #self.selectAI.setLayout(self.selectAI_layout)
        
        self.selectAI_layout.addWidget(QLabel("Izvēlies algoritmu"))
        
        self.minimax_button = QPushButton("Minimax")
        self.selectAI_layout.addWidget(self.minimax_button)
        self.minimax_button.clicked.connect(self.on_minimax_clicked)

        self.alphabeta_button = QPushButton("Alfa-Beta")
        self.selectAI_layout.addWidget(self.alphabeta_button)
        self.alphabeta_button.setEnabled(False)
        
        #this never happens, button is locked.
        self.alphabeta_button.clicked.connect(self.on_alphabeta_clicked)
        
    def on_minimax_clicked(self):
        print("Minimax button clicked!")
        global globalDataCollector
        globalDataCollector.algorithm = "minimax"
        self.processStack.setCurrentIndex(1)

    def on_alphabeta_clicked(self):
        print("Alfa-Beta button clicked!")
        global globalDataCollector
        globalDataCollector.algorithm = "alfabeta"
        self.processStack.setCurrentIndex(1)
            
class ChoosePlayer(QWidget):
    def __init__(self, processStack: QStackedWidget):
        super().__init__()
        
        self.index = 1
        self.processStack = processStack
        
        # Layout for selecting algorithm
        self.selectPlayer_layout = QVBoxLayout()
        self.setLayout(self.selectPlayer_layout)
        #self.selectPlayer.setLayout(self.selectPlayer_layout)
        
        self.selectPlayer_layout.addWidget(QLabel("Izvēlies kurš sāks"))
        
        self.humanPlayer = QPushButton("Cilvēks")
        self.selectPlayer_layout.addWidget(self.humanPlayer)
        self.humanPlayer.clicked.connect(self.on_humanPlayer_clicked)

        self.artificialInellect = QPushButton("Mākslīgais Intelekts")
        self.selectPlayer_layout.addWidget(self.artificialInellect)
        self.artificialInellect.clicked.connect(self.on_artificialIntellect_clicked)
        
    def on_humanPlayer_clicked(self):
        print("Izvēlēts cilvēks.")
        global globalDataCollector
        globalDataCollector.startingPlayer = "human"
        self.processStack.setCurrentIndex(2)

    def on_artificialIntellect_clicked(self):
        print("Izvēlēts mākslīgais intelekts.")
        global globalDataCollector
        globalDataCollector.startingPlayer = "ai"
        self.processStack.setCurrentIndex(2)
            
class NumberButton(QWidget):
    number_clicked = Signal(int)

    def __init__(self, number, processStack: QStackedWidget ):
        super().__init__()
        self.number = number
        self.processStack = processStack

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.button = QPushButton(f"{self.number}")
        self.button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.button)

    def on_button_clicked(self):
        self.processStack.setCurrentIndex(3)
        global globalDataCollector
        global minimaxAIMoveset
        global minimaxCompleteMoveset
        global globalminmaxGameTree
        globalDataCollector.startingNumber = self.number
        minimaxAIMoveset, minimaxCompleteMoveset, globalminmaxGameTree = parseAndRunAlgo(globalDataCollector)
        print(f"rational moveset: {minimaxCompleteMoveset}") #debug
        self.number_clicked.emit(self.number)
        self.processStack.widget(3).divByTwo.setEnabled(True)
        self.processStack.widget(3).divByThree.setEnabled(True)
        if (globalDataCollector.algorithm == "minimax"):
            if (globalDataCollector.startingPlayer == "ai"):
                self.processStack.widget(3).aiStartInitialization()
        else:
            if (globalDataCollector.startingPlayer == "ai"):
                #TODO: alfabeta kas ja sāk MI
                pass
        
        #global alfabetaGameTree
        #alfabetaGameTree = Alfa_Beta.Speles_koka_veidoshana(globalDataCollector.startingNumber)
        #global alfabetaNode
        #alfabetaNode = Alfa_Beta.Speles_stavokli(globalDataCollector.startingNumber, 0, 0)
        
        #nosūta datus savienotajām funkcijām      

class ChooseNumber(QWidget):
    def __init__(self, processStack: QStackedWidget):
        super().__init__()

        self.index = 2
        self.processStack = processStack

        self.numbers = generate_numbers()

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        
        self.label = QLabel("Choose a Number:", self)
        self.layout.addWidget(self.label)

        # Add buttons for each number
        for number in self.numbers:
            button = NumberButton(number, processStack)
            button.number_clicked.connect(self.transmit_number)
            self.layout.addWidget(button)
            
    def transmit_number(self, number):
        self.processStack.currentWidget().receive_number(number)
        
class PlayGame(QWidget):
    game_ended = Signal(int)
    global globalDataCollector
    global minimaxCompleteMoveset
    global minimaxAIMoveset
    
    def __init__(self, processStack: QStackedWidget):
        super().__init__()
        
        self.index = 3
        self.processStack = processStack
        
        self.layout = QVBoxLayout(self)
        
        self.numberLabel = QLabel("Šobrīdējais skaitlis:", self)
        self.numberDisplay = QLCDNumber(5,self)
        self.layout.addWidget(self.numberLabel)
        self.layout.addWidget(self.numberDisplay)
        
        self.humanPointsLabel = QLabel("Cilvēka spēlētāja punkti:", self)
        self.humanPoints = QLCDNumber(2,self)
        self.layout.addWidget(self.humanPointsLabel)
        self.layout.addWidget(self.humanPoints)
        
        self.aiPointsLabel = QLabel("Mākslīgā intelekta punkti:", self)
        self.aiPoints = QLCDNumber(2,self)
        self.layout.addWidget(self.aiPointsLabel)
        self.layout.addWidget(self.aiPoints)
        
        self.enemyMovesLabel = QLabel("Pretinieka pēdējais gājiens:", self)
        self.layout.addWidget(self.enemyMovesLabel)
        
        self.movesLabel = QLabel("Gājieni:", self)
        self.layout.addWidget(self.movesLabel)
        self.buttonContainer = QHBoxLayout(self)
        self.divByTwo = QPushButton("/2")
        self.buttonContainer.addWidget(self.divByTwo)
        self.divByTwo.clicked.connect(self.ondivByTwo_clicked)
        self.divByThree = QPushButton("/3")
        self.buttonContainer.addWidget(self.divByThree)
        self.divByThree.clicked.connect(self.ondivByThree_clicked)
        self.layout.addLayout(self.buttonContainer)
        
    def receive_number(self, number):
        self.numberDisplay.display(number)
        
    def aiStartInitialization(self):
        global globalDataCollector
        global minimaxCompleteMoveset
        global minimaxAIMoveset
        aiMove = minimaxAIMoveset.pop()
        minimaxCompleteMoveset.pop()
        print(f"rational moveset: {minimaxCompleteMoveset}") #debug
        print
        curVal = self.numberDisplay.intValue()
        curVal = curVal / aiMove
        self.numberDisplay.display(curVal)
        self.enemyMovesLabel.setText(f"Pretinieka pēdējais gājiens: {aiMove}")
        if aiMove == 2:
            humanScore = self.humanPoints.intValue()
            humanScore = humanScore + aiMove
            self.humanPoints.display(humanScore)
            list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42.append(aiMove)
            if not dividesAtAll(curVal):
                self.gameEnd()
                
        else:
            aiScore = self.aiPoints.intValue()
            aiScore = aiScore + aiMove
            self.humanPoints.display(aiScore)
            list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42.append(aiMove)
            if not dividesAtAll(curVal):
                self.gameEnd()
    
    def ondivByTwo_clicked(self):
        global globalDataCollector
        global minimaxCompleteMoveset
        global minimaxAIMoveset
        global list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42
        self.divByThree.setEnabled(False)
        
        aiScore = self.aiPoints.intValue()
        aiScore = aiScore + 2
        self.aiPoints.display(aiScore)
        
        curVal = self.numberDisplay.intValue()
        curVal = curVal / 2
        #pārbauda vai gājiens ir racionāls
        curMove = minimaxCompleteMoveset.pop()
        print(f"rational moveset: {minimaxCompleteMoveset}") #debug
        
        list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42.append(2)
        match globalDataCollector.algorithm:
            case "minimax":
                if curMove == 2:
                    #spēlētāja gājiens ir racionāls ^
                    if dividesAtAll(curVal):
                        aiMove = None
                        if len(minimaxAIMoveset) > 0:
                            aiMove = minimaxAIMoveset.pop()
                            minimaxCompleteMoveset.pop()
                            print(f"rational moveset: {minimaxCompleteMoveset}") #debug
                        else: 
                            #šim nevajadzētu notikt
                            print("impossible condition met. how ???????")
                            
                        curVal = curVal / aiMove
                        if aiMove == 2:
                            humanScore = self.humanPoints.intValue()
                            humanScore = humanScore + aiMove
                            self.humanPoints.display(humanScore)
                            list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42.append(aiMove)
                            if not dividesAtAll(curVal):
                                self.gameEnd()
                                
                        else:
                            aiScore = self.aiPoints.intValue()
                            aiScore = aiScore + aiMove
                            self.humanPoints.display(aiScore)
                            list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42.append(aiMove)
                            if not dividesAtAll(curVal):
                                self.gameEnd()
                        
                        self.enemyMovesLabel.setText(f"Pretinieka pēdējais gājiens: {aiMove}")
                        self.numberDisplay.display(curVal)
                        if not dividesByTwo(curVal):
                            self.divByTwo.setEnabled(False)
                        else: 
                            self.divByTwo.setEnabled(True)
                        if not dividesByThree(curVal):
                            self.divByThree.setEnabled(False)
                        else: 
                            self.divByThree.setEnabled(True)
                    else:
                        self.gameEnd()
                else:
                    print("Played path doesnt match rational")
                    #============= jaunais moveset
                    minimaxCompleteMoveset = minimax.retraceRationalMoveset(globalminmaxGameTree, minimaxSoWhoIsThePlayer(globalDataCollector.startingPlayer), list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42)
                    minimaxAIMoveset = minimax.filterAIMoves(minimaxCompleteMoveset, -1)
                    #print(f"new moveset: {minimaxCompleteMoveset}")
                    #print(f"new ai moveset: {minimaxAIMoveset}")
                    if dividesAtAll(curVal):
                        aiMove = None
                        if len(minimaxAIMoveset) > 0:
                            aiMove = minimaxAIMoveset.pop()
                            minimaxCompleteMoveset.pop()
                            print(f"rational moveset: {minimaxCompleteMoveset}") #debug
                        curVal = curVal / aiMove
                        if aiMove == 2:
                            humanScore = self.humanPoints.intValue()
                            humanScore = humanScore + aiMove
                            self.humanPoints.display(humanScore)
                            list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42.append(aiMove)
                            if not dividesAtAll(curVal):
                                self.gameEnd()
                        else:
                            aiScore = self.aiPoints.intValue()
                            aiScore = aiScore + aiMove
                            self.humanPoints.display(aiScore)
                            list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42.append(aiMove)
                            if not dividesAtAll(curVal):
                                self.gameEnd()
                        
                        self.enemyMovesLabel.setText(f"Pretinieka pēdējais gājiens: {aiMove}")
                        self.numberDisplay.display(curVal)
                        if not dividesByTwo(curVal):
                            self.divByTwo.setEnabled(False)
                        else: 
                            self.divByTwo.setEnabled(True)
                        if not dividesByThree(curVal):
                            self.divByThree.setEnabled(False)
                        else: 
                            self.divByThree.setEnabled(True)
                    else:
                        self.gameEnd()
                    
            case "alfabeta":
                aiScore = self.aiPoints.intValue()
                aiScore = aiScore + 2
                self.aiPoints.display(aiScore)
                
                
                
    
    def ondivByThree_clicked(self):
        global globalDataCollector
        global minimaxCompleteMoveset
        global minimaxAIMoveset
        global list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42
        self.divByThree.setEnabled(False)
        
        humanScore = self.humanPoints.intValue()
        humanScore = humanScore + 3
        self.humanPoints.display(humanScore)
        
        curVal = self.numberDisplay.intValue()
        curVal = curVal / 3
        #pārbauda vai gājiens ir racionāls
        curMove = minimaxCompleteMoveset.pop()
        print(f"rational moveset: {minimaxCompleteMoveset}") #debug
        
        list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42.append(3)
        match globalDataCollector.algorithm:
            case "minimax":
                if curMove == 3:
                    #spēlētāja gājiens ir racionāls ^
                    if dividesAtAll(curVal):
                        aiMove = None
                        if len(minimaxAIMoveset) > 0:
                            aiMove = minimaxAIMoveset.pop()
                            minimaxCompleteMoveset.pop()
                            print(f"rational moveset: {minimaxCompleteMoveset}") #debug
                        curVal = curVal / aiMove
                        if aiMove == 2:
                            humanScore = self.humanPoints.intValue()
                            humanScore = humanScore + aiMove
                            self.humanPoints.display(humanScore)
                            list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42.append(aiMove)
                            if not dividesAtAll(curVal):
                                self.gameEnd()
                        else:
                            aiScore = self.aiPoints.intValue()
                            aiScore = aiScore + aiMove
                            self.humanPoints.display(aiScore)
                            list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42.append(aiMove)
                            if not dividesAtAll(curVal):
                                self.gameEnd()
                        
                        self.enemyMovesLabel.setText(f"Pretinieka pēdējais gājiens: {aiMove}")
                        self.numberDisplay.display(curVal)
                        if not dividesByTwo(curVal):
                            self.divByTwo.setEnabled(False)
                        else: 
                            self.divByTwo.setEnabled(True)
                        if not dividesByThree(curVal):
                            self.divByThree.setEnabled(False)
                        else: 
                            self.divByThree.setEnabled(True)
                    else:
                        self.gameEnd()
                else:
                    print("Played path doesnt match rational")
                    #============= jaunais moveset
                    minimaxCompleteMoveset = minimax.retraceRationalMoveset(globalminmaxGameTree, minimaxSoWhoIsThePlayer(globalDataCollector.startingPlayer), list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42)
                    minimaxAIMoveset = minimax.filterAIMoves(minimaxCompleteMoveset, -1)
                    #print(f"new moveset: {minimaxCompleteMoveset}")
                    #print(f"new ai moveset: {minimaxAIMoveset}")
                    if dividesAtAll(curVal):
                        aiMove = None
                        if len(minimaxAIMoveset) > 0:
                            aiMove = minimaxAIMoveset.pop()
                            minimaxCompleteMoveset.pop()
                            print(f"rational moveset: {minimaxCompleteMoveset}") #debug
                        else: 
                            #šim nevajadzētu notikt
                            print("impossible condition met. how ???????")
                            
                        curVal = curVal / aiMove
                        if aiMove == 2:
                            humanScore = self.humanPoints.intValue()
                            humanScore = humanScore + aiMove
                            self.humanPoints.display(humanScore)
                            list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42.append(aiMove)
                            if not dividesAtAll(curVal):
                                self.gameEnd()
                        else:
                            aiScore = self.aiPoints.intValue()
                            aiScore = aiScore + aiMove
                            self.humanPoints.display(aiScore)
                            list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42.append(aiMove)
                            if not dividesAtAll(curVal):
                                self.gameEnd()
                        
                        self.enemyMovesLabel.setText(f"Pretinieka pēdējais gājiens: {aiMove}")
                        self.numberDisplay.display(curVal)
                        if not dividesByTwo(curVal):
                            self.divByTwo.setEnabled(False)
                        else: 
                            self.divByTwo.setEnabled(True)
                        if not dividesByThree(curVal):
                            self.divByThree.setEnabled(False)
                        else: 
                            self.divByThree.setEnabled(True)
                    else:
                        self.gameEnd()
                    
            case "alfabeta":
                pass
            
    def gameEnd(self):
        print("game end")
        self.processStack.setCurrentIndex(4)
        self.processStack.widget(4).receive_airesult(self.aiPoints.intValue())
        self.processStack.widget(4).receive_humanresult(self.humanPoints.intValue())
        if self.aiPoints.intValue() > self.humanPoints.intValue():
            self.processStack.widget(4).whoWonLabel.setText("Uzvarēja mākslīgais intelekts !")
        elif self.aiPoints.intValue() < self.humanPoints.intValue():
            self.processStack.widget(4).whoWonLabel.setText("Jūs uzvarējāt !")
        else:
            self.processStack.widget(4).whoWonLabel.setText("Neizšķirts.")
        global list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42
        list_of_player_moves_as_integers_which_represents_the_sequence_of_actions_taken_by_players_in_the_game_integers_game_player_moves_i_am_going_insnae_42 = []
            
class GameResult(QWidget):
    def __init__(self, processStack: QStackedWidget):
        super().__init__()
        
        self.index = 4
        self.processStack = processStack
        
        self.layout = QVBoxLayout(self)
        
        self.humanPointsLabel = QLabel("Cilvēka spēlētāja punkti:", self)
        self.humanPoints = QLCDNumber(2,self)
        self.layout.addWidget(self.humanPointsLabel)
        self.layout.addWidget(self.humanPoints)
        
        self.aiPointsLabel = QLabel("Mākslīgā intelekta punkti:", self)
        self.aiPoints = QLCDNumber(2,self)
        self.layout.addWidget(self.aiPointsLabel)
        self.layout.addWidget(self.aiPoints)
        
        #TODO: paņemt punktus, salīdzināt
        
        self.whoWonLabel = QLabel(f"Uzvarēja ...", self)
        self.layout.addWidget(self.whoWonLabel)
        
        #TODO: poga ar kuru atsāk spēli
        self.playAgain = QPushButton("Play again")
        self.layout.addWidget(self.playAgain)
        self.playAgain.clicked.connect(self.onplayAgain_clicked)
        
    def receive_airesult(self, number):
        self.aiPoints.display(number)
        
    def receive_humanresult(self, number):
        self.humanPoints.display(number)
        
    def onplayAgain_clicked(self):
        # TODO: NEED TO RESET COUNTERS AT WIDGET INDEX 3 and 4
        self.processStack.setCurrentIndex(0)
        print("Playing again, reinputting params.")
        self.processStack.widget(3).humanPoints.display(0)
        self.processStack.widget(3).aiPoints.display(0)
        self.humanPoints.display(0)
        self.aiPoints.display(0)
    
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dalītāju spēle")
        self.setFixedSize(400, 300)

        # Create main container widget
        self.container_widget = QWidget(self)
        self.setCentralWidget(self.container_widget)

        # Create layout for the container widget
        self.layout = QVBoxLayout()
        self.container_widget.setLayout(self.layout)
        
        self.processStack = QStackedWidget(self)
        
        #Layouts (refer to classes)
        self.selectAI = ChooseAI(self.processStack) 
        self.selectPlayer = ChoosePlayer(self.processStack) 
        self.selectNumber = ChooseNumber(self.processStack) 
        self.playGame = PlayGame(self.processStack)
        self.gameResult = GameResult(self.processStack)

        self.processStack.addWidget(self.selectAI)
        self.processStack.addWidget(self.selectPlayer)
        self.processStack.addWidget(self.selectNumber)
        self.processStack.addWidget(self.playGame)
        self.processStack.addWidget(self.gameResult)
        
        self.layout.addWidget(self.processStack)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



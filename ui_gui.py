import random

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

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

class Ui_Dialog(object):

    ## Created by: Qt User Interface Compiler version 5.15.2

    def setupUi(self, Dialog):

        self.numbers = None
        self.starting_number = None
        self.first_player = None
        self.ai_algorith = None
        self.current_number = None
        self.user_score = 0
        self.computer_score = 0

        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 304)
        font = QFont()
        font.setFamily(u"SimSun")
        font.setPointSize(14)
        Dialog.setFont(font)

        self.stackedWidget = QStackedWidget(Dialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(10, 20, 381, 281))
        self.stackedWidget.setFrameShape(QFrame.Box)
        self.stackedWidget.setFrameShadow(QFrame.Plain)

        self.algo_choice = QWidget()
        self.algo_choice.setObjectName(u"algo_choice")

        self.algoChoiceLBL = QLabel(self.algo_choice)
        self.algoChoiceLBL.setObjectName(u"algoChoiceLBL")
        self.algoChoiceLBL.setGeometry(QRect(20, 20, 181, 21))
        self.algoChoiceLBL.setFont(font)

        self.splitter = QSplitter(self.algo_choice)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setGeometry(QRect(20, 60, 341, 211))        
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Vertical)

        self.minmaxBTN = QPushButton(self.splitter)
        self.minmaxBTN.setObjectName(u"minmaxBTN")
        self.minmaxBTN.clicked.connect(self.switch_to_startChoice)
        self.splitter.addWidget(self.minmaxBTN)

        self.alfabetaBTN = QPushButton(self.splitter)
        self.alfabetaBTN.setObjectName(u"alfabetaBTN")
        self.alfabetaBTN.clicked.connect(self.switch_to_startChoice)
        self.splitter.addWidget(self.alfabetaBTN)

        self.exitBTN = QPushButton(self.splitter)
        self.exitBTN.setObjectName(u"exitBTN")
        self.exitBTN.clicked.connect(QCoreApplication.instance().quit)
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.exitBTN.sizePolicy().hasHeightForWidth())
        self.exitBTN.setSizePolicy(sizePolicy1)
        self.exitBTN.setBaseSize(QSize(0, 0))
        self.splitter.addWidget(self.exitBTN)

        self.stackedWidget.addWidget(self.algo_choice)

        self.start_choice = QWidget()
        self.start_choice.setObjectName(u"start_choice")

        self.splitter_2 = QSplitter(self.start_choice)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setGeometry(QRect(20, 60, 341, 211))
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(Qt.Vertical)

        self.userBTN = QPushButton(self.splitter_2)
        self.userBTN.setObjectName(u"userBTN")
        self.userBTN.clicked.connect(self.user_BTN_pressed)
        self.splitter_2.addWidget(self.userBTN)

        self.computerBTN = QPushButton(self.splitter_2)
        self.computerBTN.setObjectName(u"computerBTN")
        self.computerBTN.clicked.connect(self.computer_BTN_pressed)
        self.splitter_2.addWidget(self.computerBTN)

        self.backBTN = QPushButton(self.splitter_2)
        self.backBTN.setObjectName(u"backBTN")
        sizePolicy1.setHeightForWidth(self.backBTN.sizePolicy().hasHeightForWidth())
        self.backBTN.setSizePolicy(sizePolicy1)
        self.backBTN.setBaseSize(QSize(0, 0))
        self.backBTN.clicked.connect(self.switch_to_algoChoice)
        self.splitter_2.addWidget(self.backBTN)

        self.gameStartLBL = QLabel(self.start_choice)
        self.gameStartLBL.setObjectName(u"gameStartLBL")
        self.gameStartLBL.setGeometry(QRect(20, 20, 181, 21))
        self.gameStartLBL.setFont(font)

        self.stackedWidget.addWidget(self.start_choice)

        self.number_choice = QWidget()
        self.number_choice.setObjectName(u"number_choice")

        self.numChoiceLBL = QLabel(self.number_choice)
        self.numChoiceLBL.setObjectName(u"numChoiceLBL")
        self.numChoiceLBL.setGeometry(QRect(90, 20, 201, 21))
        self.numChoiceLBL.setFont(font)

        self.layoutWidget = QWidget(self.number_choice)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(40, 60, 301, 201))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.startchoiceA = QPushButton(self.layoutWidget)
        self.startchoiceA.setObjectName(u"startchoiceA")
        self.startchoiceA.clicked.connect(self.startchoiceA_pressed)
        self.verticalLayout.addWidget(self.startchoiceA)

        self.startchoiceB = QPushButton(self.layoutWidget)
        self.startchoiceB.setObjectName(u"startchoiceB")
        self.startchoiceB.clicked.connect(self.startchoiceB_pressed)
        self.verticalLayout.addWidget(self.startchoiceB)

        self.startchoiceC = QPushButton(self.layoutWidget)
        self.startchoiceC.setObjectName(u"startchoiceC")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.startchoiceC.sizePolicy().hasHeightForWidth())
        self.startchoiceC.setSizePolicy(sizePolicy2)
        self.startchoiceC.clicked.connect(self.startchoiceC_pressed)
        self.verticalLayout.addWidget(self.startchoiceC)

        self.startchoiceD = QPushButton(self.layoutWidget)
        self.startchoiceD.setObjectName(u"startchoiceD")
        sizePolicy2.setHeightForWidth(self.startchoiceD.sizePolicy().hasHeightForWidth())
        self.startchoiceD.setSizePolicy(sizePolicy2)
        self.startchoiceD.clicked.connect(self.startchoiceD_pressed)
        self.verticalLayout.addWidget(self.startchoiceD)

        self.startchoiceE = QPushButton(self.layoutWidget)
        self.startchoiceE.setObjectName(u"startchoiceE")
        sizePolicy2.setHeightForWidth(self.startchoiceE.sizePolicy().hasHeightForWidth())
        self.startchoiceE.setSizePolicy(sizePolicy2)
        self.startchoiceE.clicked.connect(self.startchoiceE_pressed)
        self.verticalLayout.addWidget(self.startchoiceE)

        self.stackedWidget.addWidget(self.number_choice)

        self.gameplay = QWidget()
        self.gameplay.setObjectName(u"gameplay")
        self.userGRP = QGroupBox(self.gameplay)
        self.userGRP.setObjectName(u"userGRP")
        self.userGRP.setGeometry(QRect(10, 30, 171, 221))
        self.curNumU = QLabel(self.userGRP)
        self.curNumU.setObjectName(u"curNumU")
        self.curNumU.setGeometry(QRect(100, 90, 61, 31))
        self.curNumU.setFrameShape(QFrame.WinPanel)
        self.curNumU.setFrameShadow(QFrame.Sunken)
        self.curNumU.setAlignment(Qt.AlignCenter)
        self.curScoreU = QLabel(self.userGRP)
        self.curScoreU.setObjectName(u"curScoreU")
        self.curScoreU.setGeometry(QRect(100, 40, 47, 31))
        self.curScoreU.setFrameShape(QFrame.WinPanel)
        self.curScoreU.setFrameShadow(QFrame.Sunken)
        self.curScoreU.setAlignment(Qt.AlignCenter)
        self.UnumberLBL = QLabel(self.userGRP)
        self.UnumberLBL.setObjectName(u"UnumberLBL")
        self.UnumberLBL.setGeometry(QRect(10, 90, 81, 31))
        self.UscoreLBL = QLabel(self.userGRP)
        self.UscoreLBL.setObjectName(u"UscoreLBL")
        self.UscoreLBL.setGeometry(QRect(10, 40, 61, 31))
        self.splitter_3 = QSplitter(self.userGRP)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setGeometry(QRect(11, 140, 150, 51))
        self.splitter_3.setOrientation(Qt.Horizontal)

        self.divTwoU = QPushButton(self.splitter_3)
        self.divTwoU.setObjectName(u"divTwoU")
        self.divTwoU.clicked.connect(self.divTwoU_pressed)
        self.splitter_3.addWidget(self.divTwoU)

        self.divThreeU = QPushButton(self.splitter_3)
        self.divThreeU.setObjectName(u"divThreeU")
        self.divThreeU.clicked.connect(self.divThreeU_pressed)
        self.splitter_3.addWidget(self.divThreeU)

        self.computerGRP = QGroupBox(self.gameplay)
        self.computerGRP.setObjectName(u"computerGRP")
        self.computerGRP.setGeometry(QRect(190, 30, 171, 221))
        self.curNumC = QLabel(self.computerGRP)
        self.curNumC.setObjectName(u"curNumC")
        self.curNumC.setGeometry(QRect(100, 90, 61, 31))
        self.curNumC.setFrameShape(QFrame.WinPanel)
        self.curNumC.setFrameShadow(QFrame.Sunken)
        self.curNumC.setAlignment(Qt.AlignCenter)
        self.curScoreC = QLabel(self.computerGRP)
        self.curScoreC.setObjectName(u"curScoreC")
        self.curScoreC.setGeometry(QRect(100, 40, 47, 31))
        self.curScoreC.setFrameShape(QFrame.WinPanel)
        self.curScoreC.setFrameShadow(QFrame.Sunken)
        self.curScoreC.setAlignment(Qt.AlignCenter)
        self.CnumberLBL = QLabel(self.computerGRP)
        self.CnumberLBL.setObjectName(u"CnumberLBL")
        self.CnumberLBL.setGeometry(QRect(10, 90, 81, 31))
        self.CscoreLBL = QLabel(self.computerGRP)
        self.CscoreLBL.setObjectName(u"CscoreLBL")
        self.CscoreLBL.setGeometry(QRect(10, 40, 61, 31))
        self.splitter_4 = QSplitter(self.computerGRP)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setGeometry(QRect(11, 140, 150, 51))
        self.splitter_4.setOrientation(Qt.Horizontal)

        self.divTwoC = QPushButton(self.splitter_4)
        self.divTwoC.setObjectName(u"divTwoC")
        # self.divTwoC.clicked.connect(self.divTwoC_pressed)
        self.splitter_4.addWidget(self.divTwoC)

        self.divThreeC = QPushButton(self.splitter_4)
        self.divThreeC.setObjectName(u"divThreeC")
        # self.divThreeC.clicked.connect(self.divThreeC_pressed)
        self.splitter_4.addWidget(self.divThreeC)

        self.stackedWidget.addWidget(self.gameplay)

        self.win = QWidget()
        self.win.setObjectName(u"win")
        self.winLBL = QLabel(self.win)
        self.winLBL.setObjectName(u"winLBL")
        self.winLBL.setGeometry(QRect(50, 30, 281, 111))
        self.winLBL.setFrameShape(QFrame.WinPanel)
        self.winLBL.setFrameShadow(QFrame.Raised)
        self.winLBL.setLineWidth(1)
        self.winLBL.setMidLineWidth(1)
        self.winLBL.setAlignment(Qt.AlignCenter)

        self.WretryBTN = QPushButton(self.win)
        self.WretryBTN.setObjectName(u"WretryBTN")
        self.WretryBTN.clicked.connect(self.switch_to_algoChoice)
        self.WretryBTN.setGeometry(QRect(110, 190, 161, 51))

        self.stackedWidget.addWidget(self.win)
        self.lose = QWidget()
        self.lose.setObjectName(u"lose")

        self.LretryBTN = QPushButton(self.lose)
        self.LretryBTN.setObjectName(u"LretryBTN")
        self.LretryBTN.clicked.connect(self.switch_to_algoChoice)
        self.LretryBTN.setGeometry(QRect(110, 190, 161, 51))

        self.loseLBL = QLabel(self.lose)
        self.loseLBL.setObjectName(u"loseLBL")
        self.loseLBL.setGeometry(QRect(50, 30, 281, 111))
        self.loseLBL.setFrameShape(QFrame.WinPanel)
        self.loseLBL.setFrameShadow(QFrame.Raised)
        self.loseLBL.setLineWidth(1)
        self.loseLBL.setMidLineWidth(1)
        self.loseLBL.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(self.lose)

        self.draw = QWidget()
        self.draw.setObjectName(u"draw")

        self.DretryBTN = QPushButton(self.draw)
        self.DretryBTN.setObjectName(u"DretryBTN")
        self.DretryBTN.clicked.connect(self.switch_to_algoChoice)
        self.DretryBTN.setGeometry(QRect(110, 190, 161, 51))

        self.drawLBL = QLabel(self.draw)
        self.drawLBL.setObjectName(u"drawLBL")
        self.drawLBL.setGeometry(QRect(50, 30, 281, 111))
        self.drawLBL.setFrameShape(QFrame.WinPanel)
        self.drawLBL.setFrameShadow(QFrame.Raised)
        self.drawLBL.setLineWidth(1)
        self.drawLBL.setMidLineWidth(1)
        self.drawLBL.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(self.draw)

        self.retranslateUi(Dialog)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.algoChoiceLBL.setText(QCoreApplication.translate("Dialog", u"Algoritma izv\u0113le", None))
        self.minmaxBTN.setText(QCoreApplication.translate("Dialog", u"Mini-Max", None))
        self.alfabetaBTN.setText(QCoreApplication.translate("Dialog", u"Alfa-Beta", None))
        self.exitBTN.setText(QCoreApplication.translate("Dialog", u"P\u0101rtraukt sp\u0113li", None))
        self.userBTN.setText(QCoreApplication.translate("Dialog", u"Lietot\u0101js", None))
        self.computerBTN.setText(QCoreApplication.translate("Dialog", u"Dators", None))
        self.backBTN.setText(QCoreApplication.translate("Dialog", u"Atpaka\u013c", None))
        self.gameStartLBL.setText(QCoreApplication.translate("Dialog", u"Sp\u0113li uzs\u0101k", None))
        self.numChoiceLBL.setText(QCoreApplication.translate("Dialog", u"S\u0101kuma skait\u013ca izv\u0113le", None))
        self.startchoiceA.setText("")
        self.startchoiceB.setText("")
        self.startchoiceC.setText("")
        self.startchoiceD.setText("")
        self.startchoiceE.setText("")
        self.userGRP.setTitle(QCoreApplication.translate("Dialog", u"Lietot\u0101js", None))
        self.curNumU.setText(QCoreApplication.translate("Dialog", u"34", None))
        self.curScoreU.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.UnumberLBL.setText(QCoreApplication.translate("Dialog", u"Skaitlis", None))
        self.UscoreLBL.setText(QCoreApplication.translate("Dialog", u"Punkti", None))
        self.divTwoU.setText(QCoreApplication.translate("Dialog", u"2", None))
        self.divThreeU.setText(QCoreApplication.translate("Dialog", u"3", None))
        self.computerGRP.setTitle(QCoreApplication.translate("Dialog", u"Dators", None))
        self.curNumC.setText(QCoreApplication.translate("Dialog", u"34", None))
        self.curScoreC.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.CnumberLBL.setText(QCoreApplication.translate("Dialog", u"Skaitlis", None))
        self.CscoreLBL.setText(QCoreApplication.translate("Dialog", u"Punkti", None))
        self.divTwoC.setText(QCoreApplication.translate("Dialog", u"2", None))
        self.divThreeC.setText(QCoreApplication.translate("Dialog", u"3", None))
        self.winLBL.setText(QCoreApplication.translate("Dialog", u"Tu esi uzvar\u0113jis!", None))
        self.WretryBTN.setText(QCoreApplication.translate("Dialog", u"M\u0113\u0123in\u0101t v\u0113lreiz", None))
        self.LretryBTN.setText(QCoreApplication.translate("Dialog", u"M\u0113\u0123in\u0101t v\u0113lreiz", None))
        self.loseLBL.setText(QCoreApplication.translate("Dialog", u"Tu esi zaud\u0113jis!", None))
        self.DretryBTN.setText(QCoreApplication.translate("Dialog", u"M\u0113\u0123in\u0101t v\u0113lreiz", None))
        self.drawLBL.setText(QCoreApplication.translate("Dialog", u"Neiz\u0161\u0137irts!", None))
    # retranslateUi
    
    @Slot()
    def minmax_BTN_pressed(self):
        self.ai_algorithm = "Min-Max"
        self.switch_to_startChoice()

    @Slot()
    def alfabeta_BTN_pressed(self):
        self.ai_algorithm = "Alpha-Beta"
        self.switch_to_startChoice()

    

    @Slot()
    def user_BTN_pressed(self):
        self.first_player = "player"
        self.switch_to_numberChoice()

    @Slot()
    def computer_BTN_pressed(self):
        self.first_player = "bot"
        self.switch_to_numberChoice()



    @Slot()
    def startchoiceA_pressed(self):
        if self.numbers is not None and self.first_player is not None and len(self.numbers) >= 5:
            self.starting_number = int(self.numbers[0])
            self.switch_to_gameplay(self.starting_number)

    @Slot()
    def startchoiceB_pressed(self):
        if self.numbers is not None and self.first_player is not None and len(self.numbers) >= 5:
            self.starting_number = int(self.numbers[1])
            self.switch_to_gameplay(self.starting_number)

    @Slot()
    def startchoiceC_pressed(self):
        if self.numbers is not None and self.first_player is not None and len(self.numbers) >= 5:
            self.starting_number = int(self.numbers[2])
            self.switch_to_gameplay(self.starting_number)

    @Slot()
    def startchoiceD_pressed(self):
        if self.numbers is not None and self.first_player is not None and len(self.numbers) >= 5:
            self.starting_number = int(self.numbers[3])
            self.switch_to_gameplay(self.starting_number)

    @Slot()
    def startchoiceE_pressed(self):
        if self.numbers is not None and self.first_player is not None and len(self.numbers) >= 5:
            self.starting_number = int(self.numbers[4])
            self.switch_to_gameplay(self.starting_number)
    


    @Slot()
    def switch_to_algoChoice(self):
        self.stackedWidget.setCurrentIndex(0)

    @Slot()
    def switch_to_startChoice(self):
        self.stackedWidget.setCurrentIndex(1)

    @Slot()
    def switch_to_numberChoice(self):
        self.stackedWidget.setCurrentIndex(2)

        self.numbers = generate_numbers()

        self.startchoiceA.setText(QCoreApplication.translate("Dialog", str(self.numbers[0]), None))
        self.startchoiceB.setText(QCoreApplication.translate("Dialog", str(self.numbers[1]), None))
        self.startchoiceC.setText(QCoreApplication.translate("Dialog", str(self.numbers[2]), None))
        self.startchoiceD.setText(QCoreApplication.translate("Dialog", str(self.numbers[3]), None))
        self.startchoiceE.setText(QCoreApplication.translate("Dialog", str(self.numbers[4]), None))

    @Slot(int)
    def switch_to_gameplay(self, starting_number):
        
        if starting_number is not None:
            self.stackedWidget.setCurrentIndex(3)
            self.curNumU.setText(QCoreApplication.translate("Dialog", str(starting_number), None))
            self.curNumC.setText(QCoreApplication.translate("Dialog", str(starting_number), None))

            self.current_number = starting_number
            self.player_turn = self.first_player
            
            if self.player_turn ==  "bot":
                self.botTurn()
            
        else:
           self.showErrorMessage("Error", "Starting number is None, cannot switch to gameplay.")

        
    @Slot()
    def update_curNum(self,newCurnNum):
        if newCurnNum > 10:
            self.curNumU.setText(QCoreApplication.translate("Dialog", str(newCurnNum), None))
            self.curNumC.setText(QCoreApplication.translate("Dialog", str(newCurnNum), None))
        else:
            self.end_game()

    @Slot()
    def divTwoU_pressed(self):
        if self.player_turn == "player":
            
            if self.current_number % 2 == 0:
                self.user_score += 2
                self.current_number = self.current_number / 2
                self.update_curNum(self.current_number)
                self.player_turn = "bot"
                self.botTurn()
            else:
                self.showErrorMessage("Error", "Nederīga izvēle, mēģini vēlreiz.")
                self.switch_to_algoChoice()

        else:
            self.showErrorMessage("Error", "It is not your turn.")

    @Slot()
    def divThreeU_pressed(self):
        if self.player_turn == "player":
            
            if self.current_number % 3 == 0:
                self.user_score += 3
                self.current_number //= 3
                self.update_curNum(self.current_number)
                self.player_turn = "bot"
                self.botTurn()

            else:
                
                self.showErrorMessage("Error", "Nederīga izvēle, mēģini vēlreiz.")
                self.switch_to_algoChoice()
                

            
        else:
            self.showErrorMessage("Error", "It is not your turn.")

    def botTurn(self):
        divisor = bot_choice(self.current_number)
        if self.current_number % divisor == 0:
            if divisor == 2:
                self.computer_score += 2
            else:
                self.computer_score += 3

            self.current_number //= divisor
            self.update_curNum(self.current_number)
            self.player_turn = "player"
            
        else:
            self.showErrorMessage("Error", "Dators veica nederīgu izvēli, mēģini vēlreiz.")
            self.switch_to_algoChoice()
                

    # @Slot()
    # def divTwoC_pressed(self):
    #     if self.player_turn == "player":
            
    #         if self.current_number % 2 == 0:
    #             self.user_score += 2
    #             self.current_number = self.current_number / 2
    #             self.update_curNum(self.current_number)

    #         else:
    #             self.showErrorMessage("Error", "Nederīga izvēle, mēģini vēlreiz.")
    #             self.switch_to_algoChoice

    #         self.player_turn = "bot"
    #     else:
    #         self.showErrorMessage("Error", "It is not your turn.")
    # @Slot()
    # def divThreeC_pressed(self):
    #     if self.player_turn == "player":
            
    #         if self.current_number % 2 == 0:
    #             self.user_score += 2
    #             self.current_number = self.current_number / 2
    #             self.update_curNum(self.current_number)

    #         else:
    #             self.showErrorMessage("Error", "Nederīga izvēle, mēģini vēlreiz.")
    #             self.switch_to_algoChoice

    #         self.player_turn = "bot"
    #     else:
    #         self.showErrorMessage("Error", "It is not your turn.")
        
    # while current_number > 10:

    #     if player_turn == "player":
    #         divisor = int(input(f"Izvēlies, ar ko dalīt skaitli {current_number} (2 vai 3): "))
    #     else:
    #         divisor = bot_choice(current_number)
    #         print(f"Bot chooses to divide {current_number} by {divisor}")
    #     if divisor not in (2, 3):
    #         print("Var dalīt tikai ar 2 vai 3!")
    #         continue
    #     if current_number % divisor == 0:
    #         if divisor == 2:
    #             player2_points += 2
    #         else:
    #             player1_points += 3
    #         current_number //= divisor
    #         print(f"Punkti: Spēlētājs 1 - {player1_points}, Spēlētājs 2 - {player2_points}")
    #     else:
    #         print("Nederīga izvēle, mēģini vēlreiz.")
    #         break  # End the game if the number cannot be divided evenly
    #     if player_turn == "player":
    #         player_turn = "bot"
    #     else:
    #         player_turn = "player"

    @Slot()
    def end_game(self):
        if self.curScoreU > self.curScoreC:
            self.switch_to_win()
        elif self.curScoreU < self.curScoreC:
            self.switch_to_lose()
        else:
            self.switch_to_draw()

        

    @Slot()
    def switch_to_win(self):
        self.stackedWidget.setCurrentIndex(4)

    @Slot()
    def switch_to_lose(self):
        self.stackedWidget.setCurrentIndex(5)

    @Slot()
    def switch_to_draw(self):
        self.stackedWidget.setCurrentIndex(6)


    def showErrorMessage(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

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
    import sys
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
    main()

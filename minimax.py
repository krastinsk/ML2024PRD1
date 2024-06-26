"""
RTU 2024
Autors: Edgars Lejnieks, 221RDB168

Paka satur koka ģenerēšanas funkciju un 
minimax algoritma funkciju kas darbojas ar uzģenerēto koku.

Nepieciešamības:
Python 3
pakotne random >>> cmd >>> pip install random
pakotne treelib >>> cmd >>> pip install treelib
"""

# priekšprocesi ==================================================================

import random
import treelib # ārējā paka koku attēlošanai

# statiskas vērtības =============================================================

MAXIMUM_NUMBER = 20000
MINIMUM_NUMBER = 10000

# globālas vērtības ==============================================================

usedNodeRFID = 0
#iterācija pāri koka eksistējošajām un neeksistējošajām 2^n virsotnēm

# klases =========================================================================

# tika atmestas lai tā vietā lietotu treelib

# funkcijas ======================================================================

def divisible(number: int):
    if number % 2 != 0:
        return False
    if number % 3 != 0:
        return False
    return True
    
def getValidTestValue():
    """
    input: none
    output: int
    
    ģenerē veselu skaitli (int) kas ir starp 10000 līdz 20000 abus skaitļus ieskaitot
    vienlaicīgi pieskaitot tiem gala rezultāta vērtības
    """  
    matchesCondition = False
    while(matchesCondition != True):
        testValue = random.randrange(MINIMUM_NUMBER, MAXIMUM_NUMBER, 1)
        if divisible(testValue):
            matchesCondition = True
    return testValue

# v2 - pievienots pēc pārstrukturēšanas
def heuristicScoreAssign(tree: treelib.Tree, parentNodeRFID: int, scoreSetter: int, level: int, divisor: int):
    """
    input: treelib.Tree, int, int, int, int, int
    output: int
    
    Ģenerē heiristisko vērtību balstoties uz to, kāds ir gājiens, un vai ja gājiens (tikai dalīšana ar 3) spiež pretiniekam veikt nevēlamu gājienu.
    """
    node = tree.get_node(parentNodeRFID)
    aiScores = None
    score = 0
    finalScore = None
    
    if scoreSetter == 1:
        aiScores = (-2, 3) # spēlētājs maksimizē
    elif scoreSetter == -1:
        aiScores = (2, -3) # intelekts maksimizē
    else:
        print("bad scoreSetter.")
        return
        
    # -gājieni kuros dala ar trīs, pieskaitīt (punktu skaitu * 1.3)
    # -pretējā gadījumā, (ps * 0.7)
    if((level == 0) or (level % 2 == 0)):
        if divisor == 2:
            score = aiScores[0]*(0.7*scoreSetter)*-1
        elif divisor == 3:
            score = aiScores[1]*(1.3*scoreSetter)*-1
            lookAhead = node.data["value"]
            if lookAhead % 3 == 0:
                lookAhead = lookAhead / 3
                if lookAhead % 3 != 0 and lookAhead % 2 == 0:
                    score = score*1.5

    elif((level == 1) or (level % 3 == 0)):
        if divisor == 2:
            score = aiScores[0]*(0.7*scoreSetter)
        elif divisor == 3:
            score = aiScores[1]*(1.3*scoreSetter)
            lookAhead = node.data["value"]
            if lookAhead % 3 == 0:
                lookAhead = lookAhead / 3
                if lookAhead % 3 != 0 and lookAhead % 2 == 0:
                    score = score*1.5
    
    finalScore = node.tag + round(float(score),2)
    return round(finalScore, 2)

def generateGameTree(number: int, scoreSetter: int):
    """
    input: int, int
    output: treelib.tree
    
    izmantojot treelib bibliotēku izveido koku ar visiem iespējamajiem gājieniem
    ja scoreSetter = 1, lielāki skaitļi ir cilvēka spēlētājam vēlami
    ja scoreSetter = -1, lielāki skaitļi ir mākslīgam intelektam vēlami
    """
    if not divisible(number):
        print("generateGameTree: bad number")
        return []
    
    aiScores = None
    if scoreSetter == 1:
        aiScores = (-2, 3) # spēlētājs maksimizē
    elif scoreSetter == -1:
        aiScores = (2, -3) # intelekts maksimizē
    else:
        print(f"generateGameTree({number}, {scoreSetter})")
        print(f"bad function input.")
        return
    
    # vars
    global usedNodeRFID
    variableNumber = number
    levelIteration = 0
    loopCondition = True
    theScore = None
    
    # structs
    libraryTree = treelib.Tree()
    libraryTree.create_node(0, usedNodeRFID, None, {"value":number, "divisor":0, "score":0})
    
    # func (REWRITTEN)
    db2 = lambda variableNumber: variableNumber / 2
    db3 = lambda variableNumber: variableNumber / 3
    
    levelIteration += 1
    
    if variableNumber % 2 == 0:
        usedNodeRFID += 1
        libraryTree.create_node(heuristicScoreAssign(libraryTree,0,scoreSetter,levelIteration,2), usedNodeRFID, 0, {"value":db2(variableNumber), "divisor":2, "score":-2*scoreSetter})
    if variableNumber % 3 == 0:
        usedNodeRFID += 1
        libraryTree.create_node(heuristicScoreAssign(libraryTree,0,scoreSetter,levelIteration,3), usedNodeRFID, 0, {"value":db3(variableNumber), "divisor":3, "score":3*scoreSetter})
    
    while(loopCondition):
        levelIteration += 1
        loopCondition = False
        
        # https://github.com/caesar0301/treelib/issues/147
        # depth_2_nodes = list(my_tree.filter_nodes(lambda x: my_tree.depth(x) == 2))
        
        for item in list(libraryTree.filter_nodes(lambda x: libraryTree.depth(x) == (levelIteration - 1))):
            variableNumber = item.data["value"]
            if variableNumber % 2 == 0 and variableNumber > 0:
                usedNodeRFID += 1
                if levelIteration % 2 == 0:
                    theScore = item.data["score"] + (aiScores[0]*-1)
                else:
                    theScore = item.data["score"] + (aiScores[0])
                libraryTree.create_node(heuristicScoreAssign(libraryTree,item.identifier,scoreSetter,levelIteration,2), usedNodeRFID, item.identifier, {"value":db2(variableNumber), "divisor":2, "score":theScore})
                loopCondition = True
            else:
                usedNodeRFID += 1

            if variableNumber % 3 == 0 and variableNumber > 0:
                if levelIteration % 2 == 0:
                    theScore = item.data["score"] + (aiScores[1]*-1)
                else:
                    theScore = item.data["score"] + (aiScores[1])
                usedNodeRFID += 1
                libraryTree.create_node(heuristicScoreAssign(libraryTree,item.identifier,scoreSetter,levelIteration,3), usedNodeRFID, item.identifier, {"value":db3(variableNumber), "divisor":3, "score":theScore})
                loopCondition = True
            else:
                usedNodeRFID += 1
                
    print(libraryTree.show(stdout=False))
    usedNodeRFID = 0 # v2 - reset global to 0
    return libraryTree

def minimax(tree: treelib.tree, node_id: int, maximizing_player: int = 1):
    """
    input: treelib.tree, int, int
    output: [int, list, tree]
    
    Minimax algoritms. Pārmeklē uzģenerēto koku pilnā apmērā.
    Ņemot vērā iespējamos galējos rezultātus, atrod visticamāko
    ceļu kādu spēlētājam un intelektam spēlējot racionāli būtu jāņem.
    Ja tiek atrasti divi vienāda vērtējuma ceļi, tiek ņemts pirmais sarakstā
    (kreisā puse grafiski.)
    
    Dalītāji tiek ievietoti masīvā sākot no pēdējā gājiena, tāpēc
    rezultējošais masīvs jālasa no labās uz kreiso pusi (<-),
    kur pēdējais skaitlis ir pirmais.
    (Līdzīgi kā stekā. Der darbībai ar .pop() )
    
    """
    actionstack = []
    childValues = []
    node = tree.get_node(node_id)
    
    if node in tree.leaves():
        movestack = []
        return node.tag, movestack, tree
    
    #https://treelib.readthedocs.io/en/latest/treelib.html#module-treelib.tree
    #is_branch(nid)
    #Returns the children (ID) list of nid. Empty list is returned if nid does not exist
    
    if maximizing_player == 1:
        for child_id in tree.is_branch(node_id):
            childValue, movestack, tree = minimax(tree, child_id, -1)
            childValues.append((childValue, child_id, movestack))
        best_value = max(childValues, key=lambda x: x[0])
        #print(f"best value: {best_value}")
        curNode = tree.get_node(best_value[1])
        actionstack = best_value[2]
        actionstack.append(curNode.data["divisor"])
        return best_value[0], actionstack, tree
    elif maximizing_player == -1:
        for child_id in tree.is_branch(node_id):
            childValue, movestack, tree = minimax(tree, child_id, 1)
            childValues.append((childValue, child_id, movestack))
        best_value = min(childValues, key=lambda x: x[0])
        #print(f"best value: {best_value}")
        curNode = tree.get_node(best_value[1])
        actionstack = best_value[2]
        actionstack.append(curNode.data["divisor"])
        return best_value[0], actionstack, tree
    
def testDataCollect():
    """
    input: 
    output: int, int
    
    funkcija kuru var izsaukt lai ievadītu spēles skaitli un spēlētāju kura punkti tiek uzskaitīti
    """
    testVal = 0
    gook = input("Manual value: 1, Random value: 2\ninput: ")
    if int(gook) == 1:
        testVal = int(input("input test value: "))
        if divisible(testVal) and testVal in range(10000, 20000, 1):
            print("test value is " + str(testVal))
        else:
            print(f"bad input. ending.")
            return
    elif int(gook) == 2:
        testVal = getValidTestValue()
        print("test value is " + str(testVal))
    else:
        print(f"bad input, expected 1 or 2, ending.")
        return
    scoreSetter = int(input("scoreSetter = 1 >>>> player starts\nscoreSetter = -1 >>>> AI starts\ninput: "))
    return testVal, scoreSetter

def shouldScriptOutputToGraphviz(tree: treelib.Tree):
    """
    input: treelib.Tree
    output:
    
    izveido skripta faila mapē failu "idk.txt" 
    kurā ir kods (DOT formatējumā) ar kuru var vizualizēt koku kā attēlu
    Graphviz dokumentācija: https://graphviz.org/
    Tiešsaistes rīks koda attēlošanai: https://dreampuf.github.io/GraphvizOnline/
    """
    ans = input(f"output graphviz file ? Y/N\n")
    if ans == "y":
        tree.to_graphviz("DOT_code_for_graph.txt")
    else:
        return
    
def printAllNodesButNicer(tree: treelib.Tree):
    """
    input: treelib.Tree
    output: 
    
    saraksta veidā izprintē katras virsotnes datus
    """
    nodeList = tree.all_nodes_itr()
    lines = [str(item) + "\n" for item in nodeList]
    result = "".join(lines)
    print(result)
    
# v2 - no gājiena saraksta izvada MI gājienus
def filterAIMoves(moveList: list, scoreSetter: int):
    if(scoreSetter == 1):
        glubby = list(reversed(moveList))[1::2]
        glubby.reverse()
        return glubby
    elif(scoreSetter == -1):
        glubby = list(reversed(moveList))[::2]
        glubby.reverse()
        return glubby
    
# v3 - paņemt apakškoku, ja spēlētājs veic neracionālu gājienu
def retraceRationalMoveset(tree: treelib.tree, maximizing_player: int = 1, movesToFollow: list = None):
    """
    input: treelib.Tree, int, list
    output: list
    
    Pieņemot iespēju, ka spēlētājs var veikt neracionālu gājienu, šis algoritms iegūst apakškoku spēles kokam atkarīgi no tā, kādi gājieni ir veikti.
    """
    node_id = 0
    for num in movesToFollow:
        if num == 2:
            node_id = node_id * 2 + 1
        elif num == 3:
            node_id = node_id * 2 + 2
        else:
            raise ValueError("Invalid number in the list. Only 2 and 3 are allowed.")
    new_tree = treelib.Tree(tree.subtree(node_id), deep=True)
    bestVal, optimalMoveset, unused = minimax(new_tree, node_id, maximizing_player)
    return optimalMoveset



# darbības =======================================================================
# NOŅEMT JA NETIEK LIETOTS TESTĒŠANAI

"""
#uzģenerēt testa koku:
testVal, scoreSetter = testDataCollect() #savāc datus
gameTree = generateGameTree(testVal, scoreSetter)
minimax_result = minimax(gameTree, 0, scoreSetter)
print(f"minimax_best_value: {minimax_result[0]}, AIpath: {filterAIMoves(minimax_result[1], scoreSetter)},\n All Moves: {minimax_result[1]}")

printAllNodesButNicer(gameTree) #izprintē virsotnes sarakstā (atkļūdošanai)

#shouldScriptOutputToGraphviz(gameTree) #izvada failu ar DOT kodu (atkļūdošanai)

input() #palaižot kā skriptu uz datora, ļauj nospiest pogu lai pabeigtu skriptu
"""

#labi vai unikali skaitļi
# 14592
# 18954
# 12204
# 14112 <--- rekomendācija
# 13608
# 15552

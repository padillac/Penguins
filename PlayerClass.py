
class Player:

    def __init__(self, team):
        self.team = team
        self.livePenguinsNum = 4

    def getTeam(self):
        return self.team

    def getLivePenguinsNum(self):
        return self.livePenguinsNum


    #function to get user input and return a tuple containing the selected penguin and the selected movement vector
    def getMoveVector(self, window, allPenguins):
        selectedPenguin = None
        while selectedPenguin == None:
            selectedPoint = window.getMouse()
            for p in allPenguins:
                if p.isCollision(selectedPoint) and p.getTeam() == self.team:
                    selectedPenguin = p
        newMoveVector = selectedPenguin.getPenguinMoveVector()
        return selectedPenguin, newMoveVector


    #function that allows player to pick all movements
    def takeTurn(self, window, allPenguins):
        nextMoves = {}
        while len(nextMoves) < self.livePenguinsNum:
            nM = self.getMoveVector(window, allPenguins)
            nextMoves[nM[0]] = nM[1]
        return nextMoves

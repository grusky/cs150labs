import critter
import color    

class Elephant(critter.Critter):

    def __init__(self, steps) :
        self.steps = steps
        self.moves = 0
        self.dir = critter.SOUTH
        
    def fight(self, oppInfo):
        if oppInfo.char == 'T' :
            return critter.ROAR
        return critter.POUNCE
    
    def getColor(self):
        return color.GRAY
    
    def getMove(self, info):
        if self.moves % (4*self.steps) == 0 :
            self.dir = critter.SOUTH
        elif self.moves % (4*self.steps) == self.steps :
            self.dir = critter.WEST
        elif self.moves % (4*self.steps) == 2*self.steps :
            self.dir = critter.NORTH
        elif self.moves % (4*self.steps) == 3*self.steps :
            self.dir = critter.EAST
        #print( self.moves, self.steps )
        self.moves += 1
        return self.dir

    def getChar(self):
        return 'E'

    # we don't have a fightOver method here, because a 
    # Stone doesn't do anything with this information
    # this method is called by the client prog when a fight is over
    # since the client prog knows who won the fight, when it calls
    # this method, it passes in true for the iWon parameter if this
    # critter won the fight, and false otherwise
    # oppWeapon is the opponent's weapon (ROAR, POUNCE, or SCRATCH)
    # oppColor is the opponent's color
    # the purpose of this information is to allow you to learn strategies
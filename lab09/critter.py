import collections
Point = collections.namedtuple('Point', ['x', 'y'])

# Constants for movement.
N = "NORTH"
S = "SOUTH"
E = "EAST"
W = "WEST"
C = "CENTER"
DIRECTIONS = ("NORTH", "EAST", "SOUTH", "WEST", "CENTER")
WORLD_SIZE = Point(60, 50)
    
class Critter():
    """
    The base Critter class.
    """

    def __init__(self, x, y):
    	pass

    # Give a tuple of two nonnegative numbers, whose sum is less than or equal to 100.
    # The first represents your attack value, and the second your defense value.
    # Values are permanent--once assigned to a critter, they cannot be changed.
    def getStats(self):
        pass
        
    # Give your color.
    # @returns Your current color.
    def getColor(self):
        pass
    
    # Give your direction.
    # @param info your critter info
    # @returns A cardinal direction, in the form of a constant (N, E, S, W, C) or
    # as a string ("NORTH", "EAST", "SOUTH", WEST", "CENTER")
    def getMove(self, info):
        pass
    
    # Give your character.
    # @returns Whichever character represents this critter.
    def getChar(self):
        pass
    
    # End of fight shenanigans.
    # @param kill Boolean; true if defending critter was killed, false otherwise
    # @param oppFight Opponent's TheirCritterInfo (health, stats, char, color, type)
    # @returns Nothing.
    def fightOver(self, kill, oppFight):
        pass

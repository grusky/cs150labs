import critter
import critter_main
import collections
import color
import inspect
import random
import os
import pprint
import math

# Just an (x, y) pair, but more readable.
Point = collections.namedtuple('Point', ['x', 'y'])

# To keep track of stats
Stats = collections.namedtuple('Stats', ['attack', 'defense'])

# Again, we don't really need a whole class just to store this info.
YourCritterInfo = collections.namedtuple('YourCritterInfo', ['getSquare', 'getHealth', 'getStats', 'getChar', 'getColor', 'getType'])
TheirCritterInfo = collections.namedtuple('TheirCritterInfo', ['getHealth', 'getStats', 'getChar', 'getColor', 'getType'])

class CritterModel():
    """
    The main Critter simulation. Takes care of all the logic of
    Critter fights.
    """
    
    def __init__(self, width, height, functions):
        self.width = width
        self.height = height
        self.critters = []
        # How many turns have gone by
        self.turn_count = 0
        # How many critters have gone this turn
        self.move_count = 0
        # A map of critters to their attack and defence values.
        self.critter_stats = {}
        # A map of critters to (x, y) positions.
        self.critter_positions = {}
        # A map of critter classes to the number alive of that class.
        self.critter_class_states = {}
        # A map of critters to health points
        self.critter_healths = {}
        # A set containing all critters that qualify for a defense bonus
        self.still_critters = set()
        # A list of (x, y) indices corresponding to the critters
        self.grid = [[None for x in range(height)] for y in range(width)]
        # Just try to hack this.
        self.critter_functions = {}
        self.model_functions = functions

    def add(self, critter, num):
        """
        Adds a particular critter type num times. The critter should
        be a class, not an instantiated critter.
        """
        if critter not in self.critter_class_states:
            self.critter_class_states[critter] = ClassInfo(initial_count=num)
        self.critter_class_states[critter].alive += num
        for i in range(num):
            args = self.model_functions['create_parameters'](critter)
            pos = self.model_functions['random_location'](self)
            c = critter(*(pos + args))
            self.critter_stats[c] = Stats(*(self.critter_functions[c.__class__]['getStats'](c)))
            self.model_functions['verify_stats'](self, c.__class__.__name__, self.critter_stats[c])
            self.critters.append(c)
            self.still_critters.add(c)
            self.critter_positions[c] = pos
            self.critter_healths[c] = 50.0
            self.grid[pos.x][pos.y] = c
    
    def reset(self, num_critters):
        '''
        Resets the model, clearing out the whole board and
        repopulating it with num_critters of the same Critter types.
        '''
        self.grid = [[None for x in range(self.height)] for y in range(self.width)]
        self.critter_positions = {}
        self.critter_healths = {}
        self.still_critters = set()
        self.critters = []
        self.turn_count = 0
        critter_classes = set(self.critter_class_states.keys())
        self.critter_class_states = {}
        for critter_class in critter_classes:
            self.model_functions['add'](self, critter_class, num_critters)

    def tick(self):
        if len(self.critters) == 0:
            self.model_functions['increment_move_count'](self)
            return None, Point(0, 0), Point(0, 0)
        critter1 = self.critters[self.move_count]
        old_position = self.critter_positions[critter1]
        direction = self.critter_functions[critter1.__class__]['getMove'](critter1, YourCritterInfo(*self.model_functions['get_square_funcs'](self, critter1.__class__.__name__, old_position)))
        new_position = self.model_functions['move'](self, critter1.__class__.__name__, direction, old_position)
        if new_position == old_position:
            self.still_critters.add(critter1)
            self.model_functions['increment_move_count'](self)
            return critter1, old_position, new_position
        elif critter1 in self.still_critters:
            self.still_critters.remove(critter1)
        critter2 = self.grid[new_position.x][new_position.y]
        if critter2 and isinstance(critter2, Point_Cache):
            if critter2.attacker and isinstance(critter2.attacker, critter1.__class__) and critter2.attacker != critter1:
                self.critter_class_states[critter1.__class__].bonus += critter2.points
                self.critter_positions.pop(critter2)
            else:
                critter2.attacker = critter1
                new_position = old_position
        elif critter2 and new_position != old_position:
            kill = self.model_functions['fight'](self, critter1, critter2)
            self.critter_functions[critter1.__class__]['fightOver'](critter1, kill,
                                                                     TheirCritterInfo(
                                                                         lambda: self.critter_healths[critter2],
                                                                         lambda: (self.critter_stats[critter2].attack, self.critter_stats[critter2].defense * (2 if critter2 in self.still_critters else 1)),
                                                                         lambda: self.critter_functions[critter2.__class__]['getChar'](critter2),
                                                                         lambda: self.model_functions['get_color'](self, critter2),
                                                                         lambda: critter2.__class__.__name__))
            self.critter_functions[critter2.__class__]['fightOver'](critter2, kill,
                                                                     TheirCritterInfo(
                                                                         lambda: self.critter_healths[critter1],
                                                                         lambda: (self.critter_stats[critter1].attack, self.critter_stats[critter1].defense),
                                                                         lambda: self.critter_functions[critter1.__class__]['getChar'](critter1),
                                                                         lambda: self.model_functions['get_color'](self, critter1),
                                                                         lambda: critter1.__class__.__name__))
            if kill:
                if self.critters.index(critter2) < self.move_count:
                    self.move_count -= 1
                self.critter_positions.pop(critter2)
                self.critter_positions[critter1] = new_position
                self.critters.remove(critter2)
                self.still_critters.discard(critter2)
                self.critter_class_states[critter2.__class__].alive -= 1
                self.critter_class_states[critter1.__class__].kills += 1
            else:
                new_position = old_position
        self.grid[old_position.x][old_position.y] = None
        self.grid[new_position.x][new_position.y] = critter1
        self.critter_positions[critter1] = new_position
        self.model_functions['increment_move_count'](self)
        return critter1, old_position, new_position

    def increment_move_count(self):
        self.move_count += 1
        if self.move_count >= len(self.critters):
            self.move_count = 0
            self.turn_count += 1
            random.shuffle(self.critters)

    def award_bonuses(self):
        for c in self.critter_class_states:
            self.critter_class_states[c].bonus += self.critter_class_states[c].alive

    def create_point_cache(self):
        pos = self.model_functions['random_location'](self)
        c = Point_Cache(*self.model_functions['create_parameters'](Point_Cache))
        self.critter_positions[c] = pos
        self.grid[pos.x][pos.y] = c
        return c, pos, pos

    def move(self, critterName, direction, pos):
        """
        Returns the new position after moving in direction. This
        assumes that (0, 0) is the top-left.
        """
        if direction == "NORTH":
            return Point(pos.x, (pos.y - 1) % self.height)
        elif direction == "SOUTH":
            return Point(pos.x, (pos.y + 1) % self.height)
        elif direction == "EAST":
            return Point((pos.x + 1) % self.width, pos.y)
        elif direction == "WEST":
            return Point((pos.x - 1) % self.width, pos.y)
        elif direction == "CENTER":
            return pos
        else:
            raise LocationException("A%s %s critter has tried to go %s, which is not a valid direction." % (self.model_functions['vowel'](critterName), critterName, direction))
    
    def observe(self, x, y, position):
        """
        Returns the new position after moving x right and y up
        from position. This assumes (0, 0) is the top-left.
        """
        return Point((position.x + x) % self.width, (position.y - y) % self.height)
    
    def fight(self, critter1, critter2):
        """
        Force poor innocent Critters to fight to the death for the
        entertainment of Oberlin students. Returns true if the aggravator
        was successful in eliminating their opponent.
        """
        attack = self.critter_stats[critter1].attack
        defense = self.critter_stats[critter2].defense
        if critter2 in self.still_critters:
            defense *= 2
        self.critter_healths[critter2] -= self.get_damage(attack, defense)
        if self.critter_healths[critter2] < 0:
            self.critter_healths[critter2] = 0
        return self.critter_healths[critter2] == 0
    
    def get_damage(self, attack, defense):
        result = attack - defense
        return result if result > 0 else 0

    def get_color(self, critter):
        "Ask the critter for a color, and make sure it won't cause any errors."
        values = ('red', 'green', 'blue')
        result = self.critter_functions[critter.__class__]['getColor'](critter)
        if not isinstance(result, color.Color):
            raise ColorException("A%s %s critter has tried to return a color of type %s: %s, which is not actually a color." % (self.model_functions['vowel'](critter.__class__.__name__), critter.__class__.__name__, type(result), result))
        for c in range(3):
            if result[c] > 255:
                raise ColorException("A%s %s critter has tried to return a color with a %s value of %d, which is too high." % (self.model_functions['vowel'](critter.__class__.__name__), critter.__class__.__name__, values[c], result[c]))
            elif result[c] < 0:
                raise ColorException("A%s %s critter has tried to return a color with a %s value of %d, which is too low." % (self.model_functions['vowel'](critter.__class__.__name__), critter.__class__.__name__, values[c], result[c]))
        return result

    def verify_stats(self, critterName, stats):
        """
        Make sure levels are within the acceptable range.
        """
        values = ('attack', 'defense')
        if sum(stats) > 100:
            raise StatsException("The stats total for a%s %s critter is %d (%d attack and %d defense), which is too high." % (self.model_functions['vowel'](critterName), critterName, sum(stats), stats.attack, stats.defense))
        for s in range(2):
            if stats[s] > 100:
                raise StatsException("The %s for a%s %s critter is %d, which is too high." % (values[s], self.model_functions['vowel'](critterName), critterName, stats[s]))
            if stats[s] < 0:
                raise StatsException("The %s for a%s %s critter is %d, which is too low." % (values[s], self.model_functions['vowel'](critterName), critterName, stats[s]))
    
    def verify_observe(self, critterName, x, y):
        "Limit obervation capabilities."
        if math.hypot(x, y) > 3:
            raise ObservationException("A%s %s critter has tried to see a square %.2f squares away: (%d, %d), which is too far." % (self.model_functions['vowel'](critterName), critterName, math.hypot(x, y), x, y))

    def vowel(name):
        "I hope nobody names their critter Yvonne."
        return 'n' if (len(name) > 0 and name[0] in 'aeiouAEIOU') else ''

    def random_location(self):
        """
        Calculate a random location for a Critter to be placed. Now
        guaranteed to terminate (as long as there is at least one free
        space).

        Returns a 2-tuple of integers.
        """
        x = random.randint(0, self.width-1)
        y = random.randint(0, self.height-1)
        while self.grid[x][y] is not None:
            x += 1
            if x >= self.width:
                x = 0
                y += 1
                if y >= self.height:
                    y = 0
        return Point(x, y)
    
    def create_parameters(critter_class):
        """
        This is a bit funky. Because not all Critters take the same
        arguments in their constructor (for example, a Mouse gets a
        color while a Hippo gets an int), we need to check the
        classname and return appropriate things based on that. The
        Java version is a bit nicer because it has access to type
        information for each parameter, but c'est la vie.
        
        Return value is a tuple, which will be passed as *args to
        the critter's constructor.
        """
        if critter_class.__name__ == 'Mouse':
            return (color.getRandomColor(),)
        elif critter_class.__name__ == 'Hippo':
            return (random.randint(1, 15),)
        elif critter_class.__name__ == "Point_Cache":
            return random.randrange(1, 11), color.getRandomColor()
        else:
            return ()

    def get_square_funcs(self, critterName, position):
        "Returns the surrounding info for a particular position."
        def getSquare(x, y):
            neighbor_pos = self.model_functions['observe'](self, x, y, position)
            self.model_functions['verify_observe'](self, critterName, x, y)
            neighbor = self.grid[neighbor_pos.x][neighbor_pos.y]
            if neighbor:
                if neighbor.__class__ == Point_Cache:
                    return TheirCritterInfo(0, (0, 0),
                                            neighbor.getChar(), self.model_functions['get_color'](self, neighbor),
                                            "Point Cache")
                return TheirCritterInfo(self.critter_healths[neighbor],
                                        self.critter_stats[neighbor],
                                        neighbor.getChar(), self.model_functions['get_color'](self, neighbor),
                                        neighbor.__class__.__name__)
            return TheirCritterInfo(0, (0, 0), '.', color.BLACK, '.')
        def getHealth(x, y):
            return getSquare(x, y).getHealth
        def getStats(x, y):
            return getSquare(x, y).getStats
        def getChar(x, y):
            return getSquare(x, y).getChar
        def getColor(x, y):
            return getSquare(x, y).getColor
        def getType(x, y):
            return getSquare(x, y).getType
        return getSquare, getHealth, getStats, getChar, getColor, getType

    def results(self):
        """
        Returns the critters in the simulation, sorted by alive+kills+bonus.
        results()[0] is (overall winner, state of winner).
        """
        return sorted(self.critter_class_states.items(),
                      key=lambda state: -(state[1].kills + state[1].alive + state[1].bonus))

class Point_Cache(critter.Critter):
    
    def __init__(self, points, color):
        self.points = points
        self.attacker = None
        self.color = color
    
    def getMove(self, info):
        return "CENTER"

    def getChar(self):
        return str(self.points)
    
    def getColor(self):
        return self.color

class ClassInfo():
    """
    This would be a named tuple, but they're immutable and that's
    somewhat unwieldy for this particular case.
    """
    def __init__(self, kills=0, alive=0, bonus = 0, initial_count=0):
        self.kills = kills
        self.alive = alive
        self.bonus = bonus
        self.count = initial_count
    
    def __repr__(self):
        return '%s %s %s' % (self.kills, self.alive, self.count)

# These exceptions don't really need fancy names
class StatsException(Exception):
    pass

class LocationException(Exception):
    pass

class ObservationException(Exception):
    pass

class ColorException(Exception):
    pass

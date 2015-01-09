#!/usr/bin/env python3
import tkinter as tk
import color
import critter
import random


EMPTY_CHAR = '.'


class CritterGUI():

    def __init__(self, model, gui_functions, defaults, scale, num_critters):
        # Remember the attached model
        self.model = model
        # Secure all the gui functions
        self.gui_functions = gui_functions
        # Added to accomodate smaller screen sizes without the need for hardcoding. Set to 15 for normal size, increase for larger, and decrease for smaller.
        self.SCALE_FACTOR = scale
        # Remember how many of each to create
        self.num_critters = num_critters
        # Secure all the critter functions
        self.critter_functions = self.model.critter_functions
        # Keep track of whether the simulation is currently running or not.
        self.is_running = False
        # Award bonuses this many turns
        self.BONUS_TERM_LENGTH = 100
        # How likely each turn is to produce a Point Cache
        self.POINT_CACHE_ODDS = 0.1
        # Adjust dimensions according to scale parameter
        self.width = self.SCALE_FACTOR*self.model.width
        self.height = self.SCALE_FACTOR*self.model.height
        # Set the general window up, including labels for turn count and scores
        self.gui_functions['initialize_graphics'](self, defaults)
        # Display current critter model.
        self.gui_functions['draw_world'](self)
        # Play/Pause, Turn, Tick, Reset, Quit, speed bar
        self.gui_functions['make_buttons'](self)
        # Hotkeys for buttons and speed adjustment
        self.gui_functions['bind_keys'](self)
        # Keep the window open (similar to using input(), except this isn't a total hack and actually makes sense)
        self.root.mainloop()

    def initialize_graphics(self, defaults):
        # The window
        self.root = tk.Tk()
        self.root.grid()
        
        # The critter world
        self.canvas = tk.Canvas(self.root, bg="white", width=self.width, height=self.height)
        self.canvas.grid(columnspan=25, rowspan=10, sticky='W')
        
        # Squares of the critter world
        self.chars = [[self.canvas.create_text((x * self.SCALE_FACTOR + 7.5, y * self.SCALE_FACTOR + 7.5), text='', font=('Courier New', -self.SCALE_FACTOR))
                       for y in range(self.model.height)]
                      for x in range(self.model.width)]

        # Class states (static label)
        tk.Label(self.root, text='Classes (Alive + Kill + Bonus = Total):').grid(column=25, row=0, columnspan=3)

        # Class states (dynamic labels)
        # Keep the students' critters at the top of the list
        if len(self.model.critters) > 0:
                max_name = max([c.__name__ for c in self.model.critter_class_states])
                self.critter_classes = sorted(self.model.critter_class_states, key=lambda x: x.__name__ if x.__name__ not in defaults else max_name + x.__name__)
        else:
                self.critter_classes = []
        self.class_state_labels = {}
        row = 2
        for c in self.critter_classes:
            self.class_state_labels[c.__name__] = tk.Label(self.root, text=c.__name__+": {0} + 0 + 0 = {0}".format(self.num_critters))
            self.class_state_labels[c.__name__].grid(column=25, row=row)
            row = row + 1

        # Turn count
        self.turn_count = 0
        self.turn_count_label = tk.Label(self.root, text='0 moves')
        self.turn_count_label.grid(column=3, row=10)

    def make_buttons(self):
        # Play/Pause - start and stop the simulation
        self.play_pause_button = tk.Button(self.root, text='Play', bg='green',
                                     width=6, command=lambda: self.gui_functions['play_pause'](self))
        self.play_pause_button.grid(column=8, row=10)

        # Turn - pause simulation if still running; if not, finish current turn
        self.turn_button = tk.Button(self.root, text='Turn', bg='red',
                                     width=6, command=lambda *args: self.gui_functions['play_pause'](self) if self.is_running else self.gui_functions['turn'](self))
        self.turn_button.grid(column=9, row=10)

        # Tick - pause simulation if still running; if not, move one critter
        self.tick_button = tk.Button(self.root, text='Tick', bg='yellow',
                                     width=6, command=lambda *args: self.gui_functions['play_pause'](self) if self.is_running else self.gui_functions['tick'](self))
        self.tick_button.grid(column=10, row=10)

        # Reset - stop running, display a new critter model.
        self.reset_button = tk.Button(self.root, text='Reset', bg ='blue',
                                     width=6, command=lambda *args: self.gui_functions['reset'](self))
        self.reset_button.grid(column=11, row=10)

        # Quit - close window, exit program
        self.quit_button = tk.Button(self.root, text='Quit', bg='white',
                                     width=6, command=lambda *args: exit())
        self.quit_button.grid(column=12, row=10)

        # Speed - how long between turns
        self.speed_label = tk.Label(self.root, text='Speed:')
        self.speed_label.grid(column=0, row=10)
        self.speed_var = tk.IntVar()
        self.speed_var.set(10)
        self.scale = tk.Scale(self.root, variable=self.speed_var, orient='horizontal',
                              length=100, sliderlength=10, from_=1, to=200)
        self.scale.grid(column=1, row=10)

    def bind_keys(self):
        """
        Add hotkeys for buttons and speed adjustment.
        """
        self.root.bind("<Up>", lambda *args: self.gui_functions['change_speed'](self, 1))
        self.root.bind("<Down>", lambda *args: self.gui_functions['change_speed'](self, -1))
        self.root.bind("<Shift-Up>", lambda *args: self.gui_functions['change_speed'](self, 10))
        self.root.bind("<Shift-Down>", lambda *args: self.gui_functions['change_speed'](self, -10))
        self.root.bind("<Control-Up>", lambda *args: self.gui_functions['change_speed'](self, 200))
        self.root.bind("<Control-Down>", lambda *args: self.gui_functions['change_speed'](self, -200))
        self.root.bind("p", lambda *args: self.gui_functions['play_pause'](self))
        self.root.bind("P", lambda *args: self.gui_functions['play_pause'](self))
        self.root.bind("<Pause>", lambda *args: self.gui_functions['play_pause'](self))
        self.root.bind("<space>", lambda *args: self.gui_functions['play_pause'](self))
        self.root.bind("t", lambda *args: self.gui_functions['turn'](self))
        self.root.bind("<Return>", lambda *args: self.gui_functions['turn'](self))
        self.root.bind("T", lambda *args: self.gui_functions['tick'](self))
        self.root.bind("<Shift-Return>", lambda *args: self.gui_functions['tick'](self))
        self.root.bind("r", lambda *args: self.gui_functions['reset'](self))
        self.root.bind("R", lambda *args: self.gui_functions['reset'](self))
        self.root.bind("<BackSpace>", lambda *args: self.gui_functions['reset'](self))
        self.root.bind("q", lambda *args: exit())
        self.root.bind("Q", lambda *args: exit())
        self.root.bind("<Escape>", lambda *args: exit())

    def change_speed(self, amount):
        """
        Change the speed of the simulation. Only used with hotkey bindings for speed adjustment.
        """
        new_speed = self.speed_var.get() + amount
        new_speed = min(max(new_speed, 0), 200)
        self.speed_var.set(new_speed)

    def draw_char(self, char, color, x, y):
        """
        Displays a single char at position (x, y) on the canvas.
        """
        self.canvas.itemconfig(self.chars[x][y], text=char, fill=self.gui_functions['color_to_hex'](color), font='Courier %d bold' % ((13 * self.SCALE_FACTOR) // 15))

    def draw_world(self):
        """
        Draw all characters representing critters or empty spots.
        """
        for x in range(self.model.width):
            for y in range(self.model.height):
                critter = self.model.grid[x][y]
                if critter:
                    self.gui_functions['draw_char'](self, self.critter_functions[critter.__class__]['getChar'](critter), self.gui_functions['process_color'](self, critter), x, y)
                else:
                    self.gui_functions['draw_char'](self, EMPTY_CHAR, color.BLACK, x, y)

    def draw_critter(self, critter, old_position, new_position):
        """
        Would only draw critters that have moved, but some may still have changed their character or color
        and it'd be too much to verify that as well, so just draw everything that gets passed in here.
        Only draw blanks if they've moved, though, and since this only moves one critter at a time, we
        know for sure that if it did move, it left a blank space behind it. Have to verify each critter
	is not None as well, in case the model is running on empty.

        """
        if critter:
                if new_position != old_position:
                    self.gui_functions['draw_char'](self, EMPTY_CHAR, color.BLACK, old_position.x, old_position.y)
                self.gui_functions['draw_char'](self, self.critter_functions[critter.__class__]['getChar'](critter), self.gui_functions['process_color'](self, critter), new_position.x, new_position.y)

    def process_color(self, critter):
        """
        Processes the colors for critters according to health remaining (Point Caches default to 50),
        in order to fade colors as their health decreases.
        """
        health = self.model.critter_healths.get(critter, 50)
        results = []
        for value in self.model.model_functions['get_color'](self.model, critter):
            results += [255 - (health * (255 - value) // 50)]
        return color.Color(*results)

    def update(self):
        """
        Repeatedly updates the GUI with the appropriate characters and colors from
        the critter simulation, until stop button is pressed to pause simulation. 
        """
        if self.is_running == True:
            self.gui_functions['turn'](self)
            self.root.after(500//self.speed_var.get(), self.update)

    def update_turn_count(self):
        """
        Update turn count to match model's. Have to directly copy from model to avoid
        confusion with individual ticks occuring. Take care of potential longevity
        bonuses as well, along with new Point Cache generation.
        """
        if self.turn_count != self.model.turn_count:
            self.turn_count = self.model.turn_count
            self.turn_count_label.config(text=str(self.turn_count)+' moves')
            if self.turn_count % self.BONUS_TERM_LENGTH == 0:
                self.model.model_functions['award_bonuses'](self.model)
            # Can't add a Point Cache to a completely filled-up world
            if random.random() > (1 - self.POINT_CACHE_ODDS) and len(self.model.critters) < critter.WORLD_SIZE.x * critter.WORLD_SIZE.y:
                self.gui_functions['draw_critter'](self, *self.model.model_functions['create_point_cache'](self.model))
            return True
        return False

    def update_class_states(self):
        """
        Change the display of states of all the critter classes.
        """
        for c in self.model.critter_class_states:
            alive = self.model.critter_class_states[c].alive
            kills = self.model.critter_class_states[c].kills
            bonus = self.model.critter_class_states[c].bonus
            total = alive + kills + bonus
            self.class_state_labels[c.__name__].config(text=c.__name__+": {} + {} + {} = {}".format(alive, kills, bonus, total))

    def play_pause(self):
        "Start/stop the simulation."
        if not self.is_running:
            self.is_running = True
            self.gui_functions['update'](self)
            self.play_pause_button.config(text='Pause')
        else:
            self.is_running = False
            self.play_pause_button.config(text='Play')

    def turn(self):
        "Move all remaining critters by one step."
        moves = []
        while not self.gui_functions['update_turn_count'](self):
            moves.append(self.model.model_functions['tick'](self.model))
        for move in moves:
            self.gui_functions['draw_critter'](self, *move)
        self.gui_functions['update_class_states'](self)

    def tick(self):
        "Move one critter by 1 step."
        self.gui_functions['draw_critter'](self, *self.model.model_functions['tick'](self.model))
        self.gui_functions['update_turn_count'](self)
        self.gui_functions['update_class_states'](self)

    def reset(self):
        "Stop simulation, reset critter model and display of scores and critter world."
        self.is_running = False
        self.model.model_functions['reset'](self.model, self.num_critters)
        self.gui_functions['draw_world'](self)
        self.turn_count = 0
        self.turn_count_label.config(text='0 moves')
        self.gui_functions['update_class_states'](self)

    def color_to_hex(color):
        """
        Converts RGB colors to hex string, because tkinter thought that
        passing numeric types as strings was an AWESOME idea.
        """
        return '#%02x%02x%02x'.upper() % (color.r, color.g, color.b)

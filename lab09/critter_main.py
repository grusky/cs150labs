#!/usr/bin/env python3
# Possible previous author: Peter Fogg
#
# Chris Egerton
# Updated January - February 2014
# Updated October - November 2014
# "It's a time-honored tradition to try to hack the critter lab."
# -Anonymous lab helper



# TODO
#
# Rewrite directory scanning to accomodate for running program from directory other
# than home directory.
#
# Secure Point Caches and other free-floating module attributes
#
# CDB

import argparse
import critter
import critter_model
import critter_gui
import copy
import imp
import inspect
import os
import random
import sys

STANDARD_CRITTERS = []
for name in {"stone", "mouse", "hippo", "lion", "chameleoturtle"}:
    try:
        exec("from %s import %s" % (name, name.capitalize()))
        STANDARD_CRITTERS.append(eval(name.capitalize()))
    except Exception as e:
        pass

def get_critters(directory='.'):
    """
    Finds all modules containing critter classes in the given directory
    and returns the classes they contain in a list. Only classes which
    subclass Critter (and aren't the Critter class itself) will be included.
    """
    modules = [file_name[:-3] for file_name in os.listdir(directory) if file_name.endswith('.py')]
    critters = []
    functions = {}
    for module_name in modules:
        module = __import__(module_name)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj not in critters and issubclass(obj, critter.Critter):
                if name.lower() == module_name.lower() and not(obj == critter_model.Point_Cache or obj == critter.Critter):
                    functions[obj] = {}
                    # In case somebody tries to mess with their opponents.
                    imp.reload(module)
                    for fun in {'getChar', 'getMove', 'getStats', 'getColor', 'fightOver'}:
                        if hasattr(obj, fun):
                            functions[obj][fun] = copy.deepcopy(module.__dict__[name].__dict__.get(fun, critter.Critter.__dict__[fun]))
                    critters.append(obj)
                elif inspect.isclass(obj) and module == critter_model and obj.__name__ == "Point_Cache":
                    functions[obj] = {}
                    for fun in {'getChar', 'getColor'}:
                        functions[obj][fun] = copy.deepcopy(critter_model.Point_Cache.__dict__[fun])
    return critters, functions

def format_results(results):
    "Returns the results of a critter fight in a nice format."
    return '\n'.join(['%s:\t\t\t%s kills %3s alive %3s bonus %3s total' % (critter_class.__name__, state.kills, state.alive, state.bonus, state.kills + state.alive + state.bonus)
                      for critter_class, state in results])

def get_class(crittername, critterlist):
    """
    Returns the string name of a critter into the actual class
    object, if it's in critterlist. Otherwise return None.
    """
    for c in critterlist:
        if c.__name__.lower() == crittername.lower():
            return c
    return None

def get_fighters(names, critters):
    result = []
    for fighter in names:
        if fighter.lower() == "standard":
            result.extend(STANDARD_CRITTERS)
        else:
            critter_class = get_class(fighter, critters)
            if critter_class:
                result.append(critter_class)
            elif fighter.lower() != "none":
                print("\nCritter " + fighter + " not found.\n")
    return result

def secure(obj):
    result = {}
    for name, fun in inspect.getmembers(obj, inspect.isfunction):
        result[name] = copy.deepcopy(fun)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quickfight', action="store_true", help="Simulates a fight between all specified critters without a GUI", required=False)
    parser.add_argument('--critters', help="Simulates a fight between all specified critters with a GUI", nargs='+', required=False)
    parser.add_argument('--rounds', help="Specify the number of rounds to be played (only useful with quickfight)", type=int, required=False)
    parser.add_argument('--size', help="Specify how many of each critter to create", type=int, required=False)
    parser.add_argument('--scale', help="Specify an integer for how large the display window should be; default is 15", type=int, required=False)
    args = parser.parse_args()
    model_functions = secure(critter_model.CritterModel)
    gui_functions = secure(critter_gui.CritterGUI)
    model = critter_model.CritterModel(60, 50, model_functions)
    critter_classes, critter_functions = get_critters()
    if args.critters:
        critter_classes = get_fighters(set(args.critters), critter_classes)
    real_size = max(0, min(args.size, critter.WORLD_SIZE.x * critter.WORLD_SIZE.y // len(critter_classes))) if args.size else 25
    for critter_class in critter_classes:
        model.critter_functions[critter_class] = critter_functions[critter_class]
        model_functions['add'](model, critter_class, real_size)
    model.critter_functions[critter_model.Point_Cache] = critter_functions[critter_model.Point_Cache]
    random.shuffle(model.critters)
    if args.quickfight:
        rounds = args.rounds if args.rounds else 150
        while model.turn_count < rounds:
            model_functions['tick'](model)
        print(format_results(model_functions['results'](model)))
    else:
        critter_gui.CritterGUI(model, gui_functions, [critter_class.__name__ for critter_class in STANDARD_CRITTERS], max(1, args.scale) if args.scale else 15, real_size)
    
if __name__ == '__main__':
    main()

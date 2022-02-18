import src.Exceptions as Exception
from src.Parser import Parser
from src.Interpreteur import Interpreteur
import time
import sys

import json
settings = json.load(open("settings.json", "r"))
ERROR_MESSAGE = settings["main"]["ERROR_MESSAGE"]

args = sys.argv
if len(sys.argv) < 2:
    raise Exception.NotEnoughArguments(ERROR_MESSAGE)
debug = ("-d" in sys.argv, "-dp" in sys.argv or "-d" in sys.argv, "-di" in sys.argv or "-d" in sys.argv, "-o" in sys.argv)

arguments = False
liste_argv = []
for arg in sys.argv:
    if arg == "-a":
        arguments = True
    elif arg == "-A":
        arguments = False
    elif arguments:
        liste_argv.append(arg)

if "-p" in sys.argv:
    temps = time.time()
    print("Début de la compilation")
    parser = Parser(debug[1], debug[3])
    parser.getstr(sys.argv[1])
    parser.generateinstructions()
    if not debug : print(parser.instructions)
    print(f"Compilation terminée en {time.time()-temps}s")
else:
    temps = time.time()
    print("Début de la compilation")
    parser = Parser(debug[1], debug[3])
    parser.getstr(sys.argv[1])
    parser.generateinstructions()
    print(f"Compilation terminée en {time.time()-temps}s")
    print("Début de l'interpretation")
    temps = time.time()
    interpreteur = Interpreteur(debug[2], debug[3], liste_argv)
    interpreteur.run(parser.instructions)
    print(f"Interpretation terminée en {time.time()-temps}s")
    
import src.Exceptions as Exception
from src.Parser import Parser
from src.Interpreteur import Interpreteur
import sys

import json
settings = json.load(open("settings.json", "r"))
ERROR_MESSAGE = settings["main"]["ERROR_MESSAGE"]

args = sys.argv
if len(sys.argv) < 2:
    raise Exception.NotEnoughArguments(ERROR_MESSAGE)
debug = ("-d" in sys.argv, "-dp" in sys.argv or "-d" in sys.argv, "-di" in sys.argv or "-d" in sys.argv)
if "-p" in sys.argv:
    parser = Parser(debug[1])
    parser.getstr(sys.argv[1])
    parser.generateinstructions()
    if not debug : print(parser.instructions)
else:
    parser = Parser(debug[1])
    parser.getstr(sys.argv[1])
    parser.generateinstructions()
    interpreteur = Interpreteur(debug[2])
    interpreteur.run(parser.instructions)
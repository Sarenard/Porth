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
if "-p" in sys.argv:
    parser = Parser("-d" in sys.argv)
    parser.getstr(sys.argv[1])
    parser.generateinstructions()
    print(parser.instructions)
else:
    parser = Parser("-d" in sys.argv)
    parser.getstr(sys.argv[1])
    parser.generateinstructions()
    interpreteur = Interpreteur("-d" in sys.argv)
    interpreteur.run(parser.instructions)
from src.Instructions import I
import src.Exceptions as Exceptions

import json
settings = json.load(open("settings.json", "r"))
MACRO_MAX = settings["parser"]["MACRO_MAX"]
INCLUDE_MAX = settings["parser"]["INCLUDE_MAX"]

def replace(liste, element, truc):
    liste2 = []
    for x in liste:
        if x == element:
            liste2 += truc
        else:
            liste2.append(x)
    return liste2

class Parser:
    def __init__(self, debug):
        self.content = []
        self.instructions = []
        self._if = False
        self.temp_if = []
        self._macro = False
        self.temp_macro = []
        self._while = False
        self.temp_while = []
        self.debug = debug
        self.total_include = 0
        self.total_macros = 0
    def getstr(self, file):
        if self.debug : print(open(file).read().replace("\n", "\\n"))
        self.content = [x for x in (" ".join(" ".join(open(file).read().split(" ")).split("\n"))).split(" ") if x != ""]
        if self.debug : print(self.content)
    def generateinstructions(self):
        self.content = self.parse_includes(self.content)
        self.content = self.parse_macros(self.content)
        x = 0
        while True:
            try:
                element = self.content[x]
            except:
                break
            adder = self.instructions
            if self._if:
                adder = self.temp_if
            if self._macro:
                adder = self.temp_macro
            if self._while:
                adder = self.temp_while
            if element.isnumeric():
                adder.append((I.PUSHINT, element))
            elif element == ".":
                adder.append((I.PRINT,))
            elif element == "+":
                adder.append((I.ADD,))
            elif element == "ipt":
                element = input()
                if element.isnumeric():
                    adder.append((I.PUSHINT, element))
            elif element == "dup":
                adder.append((I.DUP,))
            elif element == "2dup":
                adder.append((I.DUP2,))
            elif element == "swap":
                adder.append((I.SWAP, ))
            elif element == "over":
                adder.append((I.OVER, ))
            elif element == "*":
                adder.append((I.MUL,))
            elif element == "drop":
                adder.append((I.DROP, ))
            elif element == "-":
                adder.append((I.SUB,))
            elif element == "=":
                adder.append((I.EQUAL,)) 
            elif element == ">" :
                adder.append((I.BIGGER,))
            elif element == "nand":
                adder.append((I.NAND,))
            elif element == "rot":
                adder.append((I.ROTATE,))
            elif element == "if":
                self._if = True
            elif element == "true":
                adder.append((I.TRUE,))
            elif element == "false":
                adder.append((I.FALSE,))
            elif element == "macro":
                self._macro = True
                self.temp_macro.append(self.content[x+1])
            elif element == "#include":
                adder.append((I.INCLUDE, self.content[x+1]))
                x += 1
            elif element == "div":
                adder.append((I.DIV, ))
            elif element == "while":
                self._while = True
            elif element == "end":
                if self._if:
                    self._if = False
                    self.instructions.append((I.IF, self.temp_if))
                    self.temp_if = []
                if self._macro:
                    self._macro = False
                    self.instructions.append((I.MACRO, self.temp_macro[0], self.temp_macro[2:]))
                    self.temp_macro = []
                if self._while:
                    self._while = False
                    self.instructions.append((I.WHILE, self.temp_while))
                    self.temp_while = []
            else:
                if element != "":
                    adder.append((I.MACROWORD, element))
            x += 1
        if self.debug : print("Instructions", self.instructions)
    def check_for_infinite_loop(self):
        if self.total_macros > MACRO_MAX:
            raise Exceptions.TooManyNestedMacros("Too many nested macros")
        if self.total_include > INCLUDE_MAX:
            raise Exceptions.TooManyNestedIncludes("Too many nested includes")
    def parse_includes(self, instructions):
        if self.debug : print("includes avant :", instructions)
        liste_includes = []
        for i in range(len(instructions)-1):
            if instructions[i] == "#include":
                liste_includes.append((instructions[i], instructions[i+1]))
                instructions[i] = instructions[i]+" "+instructions[i+1]
                del instructions[i+1]
        for include in liste_includes:
            content = open(include[1]).read().replace("\n", " ").split(" ")
            instructions = replace(instructions, include[0]+" "+include[1], content)
        if self.debug : print("includes après :", instructions)
        instructions = [x.replace("\n", " ") for x in instructions if x not in ["", " ", "\n"]]
        instructions2 = []
        for truc in instructions:
            if truc.startswith("\n"):
                instructions2.append(truc.split("\n")[1])
            elif truc.endswith("\n"):
                instructions2.append(truc.split("\n")[0])
            else:
                instructions2.append(truc)
        instructions = instructions2
        if sum([True for x in instructions if x == "#include"]) > 0:
            self.total_include += 1
            self.check_for_infinite_loop()
            instructions = self.parse_includes(instructions)
        return instructions
    def parse_macros(self, content, macros_total=[]):
        if "iteration" not in globals() : globals()["iteration"]=1
        else: globals()["iteration"] += 1
        if self.debug : print(f"macros avant (iteration {globals()['iteration']}) :", content)
        macros_total = macros_total
        macro_temp = []
        macro_en_cours = False
        content_remplacement = []
        end_compteur = 0
        for i in range(len(content)):
            if not macro_en_cours and content[i] != "macro" : content_remplacement.append(content[i])
            if content[i] == "macro":
                macro_en_cours = True
            if content[i] in ["if", "while"]:
                end_compteur += 1
            if content[i] == "end":
                if end_compteur == 0:
                    macro_en_cours = False
                    try:
                        macros_total.append((macro_temp[1], macro_temp[2:]))
                    except:
                        pass
                    macro_temp = []
                else:
                    end_compteur -= 1
            if macro_en_cours:
                macro_temp.append(content[i])
        content = content_remplacement
        if self.debug : print(f"macros pendant (iteration {globals()['iteration']}) : macros:{macros_total}, content:{content}")
        content_remplacement = []
        for i in range(len(content)):
            for macro in macros_total:
                if macro[0] == content[i]:
                    content_remplacement += macro[1]
            else:
                if not sum([macro[0] == content[i] for macro in macros_total]) :
                    content_remplacement.append(content[i])
        content = content_remplacement
        if self.debug : print(f"macros après (iteration {globals()['iteration']}) :", content)
        if sum([True for macro in macros_total for i in range(len(content)) if macro[0] == content[i]]):
            self.total_macros += 1
            self.check_for_infinite_loop()
            content = self.parse_macros(content, macros_total)
        return content
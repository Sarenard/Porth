from src.Instructions import I, Type
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
    def __init__(self, debug, debug_output):
        self.content = []
        self.instructions = []
        self.debug_output = debug_output
        self.debug = debug
        self.total_include = 0
        self.total_macros = 0
        self.instructions_temporaires = []
        self.liste_included = []
        self.in_liste = False
    def getstr(self, file):
        if self.debug : print(open(file).read().replace("\n", "\\n"))
        if self.debug_output : print(open(file).read().replace("\n", "\\n"), file=open("debug.txt", "w"), flush=True)
        self.content = [x for x in (" ".join(" ".join("".join([x for x in open(file).readlines() if not x.lstrip().startswith("//")]).split(" ")).split("\n"))).replace("    ", " ").split(" ") if x != ""]
        if self.debug : print(self.content)
        if self.debug_output : print(self.content, file=open("debug.txt", "a"), flush=True)
    def generateinstructions(self): # sourcery no-metrics
        self.content = self.parse_includes(self.content)
        self.content = self.parse_macros(self.content)
        x = 0
        a = 0
        adder = self.instructions
        while True:
            try:
                element = self.content[x]
            except:
                break
            if self.debug : print(f"\nInstruction (debut {a}) : \"{element}\"\n{self.instructions=}\n{self.instructions_temporaires=}")
            if self.debug_output : print(f"\nInstruction (debut {a}) : \"{element}\"\n{self.instructions=}\n{self.instructions_temporaires=}", file=open("debug.txt", "a"), flush=True)
            if element.startswith("["):
                self.in_liste=True
                self.instructions_temporaires.append([])
            if element.endswith("]"):
                self.in_liste=False
                self.instructions_temporaires[-1].append(element)
                total = []
                in_string = False
                string = ""
                for truc in self.instructions_temporaires[-1]:
                    if truc.startswith("\""):
                        string += f"{str(truc)} "
                        in_string=True
                    elif truc.endswith("\""):
                        string += f"{str(truc)} "
                        in_string=False
                        total.append(string[1:-2])
                    elif in_string:
                        string += f"{str(truc)} "
                    else:
                        total.append(truc)
                total[0], total[-1] = total[0][1:], total[-1][:-1]
                total2 = [(Type.INT, int(element), ) if element.isnumeric() else (Type.STRING, element, ) for element in total]
                self.instructions.append((I.PUSHLIST, total2[1:-1], ))
                self.instructions_temporaires.pop()
            elif self.in_liste:
                self.instructions_temporaires[-1].append(f"{element}")
            elif element.isnumeric():
                if self.in_liste:
                    self.instructions_temporaires[-1].append(element)
                else:
                    adder.append((I.PUSHINT, element))
            elif element == ".":
                adder.append((I.PRINT,))
            elif element in ["expand", "exp"]:
                adder.append((I.EXPEND, ))
            elif element == "in":
                adder.append((I.IN, ))
            elif element == "out":
                adder.append((I.OUT, ))
            elif element == "+":
                adder.append((I.ADD,))
            elif element in ["ipt", ","]:
                adder.append((I.INPUT, ))
            elif element == "dup":
                adder.append((I.DUP,))
            elif element == "split":
                adder.append((I.SPLIT, ))
            elif element == "2dup":
                adder.append((I.DUP2,))
            elif element == "lstack":
                adder.append((I.STACK_LEN, ))
            elif element == "over":
                 adder.append((I.OVER, ))
            elif element == "@=":
                adder.append((I.VARSET, ))
            elif element == "@!":
                adder.append((I.VARGET, ))
            elif element == "dropvar":
                adder.append((I.DROP_VAR, ))
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
            elif element.startswith("rot"):
                if element == "rot":
                    adder.append((I.ROTATE, 3, ))
                else:
                    adder.append((I.ROTATE, int(element[3:]), ))
            elif element == "true":
                adder.append((I.TRUE,))
            elif element == "false":
                adder.append((I.FALSE,))
            elif element == "#include":
                adder.append((I.INCLUDE, self.content[x+1]))
                x += 1
            elif element == "div":
                adder.append((I.DIV, ))
            elif element == "if":
                self.instructions_temporaires.append([])
                adder = self.instructions_temporaires[-1]
                adder.append((I.IF, ))
            elif element == "while":
                self.instructions_temporaires.append([])
                adder = self.instructions_temporaires[-1]
                adder.append((I.WHILE, ))
            elif element == "end":
                if len(self.instructions_temporaires) == 1:
                    adder = self.instructions
                    adder.append(self.instructions_temporaires[0])
                    self.instructions_temporaires = []
                else:
                    self.instructions_temporaires[-2] += [self.instructions_temporaires[-1]]
                    del self.instructions_temporaires[-1]
                    adder = self.instructions_temporaires[-1]
            elif element.startswith("\""):
                string = element.split("\"")[1]
                while not element.endswith("\""):
                    x += 1
                    element = self.content[x]
                    if "\"" in element:
                        string += " "+element.split("\"")[0]
                    else:
                        string += " "+element
                if self.in_liste:
                    self.instructions_temporaires[-1].append(element)
                else:
                    adder.append((I.PUSHSTRING, string))
            else:
                if element != "":
                    adder.append((I.MACROWORD, element))
            if self.debug : print(f"Etape fin {a} :\n{self.instructions=}\n{self.instructions_temporaires=}\n")
            if self.debug_output : print(f"Etape fin {a} :\n{self.instructions=}\n{self.instructions_temporaires=}\n", file=open("debug.txt", "a"), flush=True)
            x += 1
            a += 1
        self.instructions = self.traiter_ifs(self.instructions)
        if self.debug : print("\n\nInstructions finales :", self.instructions)
        if self.debug_output : print("\n\nInstructions finales :", self.instructions, file=open("debug.txt", "a"), flush=True)
    def traiter_ifs(self, instructions):
        if self.debug : print("ifs avant :", instructions)
        if self.debug_output : print("ifs avant :", instructions, file=open("debug.txt", "a"), flush=True)
        nouvelles_instructions = []
        for instruction in instructions:
            if isinstance(instruction, tuple):
                nouvelles_instructions.append(instruction)
            elif instruction[0] == (I.IF, ):
                dans_le_if = self.traiter_ifs(instruction)
                dans_le_if.pop(0)
                nouvelles_instructions.append((I.IF, dans_le_if))
            elif instruction[0] == (I.WHILE, ):
                dans_le_if = self.traiter_ifs(instruction)
                dans_le_if.pop(0)
                nouvelles_instructions.append((I.WHILE, dans_le_if))
        if self.debug : print("ifs apres :", nouvelles_instructions)
        if self.debug_output : print("ifs apres :", nouvelles_instructions, file=open("debug.txt", "a"), flush=True)
        return nouvelles_instructions
    def check_for_infinite_loop(self):
        if self.total_macros > MACRO_MAX:
            raise Exceptions.TooManyNestedMacros("Too many nested macros")
        if self.total_include > INCLUDE_MAX:
            raise Exceptions.TooManyNestedIncludes("Too many nested includes")
    def parse_includes(self, instructions):
        if self.debug : print("includes avant :", instructions, "liste modules inclus:", self.liste_included)
        if self.debug_output : print("includes avant :", instructions, "liste modules inclus:", self.liste_included, file=open("debug.txt", "a"), flush=True)
        liste_includes = []
        for i in range(len(instructions)-2):
            if instructions[i] == "#include":
                if instructions[i+1] not in self.liste_included:
                    self.liste_included.append(instructions[i+1])
                    liste_includes.append((instructions[i], instructions[i+1]))
                    instructions[i] = f'{instructions[i]} {instructions[i+1]}'
                    del instructions[i+1]
                else:
                    self.liste_included.append(instructions[i+1])
                    # liste_includes.append((instructions[i], instructions[i+1]))
                    instructions[i] = f'{instructions[i]} {instructions[i+1]}'
                    del instructions[i+1]
                    del instructions[i]
        for include in liste_includes:
            content = open(include[1]).read().replace("\n", " ").split(" ")
            instructions = replace(instructions, f'{include[0]} {include[1]}', content)
        if self.debug : print("includes apres :", instructions, "liste modules inclus:", self.liste_included)
        if self.debug_output : print("includes apres :", instructions, "liste modules inclus:", self.liste_included, file=open("debug.txt", "a"), flush=True)
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
        if sum(True for x in instructions if x == "#include") > 0:
            self.total_include += 1
            self.check_for_infinite_loop()
            instructions = self.parse_includes(instructions)
        return instructions
    def parse_macros(self, content, macros_total=[]):  # sourcery no-metrics skip: comprehension-to-generator, default-mutable-arg, hoist-statement-from-if, swap-nested-ifs
        if "iteration" not in globals() : globals()["iteration"]=1
        else: globals()["iteration"] += 1
        if self.debug : print(f"macros avant (iteration {globals()['iteration']}) :", content)
        if self.debug_output : print(f"macros avant (iteration {globals()['iteration']}) :", content, file=open("debug.txt", "a"), flush=True)
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
        if self.debug_output : print(f"macros pendant (iteration {globals()['iteration']}) : macros:{macros_total}, content:{content}", file=open("debug.txt", "a"), flush=True)
        content_remplacement = []
        for item in content:
            for macro in macros_total:
                if macro[0] == item:
                    content_remplacement += macro[1]
            if not sum(macro[0] == item for macro in macros_total):
                content_remplacement.append(item)
        content = content_remplacement
        if self.debug : print(f"macros après (iteration {globals()['iteration']}) :", content)
        if self.debug_output : print(f"macros après (iteration {globals()['iteration']}) :", content, file=open("debug.txt", "a"), flush=True)
        if sum([macro[0] == content[i] for macro in macros_total for i in range(len(content))]):
            self.total_macros += 1
            self.check_for_infinite_loop()
            content = self.parse_macros(content, macros_total)
        return content
from src.Instructions import I, Type
import src.Exceptions as Exceptions
from sys import exit

#convert

class Interpreteur:
    def __init__(self, debug, debug_output):
        self.debug = debug
        self.debug_output = debug_output
        self.stack = []
        self.stack_storage = []
        self.variables = {}
    def run(self, instructions):
        for instruction in instructions:
            if self.debug :
                print("instruction :", instruction)
                print("stack :", self.stack)
                print("stack_storage :", self.stack_storage)
                print(self.variables)
            if self.debug_output :
                print("instruction :", instruction, file=open("debug.txt", "a"), flush=True)
                print("stack :", self.stack, file=open("debug.txt", "a"), flush=True)
                print("stack_storage :", self.stack_storage,  file=open("debug.txt", "a"), flush=True)
                print(self.variables, file=open("debug.txt", "a"), flush=True)
            match instruction:
                case I.PUSHLIST, liste, :
                    self.stack.append((Type.LIST, liste))
                case I.VARSET, :
                    name = self.stack.pop()
                    value = self.stack.pop()
                    self.variables[name[1]] = value
                case I.STACK_LEN, :
                    self.stack.append((Type.INT, len(self.stack)))
                case I.SPLIT, :
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if a[1] == "":
                        for x in b[1]:
                            self.stack.append((Type.STRING, x))
                    else:
                        for x in b[1].split(a[1].replace("\\N", "")):
                            self.stack.append((Type.STRING, x))
                case I.VARGET, :
                    name = self.stack.pop()
                    self.stack.append(self.variables[name[1]])
                case I.DROP_VAR, :
                    name = self.stack.pop()
                    try:
                        self.variables.pop(name[1])
                    except KeyError:
                        raise Exceptions.VariableNotFound(f"Variable {name[1]} not found")
                case I.PUSHINT, nb:
                    self.stack.append((Type.INT, int(nb)))
                case I.PUSHSTRING, texte:
                    self.stack.append((Type.STRING, texte))
                case I.ADD, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack in the ADD, needed 2, got " + str(len(self.stack)))
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if b[0] == Type.INT and a[0] == Type.INT:
                        self.stack.append((Type.INT, int(a[1]) + int(b[1])))
                    elif b[0] == Type.STRING and a[0] == Type.STRING:
                        self.stack.append((Type.STRING, a[1] + b[1]))
                    elif b[0] == Type.STRING and a[0] == Type.INT:
                        self.stack.append((Type.STRING, str(a[1]) + b[1]))
                    elif b[0] == Type.INT and a[0] == Type.STRING:
                        self.stack.append((Type.STRING, a[1] + str(b[1])))
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack in the ADD, needed INT+INT, STRING+STRING, INT+STRING or STRING+INT, got " + str(a[0]) + " and " + str(b[0]))
                case I.PRINT, :
                    if len(self.stack) < 1 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack in the PRINT, needed 1, got " + str(len(self.stack)))
                    a = self.stack.pop()
                    if a[0] == Type.LIST:
                        print([truc[1] for truc in a[1]], end="")
                    elif a[0] == Type.STRING :
                        a = (Type.STRING, a[1].replace("\\n", "\n"))
                        a = (Type.STRING, a[1].replace("\\033", "\033"))
                        a = (Type.STRING, a[1].replace("\\N", ""))
                        print(a[1], end="")
                    elif a[0] == Type.INT:
                        print(a[1], end="")
                    elif a[0] == Type.BOOL:
                        print(a[1], end="")
                case I.READ, :
                    name = self.stack.pop()
                    if not name[0] == Type.STRING:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack in the READ, needed STRING, got " + str(name[0]))
                    content = open(name[1], "r").read()
                    self.stack.append((Type.STRING, content))
                case I.WRITE, :
                    name = self.stack.pop()
                    if not name[0] == Type.STRING:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack in the READ, needed STRING, got " + str(name[0]))
                    string = self.stack.pop()[1]
                    with open(name[1], "w") as file:
                        file.write(string)
                case I.EXIT, :
                    exit(1)
                case I.IN, :
                    liste = self.stack.pop()
                    if liste[0] != Type.LIST:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack in the IN, needed LIST, got " + str(liste[0]))
                    self.stack_storage = [x for x in self.stack]
                    self.stack = liste[1]
                case I.OUT, :
                    self.stack = [x for x in self.stack_storage]
                    self.stack_storage = []
                case I.EXPEND, :
                    liste = self.stack.pop()
                    for x in liste[1]:
                        self.stack.append(x)
                case I.INPUT, :
                    element = input()
                    if element.isnumeric():
                        self.stack.append((I.PUSHINT, element))
                    else:
                        self.stack.append((I.PUSHSTRING, element))
                case I.TRUE, :
                    self.stack.append((Type.BOOL, True))
                case I.CONVERT, :
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if a[0] == Type.INT:
                        self.stack.append((a[0], int(b[1])))
                    if a[0] == Type.BOOL:
                        self.stack.append((a[0], b[1]))
                case I.FALSE, :
                    self.stack.append((Type.BOOL, False))
                case I.DUP, :
                    if len(self.stack) < 1 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack in the DUP, needed 1, got " + str(len(self.stack)))  
                    a = self.stack.pop()
                    self.stack.append(a)
                    self.stack.append(a)
                case I.ROTATE, nb, :
                    # ex : 
                    # 5 4 3 rot ==> 4 3 5
                    if len(self.stack) < nb : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stackin the ROTATE, needed " + str(nb) + ", got " + str(len(self.stack)))
                    liste = [self.stack.pop() for _ in range(nb)]
                    self.stack.append(liste[0])
                    for x in range(nb-1, 0, -1):
                        self.stack.append(liste[x])
                case I.DUP2, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack in the DUP2, needed 2, got " + str(len(self.stack)))
                    a = self.stack.pop()
                    b = self.stack.pop()
                    self.stack.append(b)
                    self.stack.append(a)
                    self.stack.append(b)
                    a = self.stack.pop()
                    b = self.stack.pop()
                    self.stack.append(b)
                    self.stack.append(a)
                    self.stack.append(b)
                case I.DROP, :
                    if len(self.stack) < 1 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack in the DROP, needed 1, got " + str(len(self.stack)))
                    a = self.stack.pop()
                case I.NAND, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack in the NAND, needed 2, got " + str(len(self.stack)))
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if a[0] == Type.BOOL and b[0] == Type.BOOL:
                        self.stack.append((Type.BOOL, not (a[1] and b[1])))
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack in the NAND, needed BOOL+BOOL, got " + str(a[0]) + " and " + str(b[0]))
                case I.OVER, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack in the OVER, needed 2, got " + str(len(self.stack)))
                    a = self.stack.pop()
                    b = self.stack.pop()
                    self.stack.append(b)
                    self.stack.append(a)
                    self.stack.append(b)
                case I.MUL, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack in the MUL, needed 2, got " + str(len(self.stack)))
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if b[0] == Type.INT and a[0] == Type.INT:
                        self.stack.append((Type.INT, b[1]*a[1]))
                    elif b[0] == Type.STRING and a[0] == Type.INT:
                        self.stack.append((Type.STRING, b[1]*a[1]))
                    elif b[0] == Type.LIST and a[0] == Type.INT:
                        self.stack.append((Type.LIST, b[1]*a[1]))
                    elif b[0] == Type.INT and a[0] == Type.LIST:
                        self.stack.append((Type.LIST, b[1]*a[1]))
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack in the MUL, needed INT+INT or STRING+INT, got " + str(a[0]) + " and " + str(b[0]))
                case I.APPEND, :
                    valeur = self.stack.pop()
                    liste = self.stack.pop()
                    liste[1].append(valeur)
                    self.stack.append((Type.LIST, liste[1]))
                case I.REMOVE, :
                    liste = self.stack.pop()
                    element = liste[1].pop()
                    self.stack.append((Type.LIST, liste[1][0:len(liste[1])]))
                    self.stack.append(element)
                case I.DIV, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack in the DIV, needed 2, got " + str(len(self.stack)))
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if b[0] == Type.INT and a[0] == Type.INT:
                        self.stack.append((Type.INT, b[1]//a[1]))
                        self.stack.append((Type.INT, b[1]%a[1]))
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack in the DIV, needed INT+INT, got " + str(a[0]) + " and " + str(b[0]))
                case I.EQUAL, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack in the EQUAL, needed 2, got " + str(len(self.stack)))
                    a = self.stack.pop()
                    b = self.stack.pop()
                    self.stack.append((Type.BOOL, b==a))
                case I.BIGGER, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack in the BIGGER, needed 2, got " + str(len(self.stack)))
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if b[0] == Type.INT and a[0] == Type.INT:
                        self.stack.append((Type.BOOL, b[1]>a[1]))
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack in the BIGGER, needed INT+INT, got " + str(a[0]) + " and " + str(b[0]))
                case I.SUB, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack in the SUB, needed 2, got " + str(len(self.stack)))
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if b[0] == Type.INT and a[0] == Type.INT:
                        self.stack.append((Type.INT, int(b[1])-int(a[1])))
                case I.IF, instructions:
                    if len(self.stack) < 1 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack in the IF, needed 1, got " + str(len(self.stack)))
                    a = self.stack.pop()
                    if a[0] == Type.BOOL:
                        if a[1] == True:
                            self.run(instructions)
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack in the IF, needed BOOL, got " + str(a[0]))
                case I.WHILE, instructions:
                    while True:
                        if len(self.stack) < 1 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack in the WHILE, needed 1, got " + str(len(self.stack)))
                        a = self.stack.pop()
                        if a[0] == Type.BOOL:
                            if a[1] == True:
                                self.run(instructions)
                            else:
                                break
                        else:
                            raise Exceptions.BadTypesOnTheStack("Bad types on the stack in the WHILE, needed BOOL, got " + str(a[0]))
            if self.debug:
                print("stack :", self.stack)
                print("stack_storage :", self.stack_storage)
                print(self.variables, "\n")
            if self.debug_output:
                print("stack :", self.stack, file=open("debug.txt", "a"), flush=True)
                print("stack_storage :", self.stack_storage, file=open("debug.txt", "a"), flush=True)
                print(self.variables, "\n", file=open("debug.txt", "a"), flush=True)
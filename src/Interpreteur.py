from src.Instructions import I, Type
import src.Exceptions as Exceptions

class Interpreteur:
    def __init__(self, debug):
        self.debug = debug
        self.stack = []
    def run(self, instructions):
        for instruction in instructions:
            if self.debug :
                print(instruction)
                print(self.stack)
            match instruction:
                case I.PUSHINT, nb:
                    self.stack.append((Type.INT, int(nb)))
                case I.PUSHSTRING, texte:
                    self.stack.append((Type.STRING, texte))
                case I.ADD, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if b[0] == Type.INT and a[0] == Type.INT:
                        self.stack.append((Type.INT, a[1] + b[1]))
                    elif b[0] == Type.STRING and a[0] == Type.STRING:
                        self.stack.append((Type.STRING, a[1] + b[1]))
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack")
                case I.PRINT, :
                    if len(self.stack) < 1 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    if a[0] == Type.STRING :
                        a = (Type.STRING, a[1].replace("\\n", "\n"))
                        a = (Type.STRING, a[1].replace("\\033", "\033"))
                        a = (Type.STRING, a[1].replace("\\N", ""))
                    print(a[1], end="")
                case I.TRUE, :
                    self.stack.append((Type.BOOL, True))
                case I.FALSE, :
                    self.stack.append((Type.BOOL, False))
                case I.DUP, :
                    if len(self.stack) < 1 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    self.stack.append(a)
                    self.stack.append(a)
                case I.ROTATE, nb, :
                    if len(self.stack) < nb : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    liste = [self.stack.pop() for _ in range(nb)]
                    self.stack.append(liste[0])
                    for x in range(nb-1, 0, -1):
                        self.stack.append(liste[x])
                case I.DUP2, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
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
                    if len(self.stack) < 1 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                case I.NAND, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if a[0] == Type.BOOL and b[0] == Type.BOOL:
                        self.stack.append((Type.BOOL, not (a[1] and b[1])))
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack")
                case I.OVER, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    b = self.stack.pop()
                    self.stack.append(b)
                    self.stack.append(a)
                    self.stack.append(b)
                case I.MUL, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if b[0] == Type.INT and a[0] == Type.INT:
                        self.stack.append((Type.INT, b[1]*a[1]))
                    elif b[0] == Type.STRING and a[0] == Type.INT:
                        self.stack.append((Type.STRING, b[1]*a[1]))
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack")
                case I.DIV, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if b[0] == Type.INT and a[0] == Type.INT:
                        self.stack.append((Type.INT, b[1]//a[1]))
                        self.stack.append((Type.INT, b[1]%a[1]))
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack")
                case I.EQUAL, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    b = self.stack.pop()
                    self.stack.append((Type.BOOL, b==a))
                case I.BIGGER, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if b[0] == Type.INT and a[0] == Type.INT:
                        self.stack.append((Type.BOOL, b[1]>a[1]))
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack")
                case I.SUB, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if b[0] == Type.INT and a[0] == Type.INT:
                        self.stack.append((Type.INT, b[1]-a[1]))
                case I.IF, instructions:
                    if len(self.stack) < 1 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    if a[0] == Type.BOOL:
                        if a[1] == True:
                            self.run(instructions)
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack")
                case I.WHILE, instructions:
                    while True:
                        if len(self.stack) < 1 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                        a = self.stack.pop()
                        if a[0] == Type.BOOL:
                            if a[1] == True:
                                self.run(instructions)
                            else:
                                break
                        else:
                            raise Exceptions.BadTypesOnTheStack("Bad types on the stack")
            if self.debug:
                print(self.stack, "\n")
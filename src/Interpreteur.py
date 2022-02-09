from src.Instructions import I, Type
import src.Exceptions as Exceptions

class Interpreteur:
    def __init__(self, debug):
        self.debug = debug
        self.stack = []
        self._if = False
    def run(self, instructions):
        x = 0
        while True:
            try:
                instruction = instructions[x]
            except:
                if self._if:
                    self._if = False
                    return
                break
            match instruction:
                case I.PUSHINT, nb:
                    self.stack.append((Type.INT, int(nb)))
                case I.ADD, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if b[0] == Type.INT and a[0] == Type.INT:
                        self.stack.append((Type.INT, a[1] + b[1]))
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack")
                case I.PRINT, :
                    if len(self.stack) < 1 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    print(a[1])
                case I.TRUE, :
                    self.stack.append((Type.BOOL, True))
                case I.FALSE, :
                    self.stack.append((Type.BOOL, False))
                case I.DUP, :
                    if len(self.stack) < 1 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    self.stack.append(a)
                    self.stack.append(a)
                case I.ROTATE, :
                    if len(self.stack) < 3 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    b = self.stack.pop()
                    c = self.stack.pop()
                    self.stack.append(a)
                    self.stack.append(b)
                    self.stack.append(c)
                case I.DUP2, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    b = self.stack.pop()
                    self.stack.append(a)
                    self.stack.append(b)
                    self.stack.append(a)
                    self.stack.append(b)
                case I.SWAP, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    b = self.stack.pop()
                    self.stack.append(a)
                    self.stack.append(b)
                case I.DROP, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
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
                    self.stack.append((Type.BOOL, b[1]))
                    self.stack.append((Type.BOOL, a[1]))
                    self.stack.append((Type.BOOL, b[1]))
                case I.MUL, :
                    if len(self.stack) < 2 : raise Exceptions.NotEnoughStuffOnTheStack("Not enough stuff on the stack")
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if b[0] == Type.INT and a[0] == Type.INT:
                        self.stack.append((Type.INT, b[1]*a[1]))
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
                    if b[0] == Type.INT and a[0] == Type.INT:
                        self.stack.append((Type.BOOL, b[1]==a[1]))
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack")
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
                            self._if = True
                            self.run(instructions)
                    else:
                        raise Exceptions.BadTypesOnTheStack("Bad types on the stack")
            x += 1
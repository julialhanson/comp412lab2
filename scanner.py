import io
import sys
# Array to represent the words:
# 0: store, 1: sub, 2: load, 3: loadl, 4: lshift, 5: rshift, 6: mult,
# 7: add, 8: nop, 9: output, 10: =>, 11: ',', 12: EOL, 13: EOF

##loadi, nop, output defined in other constants

SUB = 3
STORE = 4
LOAD = 5
# INTO, COMMA, EOL, EOF shared
LSHIFT = 10
RSHIFT = 14
MULT = 12
ADD = 13

# add constant category that is just number

LOADI = 0
NOP = 1
OUTPUT = 2
ARITHOP = 3
MEMOP = 4
CONSTANT = 5
INTO = 6
COMMA = 7
EOL = 8
EOF = 9
REGISTER = 10
COMMENT = 11

ERROR = -1

okEndChars = ['\n', '/']

# Array to represent the categories, it goes like so:
class Scanner():
    def __init__(self, filename):
        self.filename = filename
        self.eof = False
        self.buffer = open(filename, "r", encoding="utf-8")
        self.line = ""
        self.i = 0
        self.maxreg = 0
        self.error = ""
        self.linenum = 0
        self.wordArr = ["loadI", "nop", "output", "sub", "store", "load", "=>", ',', "\\n",  "", "lshift", "COMMENT", "mult", "add", "rshift"]
        self.categoryArr = ["LOADI", "NOP", "OUTPUT", "ARITHOP", "MEMOP",  "CONSTANT", "INTO", "COMMA", "EOL", "EOF", "REGISTER", "COMMENT"]
        pass
    
    def getLine(self):
        return self.linenum
    
    def getMaxReg(self):
        return self.maxreg
    
    def getEOF(self):
        return self.eof

    def readLine(self):
        self.line = self.buffer.readline()
        if (len(self.line) == 0 or self.line[-1] != '\n'):
            self.line += (ascii(7))
        self.linenum += 1
        self.i = 0
        
    def readWord(self):
        
        while (self.line[self.i].isspace()):
            if (self.line[self.i] == '\n'):
                self.readLine()
                return (EOL, EOL)
            if (self.line[self.i]== '\r'):
                self.i += 1
                if (self.line[self.i] == '\n'):
                    self.readLine()
                    return (EOL, EOL)
                else:
                    print("ERROR: " + str(self.linenum) + "\\r must be followed by \\n.", file=sys.stderr)
                    self.readLine()
                    return (ERROR, ERROR)
            self.i += 1
        
        if(self.line[self.i] == ascii(7)):
            self.eof = True
            return (EOF, EOF) 
        
        word = ""
        
        # handling the words sub, store
        if self.line[self.i] == 's':
            self.i += 1
            if self.line[self.i] == 'u':
                self.i += 1
                if self.line[self.i] == 'b':
                    self.i += 1
                    if self.line[self.i].isspace():
                        return (ARITHOP, SUB)
                    else:
                        print("ERROR " + str(self.linenum) + ": sub" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                        self.readLine()
                        return(ERROR, ERROR)
                else:
                    print("ERROR " + str(self.linenum) + ": su" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                    self.readLine()
                    return(ERROR, ERROR)
            elif self.line[self.i] == 't':
                self.i += 1
                if self.line[self.i] == 'o':
                    self.i += 1
                    if self.line[self.i] == 'r':
                        self.i += 1
                        if self.line[self.i] == 'e':
                            self.i += 1
                            if self.line[self.i].isspace():
                                return (MEMOP, STORE)
                            else: 
                                print("ERROR " + str(self.linenum) + ": store" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                                self.readLine()
                                return(ERROR, ERROR)
                        else:
                            print("ERROR " + str(self.linenum) + ": stor" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                            self.readLine()
                            return(ERROR, ERROR)
                    else:
                        print("ERROR " + str(self.linenum) + ": sto" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                        self.readLine()
                        return(ERROR, ERROR)
                else:
                    print("ERROR " + str(self.linenum) + ": st" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                    self.readLine()
                    return(ERROR, ERROR)
            else:
                print("ERROR " + str(self.linenum) + ": s" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                self.readLine()
                return(ERROR, ERROR)
        # handling words lshift, loadI, load
        elif self.line[self.i] == 'l':
            self.i += 1
            if self.line[self.i] == 's':
                self.i += 1
                if self.line[self.i] == 'h':
                    self.i += 1
                    if self.line[self.i] == 'i':
                        self.i += 1
                        if self.line[self.i] == 'f':
                            self.i += 1
                            if self.line[self.i] == 't':
                                self.i += 1
                                if self.line[self.i].isspace():
                                    return (ARITHOP, LSHIFT)
                                else: 
                                    print("ERROR " + str(self.linenum) + ": lshift" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                                    self.readLine()
                                    return(ERROR, ERROR)
                            else:
                                print("ERROR " + str(self.linenum) + ": lshif" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                                self.readLine()
                                return(ERROR, ERROR)
                        else:
                            print("ERROR " + str(self.linenum) + ": lshi" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                            self.readLine()
                            return(ERROR, ERROR)
                    else:
                        print("ERROR " + str(self.linenum) + ": lsh" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                        self.readLine()
                        return(ERROR, ERROR)
                else:
                    print("ERROR " + str(self.linenum) + ": ls" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                    self.readLine()
                    return(ERROR, ERROR)
            elif self.line[self.i] == 'o':
                self.i += 1
                if self.line[self.i] == 'a':
                    self.i += 1
                    if self.line[self.i] == 'd':
                        self.i += 1
                        if self.line[self.i] == 'I':
                            self.i += 1
                            if self.line[self.i].isspace():
                                return (LOADI, LOADI)
                            else:
                                print("ERROR " + str(self.linenum) + ": loadI" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                                self.readLine()
                                return(ERROR, ERROR)
                        elif self.line[self.i].isspace():
                            return (MEMOP, LOAD)
                        else:
                            print("ERROR " + str(self.linenum) + ": load" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                            self.readLine()
                            return(ERROR, ERROR)
                    else:
                        print("ERROR " + str(self.linenum) + ": loa" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                        self.readLine()
                        return(ERROR, ERROR)
                else:
                    print("ERROR " + str(self.linenum) + ": lo" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                    self.readLine()
                    return(ERROR, ERROR)
            else: 
                print("ERROR " + str(self.linenum) + ": l" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                self.readLine()
                return(ERROR, ERROR)
        #handling rshift and registers
        elif self.line[self.i] == 'r':
            self.i += 1
            if self.line[self.i] == 's':
                self.i += 1
                if self.line[self.i] == 'h':
                    self.i += 1
                    if self.line[self.i] == 'i':
                        self.i += 1
                        if self.line[self.i] == 'f':
                            self.i += 1
                            if self.line[self.i] == 't':
                                self.i += 1
                                if self.line[self.i].isspace():
                                    return (ARITHOP, RSHIFT)
                                else: 
                                    print("ERROR " + str(self.linenum) + ": rshift" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                                    self.readLine()
                                    return(ERROR, ERROR)
                            else:
                                print("ERROR " + str(self.linenum) + ": rshif" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                                self.readLine()
                                return(ERROR, ERROR)
                        else:
                            print("ERROR " + str(self.linenum) + ": rshi" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                            self.readLine()
                            return(ERROR, ERROR)
                    else:
                        print("ERROR " + str(self.linenum) + ": rsh" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                        self.readLine()
                        return(ERROR, ERROR)
                else:
                    print("ERROR " + str(self.linenum) + ": rs" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                    self.readLine()
                    return(ERROR, ERROR)
            #handling consonants
            elif ord(self.line[self.i]) >= 48 and ord(self.line[self.i]) <= 57:
                regstr = ""
                while self.i < len(self.line) and (ord(self.line[self.i]) >= 48 and ord(self.line[self.i]) <= 57):
                    regstr = regstr + self.line[self.i]
                    self.i += 1
                    if int(regstr) > self.maxreg:
                        self.maxreg = int(regstr)
                return(REGISTER, int(regstr))
            else:
                print("ERROR " + str(self.linenum) + ": r" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                self.readLine()
                return(ERROR, ERROR)
        elif self.line[self.i] == 'm':
            self.i += 1
            if self.line[self.i] == 'u':
                self.i += 1
                if self.line[self.i] == 'l':
                    self.i += 1
                    if self.line[self.i] == 't':
                        self.i += 1
                        if self.line[self.i].isspace():
                            return (ARITHOP, MULT)
                        else:
                            print("ERROR " + str(self.linenum) + ": mult" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                            self.readLine()
                            return(ERROR, ERROR)
                    else:
                        print("ERROR " + str(self.linenum) + ": mul" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                        self.readLine()
                        return(ERROR, ERROR)
                else:
                    print("ERROR " + str(self.linenum) + ": mu" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                    self.readLine()
                    return(ERROR, ERROR)
            else:
                print("ERROR " + str(self.linenum) + ": m" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                self.readLine()
                return(ERROR, ERROR)
        elif self.line[self.i] == 'a':
            self.i += 1
            if self.line[self.i] == 'd':
                self.i += 1
                if self.line[self.i] == 'd':
                    self.i += 1
                    if self.line[self.i].isspace():
                        return (ARITHOP, ADD)
                    else:
                        print("ERROR " + str(self.linenum) + ": add" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                        self.readLine()
                        return(ERROR, ERROR)
                else:
                    print("ERROR " + str(self.linenum) + ": ad" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                    self.readLine()
                    return(ERROR, ERROR)
            else:
                print("ERROR " + str(self.linenum) + ": a" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                self.readLine()
                return(ERROR, ERROR)
        elif self.line[self.i] == 'n':
            self.i += 1
            if self.line[self.i] == 'o':
                self.i += 1
                if self.line[self.i] == 'p':
                    self.i += 1
                    if self.line[self.i].isspace():
                        return (NOP, NOP)
                    else:
                        print("ERROR " + str(self.linenum) + ": nop" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                        self.readLine()
                        return(ERROR, ERROR)
                else:
                    print("ERROR " + str(self.linenum) + ": no" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                    self.readLine()
                    return(ERROR, ERROR)
            else:
                print("ERROR " + str(self.linenum) + ": n" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                self.readLine()
                return(ERROR, ERROR)
        elif self.line[self.i] == 'o':
            self.i += 1
            if self.line[self.i] == 'u':
                self.i += 1
                if self.line[self.i] == 't':
                    self.i += 1
                    if self.line[self.i] == 'p':
                        self.i += 1
                        if self.line[self.i] == 'u':
                            self.i += 1
                            if self.line[self.i] == 't':
                                self.i += 1
                                if self.line[self.i].isspace():
                                    return (OUTPUT, OUTPUT)
                                else:
                                    print("ERROR " + str(self.linenum) + ": output" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                                    self.readLine()
                                    return(ERROR, ERROR)
                            else:
                                print("ERROR " + str(self.linenum) + ": outpu" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                                self.readLine()
                                return(ERROR, ERROR)
                        else:
                            print("ERROR " + str(self.linenum) + ": outp" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                            self.readLine()
                            return(ERROR, ERROR)
                    else:
                        print("ERROR " + str(self.linenum) + ": out" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                        self.readLine()
                        return(ERROR, ERROR)
                else:
                    print("ERROR " + str(self.linenum) + ": ou" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                    self.readLine()
                    return(ERROR, ERROR)
            else:
                print("ERROR " + str(self.linenum) + ": o" + self.line[self.i] + " is not a valid string", file=sys.stderr)
                self.readLine()
                return(ERROR, ERROR)
        elif self.line[self.i] == '=':
            self.i += 1
            if self.line[self.i] == '>':
                self.i += 1
                return (INTO, INTO)
        elif self.line[self.i] == ',':
            self.i += 1
            return (COMMA, COMMA)
        elif self.line[self.i] == '/':
            self.i += 1
            if self.line[self.i] == '/':
                self.readLine()
                return (EOL, EOL)
            else:
                print("ERROR " + str(self.linenum) + ": / must be followed by another /", file=sys.stderr)
                self.readLine()
                return (ERROR, ERROR)
        elif self.line[self.i] == '\n':
            self.readLine()
            return (EOL, EOL) 
        elif self.line[self.i] == '\r':
            self.i += 1
            if self.line[self.i] == '\n':
                self.readLine()
                return (EOL, EOL) 
        elif ord(self.line[self.i]) <= 57 and ord(self.line[self.i]) >= 48:
            constr = ""
            while ord(self.line[self.i]) <= 57 and ord(self.line[self.i]) >= 48:
                constr = constr + self.line[self.i]
                self.i += 1
            return (CONSTANT, int(constr))
                           
        else:
            # print(self.line[self.i])
            print("ERROR " + str(self.linenum) + ": " + self.line[self.i] + " is not a valid starting character", file=sys.stderr)
            self.readLine()
            return(ERROR, ERROR)
    
        
    
import os
from sys import argv
from scanner import Scanner

# Constants from other file
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
INVALID = -2

errorflag = False
wordArr = ["loadI", "nop", "output", "sub", "store", "load", "=>", ',', "\\n",  "", "lshift", "COMMENT", "mult", "add", "rshift"]

maxreg = 0

class IRNode:
    def __init__(self, linenum, sr1: int = None, sr2: int = None, sr3: int = None) -> None:
        self.linenum = linenum
        self.opcode = 0
        self.sr1 = sr1
        self.sr2 = sr2
        self.sr3 = sr3
        self.vr1 = None
        self.vr2 = None
        self.vr3 = None
        self.pr1 = None
        self.pr2 = None
        self.pr3 = None
        self.nu1 = None
        self.nu2 = None
        self.nu3 = None
        self.prev = self
        self.next = self
        pass
    
    def getOpcode(self):
        return self.opcode
    
    def insertAfter(self, node):
        self.next.prev = node
        node.next = self.next
        node.prev = self
        self.next = node
        
    def __str__(self) -> str:
        return f"{wordArr[self.opcode]}     [{self.sr1}], [{self.sr2}], [{self.sr3}], [{self.vr1}], [{self.vr2}], [{self.vr3}], [{self.pr1}], [{self.pr2}], [{self.pr3}], [{self.nu1}], [{self.nu2}], [{self.nu3}]"
    
    def printVR(self):
        if (self.opcode == LOAD):
            print(f"{wordArr[self.opcode]} r{self.vr1} => r{self.vr3}")
        elif (self.opcode == STORE):
            print(f"{wordArr[self.opcode]} r{self.vr1} => r{self.vr2}")
        elif (self.opcode == LOADI):
            print(f"{wordArr[self.opcode]} {self.vr1} => r{self.vr3}")
        elif (self.opcode == ADD or self.opcode == SUB or self.opcode == MULT or self.opcode == LSHIFT or self.opcode == RSHIFT):
            print(f"{wordArr[self.opcode]} r{self.vr1}, r{self.vr2} => r{self.vr3}")
        elif (self.opcode == OUTPUT):
            print(f"{wordArr[self.opcode]} {self.vr1}")
        else:
            print(f"{wordArr[self.opcode]}")
        
def buildIR(filename):
    scanner = Scanner(filename)
    scanner.readLine()
    ir = parseLine(scanner)
    opcount = 0
    is_error = False
    head = IRNode(-1)
    
    while not scanner.getEOF():
        if ir.getOpcode() != ERROR:
            head.prev.insertAfter(ir)
            opcount += 1
        else:
            is_error = True
        ir = parseLine(scanner)
        
    # if is_error == True:
    #     print("Due to syntax errors, run terminates.")
    # else:
    #     node = head
    #     while (node.next != head):
    #         print(node.next)
    #         node = node.next
    return (head, scanner.maxreg, opcount)
            
def parseLine(scanner):
    word = scanner.readWord()
    
    while word[0] == EOL:
        word = scanner.readWord()
        
    node = IRNode(scanner.getLine())
    
    if word[0] == MEMOP:
        node.opcode = word[1]
        word = scanner.readWord()
        if word[0] == REGISTER:
            node.sr1 = word[1]
            word = scanner.readWord()
            if word[0] == INTO:
                word = scanner.readWord()
                if word[0] == REGISTER:
                    if node.opcode == STORE:
                        node.sr2 = word[1]
                    else:
                        node.sr3 = word[1]
                    word = scanner.readWord()
                    if word[0] == EOL:
                        return node
                    else:
                        print("ERROR " + str(node.linenum) + ": Extra words in " + scanner.wordArr[node.opcode] + " operation")
                        node.opcode = ERROR
                        errorFlag = True
                        return node
                else:
                    print("ERROR " + str(node.linenum) + ": Missing second source register in " + scanner.wordArr[node.opcode])
                    node.opcode = ERROR
                    errorFlag = True
                    return node
            else:
                print("ERROR " + str(node.linenum) + ":  Missing '=>' in " + scanner.wordArr[node.opcode])
                node.opcode = ERROR
                errorFlag = True
                return node
        else:
            print("ERROR " + str(node.linenum) + ": missing first source register in " + scanner.wordArr[node.opcode])
            node.opcode = ERROR
            errorFlag = True
            return node
    elif word[0] == LOADI:
        node.opcode = word[1]
        word = scanner.readWord()
        if word[0] == CONSTANT:
            node.sr1 = word[1]
            word = scanner.readWord()
            if word[0] == INTO:
                word = scanner.readWord()
                if word[0] == REGISTER:
                    node.sr3 = word[1]
                    word = scanner.readWord()
                    if word[0] == EOL:
                        return (node)
                    else:
                        print("ERROR " + str(node.linenum) + ": Extra words in " + scanner.wordArr[node.opcode] + " operation")
                        node.opcode = ERROR
                        errorFlag = True
                        return node
                else:
                    print("ERROR " + str(node.linenum) + ": Missing second source register in " + scanner.wordArr[node.opcode])
                    node.opcode = ERROR
                    errorFlag = True
                    return node
            else:
                print("ERROR " + str(node.linenum) + ": Missing '=>' in " + scanner.wordArr[node.opcode])
                node.opcode = ERROR
                errorFlag = True
                return node
        else:
            print("ERROR " + str(node.linenum) + ": missing first constant in " + scanner.wordArr[node.opcode])
            node.opcode = ERROR
            errorFlag = True
            return node
    elif word[0] == ARITHOP:
        node.opcode = word[1]
        word = scanner.readWord()
        if word[0] == REGISTER:
            node.sr1 = word[1]
            word = scanner.readWord()
            if word[0] == COMMA:
                word = scanner.readWord()
                if word[0] == REGISTER:
                    node.sr2 = word[1]
                    word = scanner.readWord()
                    if word[0] == INTO:
                        word = scanner.readWord()
                        if word[0] == REGISTER:
                            node.sr3 = word[1]
                            word = scanner.readWord()
                            if word[0] == EOL:
                                return (node)
                            else:
                                print("ERROR " + str(node.linenum) + ": Extra words in " + scanner.wordArr[node.opcode] + " operation")
                                node.opcode = ERROR
                                errorFlag = True
                                return node
                        else:
                            print("ERROR " + str(node.linenum) + ": Missing third source register in +" + scanner.wordArr[node.opcode])
                            node.opcode = ERROR
                            errorFlag = True
                            return node
                    else:
                        print("ERROR " + str(node.linenum) + ": Missing '=>' in " + scanner.wordArr[node.opcode])
                        node.opcode = ERROR
                        errorFlag = True
                        return node
                else:
                    print("ERROR " + str(node.linenum) + ": Missing second source register in" + scanner.wordArr[node.opcode])
                    node.opcode = ERROR
                    errorFlag = True
                    return node
            else:
                print("ERROR " + str(node.linenum) + ": Missing comma in " + scanner.wordArr[node.opcode])
                node.opcode = ERROR
                errorFlag = True
                return node
        else:
            print("ERROR " + str(node.linenum) + ": Missing first source register in " + scanner.wordArr[node.opcode])
            node.opcode = ERROR
            errorFlag = True
            return node
    elif word[0] == OUTPUT:
        node.opcode = word[1]
        word = scanner.readWord()
        if word[0] == CONSTANT:
            node.sr1 = word[1]
            word = scanner.readWord()
            if word[0] == EOL:
                return node
            else:
                print("ERROR " + str(node.linenum) + ": Extra words in " + scanner.wordArr[node.opcode] + " operation")
                node.opcode = ERROR
                errorFlag = True
                return node
        else:
            print("ERROR " + str(node.linenum) + ": Missing constant in " + scanner.wordArr[node.opcode])
            node.opcode = ERROR
            errorFlag = True
            return node
    elif word[0] == NOP:
        node.opcode = word[1]
        word = scanner.readWord()
        if word[0] == EOL:
            return (node)
        else:
            print("ERROR " + str(node.linenum) + ": Extra words in " + scanner.wordArr[node.opcode] + " operation")
            node.opcode = ERROR
            errorFlag = True
            return node
    elif word[0] == EOF:
        node.opcode = EOF
        return node
    elif word[0] == ERROR:
        # We don't print errors twice
        node.opcode = ERROR
        errorFlag = True
        return node
    else:
        print("ERROR  " + str(node.linenum) + ": Invalid starting part of speech, " + scanner.categoryArr[word[0]])
        node.opcode = ERROR
        errorFlag = True
        return node    

def main ():
    argslst = argv
    filename = argslst[-1]
    
    # if os.path.exists(filename) == False:
    #     print("ERROR: file does not exists or filepath is missing")
    if "-h" in argslst:
        h_flag()
    elif "-x" in argslst:
        x_flag(filename)
    else:
        validk = True
        try:
            int(argslst[1])
            validk = True
        except ValueError:
            validk = False
        if validk:
            k_flag(argslst[1])
        else:
            print("Invalid flags, please try again")        
        
def h_flag():
    print("Valid Command Line Arguments:")
    print("\n")
    print("Filename: the filename can either be a relative or an absolute path")
    print("-h: produces a list of valid command-line arguments and includes descriptions of all command-line arguments")
    print("-x <name>: 412alloc will scan and parse the input block, and then will perform renaming on the code in the input block, and print the results to the standard output stream")
    print("k <name>: this is a paramater that represents the number of registers available to the allocator. This value should be between 3 and 64 (inclusive).")

def x_flag(filename):
    
    (head, maxreg, blockLength) = buildIR(filename)
    
    vrName = 0
    sr_to_vr = [INVALID for i in range(maxreg + 1)]
    last_use = [float("inf") for i in range(maxreg + 1)]
   
    idx = blockLength
    curr = head.prev
    while curr != head:
      
        if curr.opcode == NOP:
            curr.next.prev = curr.prev
            curr.prev.next = curr.next
            curr = curr.prev
            continue
        if curr.sr3 != None:
            if sr_to_vr[curr.sr3] == INVALID:
                sr_to_vr[curr.sr3] = vrName
                vrName += 1
            curr.vr3 = sr_to_vr[curr.sr3]
            curr.nu3 = sr_to_vr[curr.sr3]
            sr_to_vr[curr.sr3] = INVALID
            last_use[curr.sr3] = float("inf")
        
        if curr.sr2 != None:
            if sr_to_vr[curr.sr2] == INVALID:
                sr_to_vr[curr.sr2] = vrName
                vrName += 1
            curr.vr2 = sr_to_vr[curr.sr2]
            curr.nu2 = last_use[curr.sr2]
        if curr.sr1 != None and curr.opcode != OUTPUT and curr.opcode != LOADI:
            if sr_to_vr[curr.sr1] == INVALID:
                sr_to_vr[curr.sr1] = vrName
                vrName += 1
            curr.vr1 = sr_to_vr[curr.sr1]
            curr.nu1 = last_use[curr.sr1]
        if (curr.sr1 != None) and (curr.opcode == OUTPUT or curr.opcode == LOADI):
            curr.vr1 = curr.sr1
        
        
       
        if curr.sr1 != None and curr.opcode != OUTPUT and curr.opcode != LOADI:
            last_use[curr.sr1] = idx
        if curr.sr2 != None:
            last_use[curr.sr2] = idx
        idx -= 1
        curr = curr.prev
        
    node = head 
    while (node.next != head):
        node.next.printVR()
        node = node.next
    
def k_flag(input):
    print(type(input))
    
if __name__ == "__main__":
    main()
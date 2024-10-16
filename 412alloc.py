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
beeboop = 32768
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
vrName1 = 0
k = 0
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
            k_flag(argslst[1], filename)
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

    return head, vrName
    # while (node.next != head):
    #     node.next.printVR()
    #     node = node.next
        



def k_flag(k, filename):
    if int(k) < 2 or int(k) > 65:
        print("K is out of expected range, please try again with an input integer between 3 and 64 (inclusive)")
        return None
    head, vrName = x_flag(filename)
    k_int = int(k)
    vr_to_pr = [INVALID for i in range(vrName)]
    pr_to_vr = [INVALID for i in range(k_int)]
    vr_to_spill = [0 for i in range(vrName)]
    pr_nu = [INVALID for i in range(k_int)]
    marked = INVALID
    available_prs = list(range(k_int-2, -1, -1))
    print("AVAIL PRS" + str(type(available_prs)))
    curr = head
    spill_pr = k_int-1  
    
    def getPR(prs, vr, nu, marked):
        if prs:
            x = prs.pop()
            vr_to_pr[vr] = x
            pr_to_vr[x] = vr
            pr_nu[x] = nu
            return x
        else:
            max_nu = 0
            max_idx = 0
            for i in range(len(pr_nu)):
                if pr_nu[i] != None:
                    if max_nu <= pr_nu[i] and marked == i:
                        continue
                    else:
                        max_nu = pr_nu[i]
                        max_idx = i
            x = max_idx
            spill(x)
            vr_to_pr[vr] = x
            pr_to_vr[x] = vr
            pr_nu[x] = nu
            return x
        
    def spill(i):
        global beeboop
        if (vr_to_spill[pr_to_vr[i]] == 0):
            vr_to_spill[pr_to_vr[i]] = beeboop
            beeboop += 4
            print(f"loadI {vr_to_spill[pr_to_vr[i]]} => r{spill_pr}")
            print(f"store r{i} => {spill_pr}")
        vr_to_pr[pr_to_vr[i]] = INVALID
        pr_to_vr[i] = INVALID
                
    def restore(vr, pr, spill):
        print(f"loadI {vr_to_spill[vr]} => r{spill_pr}")
        print(f"load r{spill_pr} => {pr}")
        
    def free_pr(pr, prs):
        prs.append(pr)
        vr_to_pr[pr_to_vr[pr]] = INVALID
        pr_to_vr[pr] = INVALID
        pr_nu[pr] = INVALID
    
    while curr.next != head:
        # handling O1
        if curr.vr1 != None:
            #print("breaking value is " + str(curr.vr1))
            if vr_to_pr[curr.vr1] != INVALID:
                curr.pr1 = vr_to_pr[curr.vr1]
            else:
                x = getPR(available_prs, curr.vr1, curr.nu1, marked)
                restore(curr.vr1, x, spill_pr)
                curr.pr1 = vr_to_pr[curr.vr1]
        if curr.nu1 == float('inf'):
            free_pr(curr.pr1, available_prs)   
        # handling O2
        if curr.vr2 != None:
            if vr_to_pr[curr.vr2] != INVALID:
                curr.pr2 = vr_to_pr[curr.vr2]
            else:
                x = getPR(available_prs, curr.vr2, curr.nu2, marked)
                restore(curr.vr2, x, spill_pr)
                curr.pr2 = x
        if curr.nu2 == float('inf'):
            free_pr(curr.pr2, available_prs)  
        # handling O3
        if curr.vr3 != None:
            x = getPR(available_prs, curr.vr1, curr.nu1, marked)
            curr.pr3 = x
        curr = curr.next
        
    #node2 = head
    # print("your coded did not break")
    # while node2.next != head:
    #     node2.next.printVR()
    #     node2 = node2.next
            
    
if __name__ == "__main__":
    main()
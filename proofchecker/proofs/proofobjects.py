# from proofchecker.proofs.proofchecker import verify_proof #CANNOT USE THIS SINCE IT DEPENDS ON THIS CLASS

class ProofLineObj:

    def __init__(self, line_no=None, expression=None, rule=None): #really rule should be type ProofRule, but keeping string for now until fully refactored
        #similarly, expression should type ProofExpression (an nary tree with methods) but keeping string for now.
        self.line_no = line_no
        self.expression = expression
        self.rule = rule
    
    def __str__(self):
        return ('Line {}: {}, {}'.format(
            self.line_no,
            self.expression,
            self.rule
        ))
    
    def setLineNum(self, myNum):
        self.line_no = myNum
    
    def getLineNum(self):
        return self.line_no

    def setExpr(self, myExpr):
        self.expression = myExpr
    
    def getExpr(self):
        return self.expression

    def setRule(self, myRule):
        self.rule = myRule

    def getRule(self):
        return self.rule  

class ProofObj:
    # added name attribute as part of object (rather than part of gui)
    def __init__(self, rules='tfl_basic', premises=[], conclusion='', lines=[], created_by='', name=""):
        self.rules = rules
        self.premises = premises
        self.conclusion = conclusion
        self.lines = lines
        self.created_by = created_by
        self.name = name
    
    def __str__(self): #BUG: this could potentially be a problem if old version called this thinking it was getting only lines!
        #result = "Proof: "+self.name+"\n" #added name as a title, but commented out to prevent testing errors based on reading lines
        result=""
        for line in self.lines:
            result += str(line) +'\n'
        return result

    def __iter__(self):
        return (x for x in self.lines)

    def getPremises(self):
        return self.premises

    def getLine(self,n):
        return self.lines[n]

    def setLine(self,n, myLine: ProofLineObj):
        self.lines[n]=myLine

    def getConclusion(self):
        return self.conclusion
    
    def setConclusion(self, myConclusion: ProofLineObj):
        self.conclusion=myConclusion

# making a rule as an extension of a Proof. 
class ProofRule(ProofObj):
    
    def __init__(self, rules='tfl_basic', premises=[], conclusion='', lines=[], created_by='', name=""):
        super().__init__(rules, premises, conclusion, lines, created_by, name)

# takes a proof and list of lines
# returns a ProofResponse err msg if any of the cited lines of the proof are not instances of self.premises, otherwise returns True
    def verifyNewRule(self, myProof: ProofObj, lines=[]):
        ans = ProofResponse(False,"") #default is False, so remember to set to True if everything passes! 
        #TODO: change err msgs to be a LIST rather than single string. for now, just appending onto single string with \n, returning at end (vs old way = on detection)
        
        #check that rule is permitted
        if self.name not in myProof.rules: #TODO: will need to change .rules to a LIST rather than a string label
            ans.err_msg += self.name+" is not in a permitted rule for this proof\n"

        #check that rule has been proved (FIAT is okay)
        result = verify_proof(self) #put back in parser, this does NOT work yet
        if not result.is_valid:
            ans.err_msg += self.name+" proof is not completed\n"  

        numPremises = len(self.premises)
        numCitations = len(lines)
        if numPremises != numCitations: #checking to see if cited the correct amt of lines
            ans.err_msg = self.name+" requires exactly "+str(numPremises)+" citations, but the proof cites "+str(numCitations)

        # check to see that each line is a valid (occurs in accessible part of proof)
        for x in range(numCitations):
            pass # copy this from one of the verify files, such as dubneginto.py, but do an append onto ans      
        
        #this part 
        for x in range(numPremises): 
            pass
            # will need a good way to access tree section of expression from the string version of the line... 
            #if myProof.lines[lines[x]].instanceOf(self.premise[x])
            # continue
            # else:  give err.msg 
        return ans

# takes a proof
    def applyNewRule(self, myProof: ProofObj):
        pass

class ProofResponse:

    def __init__(self, is_valid=False, err_msg=None):
        self.is_valid = is_valid
        self.err_msg = err_msg
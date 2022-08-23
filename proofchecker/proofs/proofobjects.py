# from proofchecker.proofs.proofchecker import verify_proof #CANNOT USE THIS SINCE IT DEPENDS ON THIS CLASS

class ProofLineObj:

    def __init__(self, line_no=None, expression=None, rule=None): #really rule should be type ProofRule, but keeping string for now until fully refactored
        #similarly, expression should type ProofExpression (an nary tree with methods) but keeping string for now. all these attribs are strings!
        self.line_no = line_no
        self.expression = expression
        self.rule = rule
    
    def __str__(self):
        return ('Line {}: {}, {}'.format(
            self.line_no,
            self.expression,
            self.rule
        ))
    
    def strList(self):  #returns a list of strings useful for JSON
        return [self.line_no, self.expression, self.rule]
    
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
        self.ruleList = [] #TODO: for future, this will have to be a list of allowed rules, not a specific string, presently 'fol_derived' etc
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
    
    def numPremises(self):
        count = 0
        for line in self.lines:
            if line.rule=="Premise":
                count+=1
        return count

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

class ProofResponse:

    def __init__(self, is_valid=False, err_msg=None):
        self.is_valid = is_valid
        self.err_msg = err_msg
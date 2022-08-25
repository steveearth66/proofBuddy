from inspect import getlineno
from proofchecker.utils import tflparser, folparser, binarytree #parser needed to create tree, binarytree for Node methods (needed for tree equality)
from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
# from exprMethods import myMakeTree #not sure why this was crashing...?
import json
from typing import List 

rawProof = [['1', 'A', 'Premise'], ['2.1', '¬A', 'Assumption'], ['2.2', '⊥', '¬E 2.1, 1'], ['3', '¬¬A', '¬I 2']]
myLines = [ProofLineObj(x[0],x[1],x[2]) for x in rawProof]
sampProof = ProofObj(rules='tfl_basic', lines=myLines, conclusion = myLines[-1], created_by='Steve', name="¬¬I") 
for x in range(sampProof.numPremises()):
    sampProof.premises.append(myLines[x])

def line2Dict(L:ProofLineObj)->dict:
    return {"lineNum":L.getLineNum(), "expr":L.getExpr(),"rule":L.getRule()}


# creates string of a json representation of a proof (later will save it into a filename)
def jsonProof(myProof: ProofObj): #nothing returned here, it just creates a jsonfile at outfile
    myDict={}
    myDict["name"]=myProof.name # didn't bother with getters since just strings/bools for these
    myDict["created_by"]=myProof.created_by
    myDict["complete"]=myProof.complete
    myDict["rules"]=myProof.rules #didn't bother with a getter since it will be obsoleted by ruleList eventually
    myDict["ruleList"]=myProof.getRuleList()
    myDict["premises"]=[line2Dict(L) for L in myProof.getPremises()]
    myDict["conclusion"]=line2Dict(myProof.getConclusion())
    myDict["lines"]=[line2Dict(L) for L in myProof.lines] #makes a sub dictionary for the lines
    with open(myProof.name.replace(" ","")+".json",'w') as f:
        json.dump({"Proofs":[myDict]} ,f,indent=2) # format for json files is a dictionary with one item containing a list of dictionaries
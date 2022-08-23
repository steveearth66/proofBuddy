from inspect import getlineno
from proofchecker.utils import tflparser, folparser, binarytree #parser needed to create tree, binarytree for Node methods (needed for tree equality)
from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from exprMethods import myMakeTree
import json
from typing import List 

rawProof = [['1', 'A', 'Premise'], ['2.1', '¬A', 'Assumption'], ['2.2', '⊥', '¬E 2.1, 1'], ['3', '¬¬A', '¬I 2']]
myLines = [ProofLineObj(x[0],x[1],x[2]) for x in rawProof]
sampProof = ProofObj(rules='tfl_basic', lines=myLines, conclusion = myLines[-1], created_by='Steve', name="¬¬I") 
for x in range(sampProof.numPremises()):
    sampProof.premises.append(myLines[x])

def dictLines(myProof: ProofObj)->List[dict]:
    return [{"lineNum":L.getLineNum(), "expr":LgetExpr(),"rule":L.getRule()} for L in myProof.lines]

# creates string of a json representation of a proof (later will save it into a filename)
def jsonProof(myProof: ProofObj)->str:
    return ""
    
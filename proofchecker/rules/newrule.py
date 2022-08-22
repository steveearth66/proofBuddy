from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.exprMethods import instanceOf
from proofchecker.proofs.proofutils import clean_rule, get_lines, verify_line_citation, make_tree, get_expressions, get_line_nos
from proofchecker.utils.binarytree import Node
# from proofchecker.proofs.proofchecker import verify_proof #CIRCULAR = verifying a rule requires verifying a proof but verifying a proof must verify rules
from proofchecker.utils import tflparser
from .rule import Rule

 # in next version, this will look for a file in the student or teacher directory named "new rule" (or with the given name),
 # but instead of loading it from the database and/or a parsed JSON file, for this version we will hardcode in the rule
 # note that due to the current non-recursive implementation of verify_proof (which depends on verify_rule), we must assume this proof is valid
rawProof = [['1', 'A', 'Premise'], ['2.1', '¬A', 'Assumption'], ['2.2', '⊥', '¬E 2.1, 1'], ['3', '¬¬A', '¬I 2']]
myLines = [ProofLineObj(x[0],x[1],x[2]) for x in rawProof]
myProof = ProofObj(rules='tfl_basic', lines=myLines, conclusion = myLines[-1], created_by='Steve', name="New Rule") #will have to read in permitted rules list
for x in range(myProof.numPremises()):
    myProof.premises.append(myLines[x]) #just needed since we are hard-coding this. normally this would be read from file

class NewRule(Rule):

    name = "New Rule" # this would be the name of the proof
    symbols = "NR"    # most likely a name of the proof without spaces? 

    def test():  #just for testing
        global myProof
        return myProof.numPremises()

    def verify(self, current_line: ProofLineObj, proof: ProofObj, parser):
        global myProof # in future version, this will be read-in as the appropriate new rule proof

        """
        Verify proper implementation of the new rule
        (assumes it has read in a name of "new rule") 
        """

        rule = clean_rule(current_line.rule)
        response = ProofResponse() #default .isvalid=False

        # testing print(current_line.line_no, current_line.expression,current_line.rule, response.err_msg, response.is_valid)   
        #cannot do: result = verify_proof(proof, tflparser.parser) because of dependency issues

        


        # Attempt to find line m
        try:
            target_line_nos = get_line_nos(rule) #this gets a list of strings of the cited lines for the rule
            n, m  = len(target_line_nos), myProof.numPremises()
            if n != m:
                response.err_msg = "Steve says Error on line {}: {} requires {} citation(s), but you provided {}"\
                        .format(str(current_line.line_no), myProof.name, str(m), str(n))
                return response
            target_lines = get_lines(rule, proof) #this gets their corresponding lineObjects

            # from this point on, we know # premises in myProof.premises = # citations in target_lines

            # Verify that line citations are valid
            for line_no in target_line_nos:
                result = verify_line_citation(current_line.line_no, line_no)
                if result.is_valid == False:
                    return result

            # Search for line m in the proof
            try:
                expressions = get_expressions(target_lines) # gets list of expressions of target lines           
                trees_cited = [make_tree(x, parser) for x in expressions] # gets list of trees of those expressions, needed for instanceOf
                trees_orig = [make_tree(x,parser) for x in myProof.premises] # gets list of trees of representing premises of new rule
                env = {} # initializing the environment of checking instances
                for i in range(n): # this is the number of premises/citations (already verified to be equal) to check pattern matching of each
                    result = instanceOf(trees_orig[i], trees_cited[i], env)
                    if result[0]: 
                        env = result[1] #updating the environment between premises
                    else:
                        response.err_msg = "Steve says Error on line {}: citation of line {} does not match premise #{} for rule {}"\
                        .format(str(current_line.line_no), target_line_nos[i], str(n+1), myProof.name)
                        return response

                result = instanceOf(make_tree(myProof.conclusion, parser), make_tree(current_line.expression, parser), env) # checking application of rule
                if result[0]: 
                    response.is_valid = True 
                else:
                    response.err_msg = "Steve says Error on line {}: this expression does not match conclusion for rule {}"\
                    .format(str(current_line.line_no), myProof.name)
                return response
                
                # TODO: still need to check if new rule is valid, AND if new rule is permitted in current proof, and if newrules.rules <= proof.rules

                              
                tree_new = make_tree(current_line.expression, parser)

                if (tree_new.value!='¬'):
                    response.err_msg = "Steve says Error on line {}: The root operand should be ¬ when applying ¬¬I (currently the root operand is {})"\
                        .format(str(current_line.line_no), str(tree_new.value))
                    return response
                
                if (tree_new.right.value!='¬'):
                    response.err_msg = "Steve says Error on line {}: The second operand should be ¬ when applying ¬¬I (currently the second operand is {})"\
                        .format(str(target_lines[0].line_no), str(tree_new.right.value))
                    return response

                if (tree_orig != tree_new.right.right):
                    response.err_msg ="Steve says Error on line {}: The double negated expressions on line {} does not match the expression on line {}"\
                        .format(str(current_line.line_no), str(target_lines[0].line_no))
                    return response
                
                response.is_valid = True  # old bug = i forgot to include this part originally to show it was okay!
                return response

            except:
                response.err_msg = "Steve says Error on line {}: Line numbers are not specified correctly.  Double Negation Introduction: ¬¬I m"\
                    .format(str(current_line.line_no))
                return response 

        except:
            response.err_msg = "Steve says Error on line {}: Rule not formatted properly.  Double Negation Introduction: ¬¬I m"\
                .format(str(current_line.line_no))
            return response
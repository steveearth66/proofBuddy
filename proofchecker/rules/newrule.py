from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import clean_rule, get_lines, verify_line_citation, make_tree, get_expressions, get_line_nos
from proofchecker.utils.binarytree import Node
# from proofchecker.proofs.proofchecker import verify_proof #CIRCULAR = verifying a rule requires verifying a proof but verifying a proof must verify rules
from proofchecker.utils import tflparser
from .rule import Rule

class NewRule(Rule):

    name = "New Rule" # this would be the name of the proof
    symbols = "NR"    # most likely a name of the proof without spaces? 

 # in next version, this will look for a file in the student or teacher directory named "new rule" (or with the given name),
 # but instead of loading it from the database and/or a parsed JSON file, for this version we will hardcode in the rule:
    rawProof = [['1', 'A', 'Premise'], ['2.1', '¬A', 'Assumption'], ['2.2', '⊥', '¬E 2.1, 1'], ['3', '¬¬A', '¬I 2']]
    myLines = [ProofLineObj(x[0],x[1],x[2]) for x in rawProof]
    myProof = ProofObj('tfl_basic', lines=myLines, created_by='Steve', name="New Rule") #purely for testing!

    def verify(self, current_line: ProofLineObj, proof: ProofObj, parser):
        """
        Verify proper implementation of the new rule
        (assumes it has read in a name of "new rule") 
        """

        rule = clean_rule(current_line.rule)
        response = ProofResponse()
        # testing print(current_line.line_no, current_line.expression,current_line.rule, response.err_msg, response.is_valid)
        
       

        #cannot do: result = verify_proof(proof, tflparser.parser) because of dependency issues

        # Attempt to find line m
        try:
            target_line_nos = get_line_nos(rule)
            target_lines = get_lines(rule, proof)

            # Verify that line citations are valid
            for line_no in target_line_nos:
                result = verify_line_citation(current_line.line_no, line_no)
                if result.is_valid == False:
                    return result

            # Search for line m in the proof
            try:
                expressions = get_expressions(target_lines)
                
                tree_orig = make_tree(expressions[0], parser)
                               #ugh, trees aren't constructed from trees, they're constructed from Strings!
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
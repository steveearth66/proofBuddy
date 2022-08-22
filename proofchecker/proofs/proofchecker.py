from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import fix_rule_whitespace_issues, make_tree, is_conclusion, depth, clean_rule
from proofchecker.rules.rulechecker import RuleChecker
from proofchecker.utils.binarytree import tree2Str #only used for testing
from proofchecker.utils.constants import Constants
from proofchecker.utils.tfllexer import IllegalCharacterError
from proofchecker.proofs.exprMethods import myMakeTree, instanceOf
from proofchecker.rules.newrule import NewRule #purely for testing

def verify_proof(proof: ProofObj, parser):
    """
    Verify if a proof is valid, line by line.  
    Returns a ProofResponse, which contains an error message if invalid
    """
    response = ProofResponse()
    ''' below is a test of instanceOf, seems to work!
    res = instanceOf(myMakeTree("A∧(A∨B)",0),myMakeTree("(B→C)∧((B→C)∨A)",0) , {}) # the ,0 of maketree indicates it is tfl vs fol
    if res[0]:
        for x in res[1].keys():
            print(x," replaced by ",res[1][x])
    else:
        print("no match")'''

    if len(proof.lines) == 0:
        response.err_msg = "Cannot validate a proof with no lines"
        return response

    for line in proof.lines:

        # Verify the line has a line number
        if not line.line_no:
            response.err_msg = "One or more lines is missing a line number"
            return response

        # Verify the line has an expression
        if (not line.expression) or (line.expression == ''):
            response.err_msg = "No expression on line {}"\
                .format(str(line.line_no))
            return response

        # Verify the expression is valid
        try:
            make_tree(line.expression, parser)
        except IllegalCharacterError as char_err:
            response.err_msg = "{} on line {}"\
                .format(char_err.message, str(line.line_no))
            return response 
        except:
            response.err_msg = 'Syntax error on line {}.  Expression "{}" does not conform to ruleset "{}"'\
                .format(str(line.line_no), line.expression, Constants.RULES_CHOICES.get(proof.rules))
            return response

        # Verify the rule is valid
        response = verify_rule(line, proof, parser) #BUG = this is returning None
        if not response.is_valid:
            return response

### adding prints here
        #print(line.line_no, tree2Str(make_tree(line.expression, parser)))

    last_line = proof.lines[len(proof.lines)-1]
    conclusion = is_conclusion(last_line, proof, parser)
    response.is_valid = True

    # If the last line is the desired conclusion, it is a full and complete proof
    if conclusion:
        if (last_line.rule.casefold() == 'assumption') or (last_line.rule.casefold() == 'assumpt'):
            response.err_msg = "Proof cannot be concluded with an assumption"
            return response            
        elif depth(last_line.line_no) > 1:
            response.err_msg = "Proof cannot be concluded within a subproof"
            return response
        else:
            response.is_valid = True
            return response

    # If not, the proof is incomplete
    else:
        response.is_valid = True
        response.err_msg = "All lines are valid, but the proof is incomplete"
        return response


def verify_rule(current_line: ProofLineObj, proof: ProofObj, parser):
    """
    Determines what rule is being applied, then calls the appropriate
    function to verify the rule is applied correctly
    """
    rule_str = clean_rule(current_line.rule)
    fixed_rule = fix_rule_whitespace_issues(rule_str)
    rule_symbols = fixed_rule.split()[0]
    rule_checker = RuleChecker()
    rule = rule_checker.get_rule(rule_symbols, proof)

    if rule == None:
        response = ProofResponse()
        response.err_msg = 'Rule "{}" on line {} not found in ruleset "{}"'\
            .format(rule_symbols, str(current_line.line_no), Constants.RULES_CHOICES.get(proof.rules))
        return response     
    else:
        return rule.verify(current_line, proof, parser)
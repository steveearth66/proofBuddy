from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import clean_rule, get_lines, verify_line_citation, make_tree, get_expressions
from .rule import Rule

class BiconditionalElim(Rule):

    name = "Biconditional Elimination"
    symbols = "↔E"


    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        """
        Verify the rule ↔E m, n
        (Biconditional Elimination)
        """
        rule = clean_rule(current_line.rule)
        response = ProofResponse()

        # Attempt to find lines (m, n) 
        try:
            target_lines = get_lines(rule, proof)

            # Verify that the line citations are valid
            for line in target_lines:
                result = verify_line_citation(current_line, line)
                if result.is_valid == False:
                    return result

            # Search for lines (m, n) in the proof
            try:
                expressions = get_expressions(target_lines)
                
                # Join the two expressions in a tree
                root_m = make_tree(expressions[0])
                root_n = make_tree(expressions[1])
                root_current = make_tree(current_line.expression)

                # Compare the trees
                if (root_n == root_m.left) or (root_n == root_m.right):
                    if (root_current == root_m.left) or (root_current == root_m.right):
                        if (root_m.left == root_m.right) or (root_n != root_current):
                            response.is_valid = True
                            return response
                        else:
                            response.err_msg = "The expressions on lines {} and {} do not represent both the left and right side of the expression on line {}"\
                                .format(str(target_lines[1].line_no), str(current_line.line_no), str(target_lines[0].line_no))
                            return response
                    else:
                        response.err_msg = "The expression on line {} does not represent the left or right side of the expression on line {}"\
                            .format(str(current_line.line_no), str(target_lines[0].line_no))
                        return response
                else:
                    response.err_msg = "The expression on line {} does not represent the left or right side of the expression on line {}"\
                        .format(str(target_lines[1].line_no), str(target_lines[0].line_no))
                    return response
            
            except:
                response.err_msg = "Line numbers are not specified correctly.  Biconditional Elimination: ↔E m, n"
                return response

        except:
            response.err_msg = "Rule is not formatted properly.  Biconditional Elimination: ↔E m, n"
            return response
from proofchecker.proof import ProofObj, ProofLineObj, ProofResponse, Node, clean_rule, get_expressions, get_lines, make_tree, verify_line_citation
from .rule import Rule

class ConjunctionIntro(Rule):

    name = 'Conjunction Introduction'
    symbols = '∧I'

    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        """
        Verify proper implementation of the rule ∧I m, n
        (Conjunction Introduction)
        """
        rule = clean_rule(current_line.rule)
        response = ProofResponse()

        # Attempt to find lines (m, n) 
        try:
            target_lines = get_lines(rule, proof)

            for line in target_lines:
                result = verify_line_citation(current_line, line)
                if result.is_valid == False:
                    return result

            # Search for lines (m, n) in the proof
            try:
                expressions = get_expressions(target_lines)
                
                # Join the two expressions in a tree
                root_m_and_n = Node('∧')
                root_m_and_n.left = make_tree(expressions[0])
                root_m_and_n.right = make_tree(expressions[1])

                root_n_and_m = Node('∧')
                root_n_and_m.left = make_tree(expressions[1])
                root_n_and_m.right = make_tree(expressions[0])

                # Create a tree from the current expression
                root_current = make_tree(current_line.expression)

                # Compare the trees
                if (root_current == root_m_and_n) or (root_current == root_n_and_m):
                    response.is_valid = True
                    return response
                else:
                    response.err_msg = "The conjunction of lines {} and {} does not equal line {}"\
                        .format(str(target_lines[0].line_no), str(target_lines[1].line_no), str(current_line.line_no))
                    return response
            
            except:
                response.err_msg = "Line numbers are not specified correctly.  Conjunction Introduction: ∧I m, n"
                return response

        except:
            response.err_msg = "Rule is not formatted properly.  Conjunction Introduction: ∧I m, n"
            return response
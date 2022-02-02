from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import clean_rule, get_line_nos, verify_line_citation, \
    make_tree, get_line_with_line_no, get_lines_in_subproof, verify_subproof_citation, get_expressions
from .rule import Rule

class DisjunctionElim(Rule):

    name = "Disjunction Elimination"
    symbols = "∨E"

    def verify(self, current_line: ProofLineObj, proof: ProofObj):
        """
        Verify proper implementation of the rule ∨E m, i, j
        (Disjunction Elimination)
        """
        rule = clean_rule(current_line.rule)
        response = ProofResponse()

        # Attempt to find lines (m, i, j)
        try:
            target_line_nos = get_line_nos(rule)
            line_m = get_line_with_line_no(target_line_nos[0], proof)
            lines_i = get_lines_in_subproof(target_line_nos[1], proof)
            lines_j = get_lines_in_subproof(target_line_nos[2], proof)
            target_lines = [line_m, lines_i[0], lines_i[1], lines_j[0], lines_j[1]]

            # Verify that line m citation is valid
            line_m_citation = verify_line_citation(current_line, target_lines[0])
            if line_m_citation.is_valid == False:
                return line_m_citation

            # Verify that subproof citations are valid
            for line in target_lines[1:len(target_lines)]:
                result = verify_subproof_citation(current_line, line)
                if result.is_valid == False:
                    return result

            # Search for lines m, i-j, k-l in the proof
            try:
                expressions = get_expressions(target_lines)
            
                # Create trees for expressions on lines m, i, j, k, and l
                root_m = make_tree(expressions[0])
                root_i = make_tree(expressions[1])
                root_j = make_tree(expressions[2])
                root_k = make_tree(expressions[3])
                root_l = make_tree(expressions[4])
                root_current = make_tree(current_line.expression)

                # Verify lines i and k represent separate sides of expression m
                if (root_i != root_k):
                    if (root_i == root_m.left) or (root_i == root_m.right):
                        if (root_k == root_m.left) or (root_k == root_m.right):
                            # Verify that j, l, and current_line expression are equivalent
                            if (root_j == root_l) and (root_l == root_current):
                                response.is_valid = True
                                return response
                            else:
                                response.err_msg = "The expressions on lines {}, {} and {} are not equivalent"\
                                    .format(str(target_lines[2].line_no),str(target_lines[4].line_no),str(current_line.line_no))
                                return response
                        else:
                            response.err_msg = "The expression on line {} is not part of the disjunction on line {}"\
                                .format(str(target_lines[3].line_no),str(target_lines[0].line_no))
                            return response
                    else:
                        response.err_msg = "The expression on line {} is not part of the disjunction on line {}"\
                            .format(str(target_lines[1].line_no),str(target_lines[0].line_no))
                        return response          
                else:
                    response.err_msg = "The expressions on lines {} and {} should be different"\
                        .format(str(target_lines[1].line_no),str(target_lines[3].line_no))
                    return response    
            except:
                response.err_msg = "Line numbers are not specified correctly.  Disjunction Elimination: ∨E m, i, j"
                return response        
        except:
            response.err_msg = "Rule not formatted properly.  Disjunction Elimination: ∨E m, i, j"
            return response

from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import clean_rule, get_line, verify_line_citation, make_tree, verify_same_structure_FOL, \
    verify_var_replaces_some_name
from proofchecker.utils.binarytree import tree2Str
from .rule import Rule

class UniversalElim(Rule):

    name = "Universal Elimination"
    symbols = "∀E"

    def verify(self, current_line: ProofLineObj, proof: ProofObj, parser):
        """
        Verify proper implementation of the rule ∀E m
        (Universal Elimination)
        """
        rule = clean_rule(current_line.rule)
        response = ProofResponse()

        # Attempt to find line m
        try:
            target_line = get_line(rule, proof)

            # Verify if line citation is valid
            result = verify_line_citation(current_line.line_no, target_line.line_no)
            if result.is_valid == False:
                return result

            try: 
                root_m = make_tree(target_line.expression, parser)
                current = make_tree(current_line.expression, parser)

                # Verify root operand of line m is ∀
                if (root_m.value[0] != '∀'):
                    response.err_msg = "Error on line {}: The root operand of line {} should be the universal quantifier (∀)"\
                        .format(str(current_line.line_no), str(target_line.line_no))
                    return response
                
                # Verify that root_m.right and current have same stucture
                result = verify_same_structure_FOL(root_m.right, current, target_line.line_no, current_line.line_no)
                if result.is_valid == False:
                    result.err_msg = 'Error on line {}: '.format(current_line.line_no) + result.err_msg
                    return result

                # Verify that all instances of the bound variable in root_m.right
                # are replaced by the same name in current
                var = root_m.value[1]

                '''# let's try doing string replacement first: this does NOT work due to  ∀x∈V Px ∧ (∀x∈V Qx), so must use tree structure to maintain scope!!
                expr_no_quant = tree2Str(root_m.right)
                new_expr = tree2Str(current)
                print("old = ", expr_no_quant,"\nnew = ",new_expr)
                ind=expr_no_quant.find(var)
                if ind>=0:
                    all_sub = expr_no_quant.replace(var,new_expr[ind] )
                    if all_sub!=new_expr: #in reality, there might be other issues such as parens to check out. really need tree struct
                        response.err_msg = "Steve says improper instantiation"
                        return response'''

                #added list of bindings to represent environment
                result = verify_var_replaces_some_name(root_m.right, current, var, target_line.line_no, current_line.line_no, [])
                if result.is_valid == False:
                    result.err_msg = 'Error on line {}: '.format(current_line.line_no) + result.err_msg
                    return result

                response.is_valid = True
                return response

            except:
                response.err_msg = "Error on line {}: Line numbers are not specified correctly.  Universal Elimination: ∀E m"\
                    .format(str(current_line.line_no))
                return response

        except:
            response.err_msg = "Error on line {}: Rule not formatted properly.  Universal Elimination: ∀E m"\
                .format(str(current_line.line_no))
            return response
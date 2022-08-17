from proofchecker.utils import tflparser #parser needed to create tree

# new global variable necessary to distinguish variables in expressions
# uncertain about constants so be sure to test those. what about parens?
BINSYMBOLS = ['∧', '∨', '→', '↔', '∀', '∃'] # not sure how quantifiers are stored in tree. possibly as binary. 
UNASYMBOLS = ['¬']
ZERSYMBOLS = ['⊥']  # also need booleans?  t_BOOL=r'((True)|(TRUE)|(False)|(FALSE)|⊥)'
ASSOCS = ['∧', '∨', '↔'] #list of nonunary operations that are associative (and therefore don't require parens in monolithic multiples. e.g A∧B∧C)
SYMBOLS = BINSYMBOLS + UNASYMBOLS + ZERSYMBOLS

# takes general expression and a specific expression and a dictionary of already known vars, and determines 
def instanceOf(genExpr, specificExpr, env):
    parser = tflparser.parser
    lex = parser.lexer
    genTree = parser.parse(genExpr, lexer=lex)
    specTree = parser.parse(specificExpr, lexer=lex) #is it okay to use the same lex?  hopefully yes.
    return 5

def f(x):  #for testing
    return x+1

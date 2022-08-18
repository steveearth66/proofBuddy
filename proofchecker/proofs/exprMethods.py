from proofchecker.utils import tflparser, binarytree #parser needed to create tree, binarytree for Node methods (not needed?)

# new global variable necessary to distinguish variables in expressions
# uncertain about constants so be sure to test those. what about parens?
BINSYMBOLS = ['∧', '∨', '→', '↔', '∀', '∃'] # not sure how quantifiers are stored in tree. possibly as binary. 
UNASYMBOLS = ['¬']
ZERSYMBOLS = ['⊥']  # also need booleans?  t_BOOL=r'((True)|(TRUE)|(False)|(FALSE)|⊥)'
ASSOCS = ['∧', '∨', '↔'] #list of nonunary operations that are associative (and therefore don't require parens in monolithic multiples. e.g A∧B∧C)
SYMBOLS = BINSYMBOLS + UNASYMBOLS + ZERSYMBOLS

# takes general expressiontree and a specific expressiontree and a dictionary of already known vars, and returns [boolean, updated env]

def myMakeTree(expr:str)->binarytree.Node:
    parser = tflparser.parser
    return parser.parse(expr, lexer=parser.lexer)

def instanceOf(genTree:binarytree.Node, specTree:binarytree.Node, env:dict):
    #no longer need below part since it's already in trees, not strings ()
    """parser = tflparser.parser
    lex = parser.lexer
    genTree = parser.parse(genExpr, lexer=lex) #turns this into a binarytree.Node
    specTree = parser.parse(specificExpr, lexer=lex) #is it okay to use the same lex?  hopefully yes.""" 
    if genTree.value=="∧":
        return [True,{1:5}]
    else:
        return [False,{2:6}]
    if genTree.value in UNASYMBOLS: # e.g. ¬(A∧B)
        if specTree.value != genTree.value: #spec isn't a ¬C
            return [False, env]
        return instanceOf()#no need for else due to return
    return

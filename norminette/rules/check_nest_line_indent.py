from rules import Rule
from scope import *

operators = [
    "RIGHT_ASSIGN",
    "LEFT_ASSIGN",
    "ADD_ASSIGN",
    "SUB_ASSIGN",
    "MUL_ASSIGN",
    "DIV_ASSIGN",
    "MOD_ASSIGN",
    "AND_ASSIGN",
    "XOR_ASSIGN",
    "OR_ASSIGN",
    "LESS_OR_EQUAL",
    "GREATER_OR_EQUAL",
    "EQUALS",
    "NOT_EQUAL",
    "ASSIGN",
    "SEMI_COLON",
    "DOT",
    "NOT",
    "MINUS",
    "PLUS",
    "MULT",
    "DIV",
    "MODULO",
    "LESS_THAN",
    "MORE_THAN",
    "PTR",
    "AND",
    "OR",
    "BWISE_XOR",
    "BWISE_OR",
    "BWISE_NOT",
    "BWISE_AND",
    "RIGHT_SHIFT",
    "LEFT_SHIFT",
]
nest_kw = ["RPARENTHESIS", "LPARENTHESIS", "NEWLINE"]

class CheckNestLineIndent(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsControlStatement", "IsExpressionStatement"]

    def find_nest_content(self, context, nest, i):
        expected = context.scope.indent + nest
        while context.peek_token(i) is not None:
            if context.check_token(i, "LPARENTHESIS") is True:
                nest += 1
                i += 1
                i = self.find_nest_content(context, nest, i)
            elif context.check_token(i, "NEWLINE") is True:
                if context.check_token(i - 1, operators):
                    context.new_error("EOL_OPERATOR", context.peek_token(i - 1))
                indent = 0
                i += 1
                while context.check_token(i, "TAB") is True:
                    indent += 1
                    i += 1
                if indent > expected:
                    context.new_error("TOO_MANY_TAB", context.peek_token(0))
                elif indent < expected:
                    context.new_error("TOO_FEW_TAB", context.peek_token(0))
            elif context.check_token(i, "RPARENTHESIS"):
                return i
            i += 1
        return i

    def run(self, context):
        i = 0
        expected = context.scope.indent
        nest = 0
        if context.history[-1] == "IsEmptyLine":
            return False, 0
        while context.check_token(i, ["LPARENTHESIS", "NEWLINE"]) is False:
            i += 1
        if context.check_token(i, "NEWLINE") is True:
            return False, 0
        if context.check_token(i, "LPARENTHESIS") is True:
            nest += 1
            i += 1
            self.find_nest_content(context, nest, i)
        return False, 0
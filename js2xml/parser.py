import ply.yacc
from slimit.parser import Parser
from js2xml.lexer import CustomLexer as Lexer
from js2xml.log import logger

lextab, yacctab = 'lextab', 'yacctab'


class CustomParser(Parser):

    def __init__(self, lex_optimize=True, lextab=lextab,
                 yacc_optimize=True, yacctab=yacctab, yacc_debug=False,
                 logger=logger):
        self.lex_optimize = lex_optimize
        self.lextab = lextab
        self.yacc_optimize = yacc_optimize
        self.yacctab = yacctab
        self.yacc_debug = yacc_debug

        self.lexer = Lexer()
        self.lexer.build(optimize=lex_optimize, lextab=lextab, errorlog=logger)
        self.tokens = self.lexer.tokens

        self.parser = ply.yacc.yacc(
            module=self,
            optimize=yacc_optimize,
            debug=yacc_debug,
            tabmodule=yacctab,
            start='program',
            errorlog=logger)

        self._error_tokens = {}


    def parse(self, text, debug=False):
        result = super(CustomParser, self).parse(text, debug=debug)
        self._error_tokens = {}
        return result

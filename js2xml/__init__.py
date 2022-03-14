import lxml.etree
from calmjs.parse.parsers.es5 import Parser

from .jsonlike import *
from .xmlvisitor import XmlVisitor


__version__ = "0.5.0"

_parser = Parser()
_visitor = XmlVisitor()


def parse(text, encoding="utf8", debug=False):
    if not isinstance(text, str):
        text = text.decode(encoding)
    tree = _parser.parse(text, debug=debug)
    xml = _visitor.visit(tree)
    return xml


def pretty_print(tree):
    return lxml.etree.tostring(tree, pretty_print=True, encoding="unicode")

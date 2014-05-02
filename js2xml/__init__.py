import lxml.etree
from slimit.parser import Parser
from js2xml.xmlvisitor import XmlVisitor

_parser = Parser()
_visitor = XmlVisitor()

def parse(text, debug=False):
    tree = _parser.parse(text, debug=debug)
    xml = _visitor.visit(tree)
    return xml

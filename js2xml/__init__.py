import lxml.etree
from js2xml.parser import CustomParser as Parser
from js2xml.xmlvisitor import XmlVisitor
import js2xml.jsonlike as jsonlike

_parser = Parser()
_visitor = XmlVisitor()

def parse(text, encoding="utf8", debug=False):
    if encoding not in (None, "utf8"):
        text = text.decode(encoding)
    tree = _parser.parse(text if not isinstance(text, unicode) else text.encode("utf8"), debug=debug)
    xml = _visitor.visit(tree)
    return xml


def pretty_print(tree):
    return lxml.etree.tostring(tree, pretty_print=True)

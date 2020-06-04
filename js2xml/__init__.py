from calmjs.parse.parsers.es5 import Parser
import lxml.etree
import six

from .jsonlike import *
from .xmlvisitor import XmlVisitor


__version__ = "0.4.0"

_parser = Parser()
_visitor = XmlVisitor()

def parse(text, encoding="utf8", debug=False):
    if not isinstance(text, six.text_type):
        text = text.decode(encoding)
    tree = _parser.parse(text, debug=debug)
    xml = _visitor.visit(tree)
    return xml


def pretty_print(tree):
    return lxml.etree.tostring(tree, pretty_print=True, encoding='unicode')

import six
import lxml.etree

from .parser import CustomParser as Parser
from .xmlvisitor import XmlVisitor
from .jsonlike import *


__version__ = "0.2.3"

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

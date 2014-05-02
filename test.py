import sys
import lxml.etree
from slimit.parser import Parser
from js2xml.xmlvisitor import XmlVisitor

text = sys.stdin.read()
if not text:
    text = """
     var x = {
        "key1": "value1",
        "key2": "value2",
        "key3": 1,
        "key4": false
    };
    """
print text
parser = Parser()
tree = parser.parse(text, debug=False)

visitor = XmlVisitor()
xml = visitor.visit(tree)
print lxml.etree.tostring(xml, pretty_print=True)

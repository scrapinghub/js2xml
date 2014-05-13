import lxml.etree
#from slimit.parser import Parser
from js2xml.parser import CustomParser as Parser
from js2xml.xmlvisitor import XmlVisitor

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


_jsonlike_elements = """
       self::object
    or self::array
    or self::assign
    or self::left
    or self::right
    or self::operator[.=":"]
    or self::string
    or self::number
    or self::boolean
    """
_jsonlike_xpath = """
    (self::object or self::array)
    and
    not(./descendant::*[not(%(elements)s)])
""" % {"elements": _jsonlike_elements}

_xp_jsonlike = lxml.etree.XPath(_jsonlike_xpath)
_topjsonlike_xpath = """
    .//*[self::object or self::array]
        [not(./descendant::*[not(%(elements)s)])]
        [not(ancestor::*[%(jsonlike)s])]
""" % {"elements": _jsonlike_elements,
       "jsonlike": _jsonlike_xpath}
_xp_findjsonlike = lxml.etree.XPath(_topjsonlike_xpath)


def is_jsonlike(subtree):
    return _xp_jsonlike(subtree)


def findall_jsonlike(tree):
    return _xp_findjsonlike(tree)


def make_dict(tree):
    if tree.tag == 'array':
        return [make_dict(child) for child in tree.iterchildren()]
    elif tree.tag == 'object':
        return dict([make_dict(child) for child in tree.iterchildren()])
    elif tree.tag == 'assign':
        return (make_dict(tree.find('./left/*')), make_dict(tree.find('./right/*')))
    elif tree.tag == 'string':
        return tree.text
    elif tree.tag == 'boolean':
        return tree.text == 'true'
    elif tree.tag == 'number':
        try:
            return int(tree.text)
        except:
            return float(tree.text)
    elif tree.tag == 'undefined':
        return tree.tag


def getall_jsonlike(tree):
    results = _xp_findjsonlike(tree)
    out = []
    if results is not None:
        for r in results:
            out.append(make_dict(r))
    return out

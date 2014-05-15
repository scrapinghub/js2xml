import lxml.etree


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
    elif tree.tag == 'null':
        return None

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
    or self::null
    or self::undefined
    """
_jsonlike_xpath = """
    (self::object or self::array)
    and
    not(./descendant::*[not(%(elements)s)])
""" % {"elements": _jsonlike_elements}

_xp_jsonlike = lxml.etree.XPath(_jsonlike_xpath)

_alljsonlike_xpath = """
    ./descendant-or-self::*[self::object or self::array]
                           [not(./descendant::*[not(%(elements)s)])]
""" % {"elements": _jsonlike_elements}
_xp_alljsonlike = lxml.etree.XPath(_alljsonlike_xpath)


def is_jsonlike(subtree):
    return _xp_jsonlike(subtree)


def findall(tree):
    candidates = _xp_alljsonlike(tree)
    out = []
    if candidates is not None:
        test_set = set(candidates)
        for candidate in candidates:
            # check if ancestors are also candidates ;
            # if so, this is not a top-level JSON-like object
            if (set(candidate.iterancestors()) & test_set):
                continue
            out.append(candidate)
    return out


def getall(tree):
    return [make_dict(obj) for obj in findall(tree)]

import lxml.etree


def make_dict(tree):
    if tree.tag == 'array':
        return [make_dict(child) for child in tree.iterchildren()]
    elif tree.tag == 'object':
        return dict([make_dict(child) for child in tree.iterchildren()])
    elif tree.tag == 'property':
        return (tree.get('name'), make_dict(tree.find('./*')))
    elif tree.tag == 'string':
        return tree.text
    elif tree.tag == 'identifier':
        return tree.get("name")
    elif tree.tag == 'boolean':
        return tree.text == 'true'
    elif tree.tag == 'number':
        try:
            return int(tree.get("value"))
        except:
            return float(tree.get("value"))
    elif tree.tag == 'undefined':
        return tree.tag
    elif tree.tag == 'null':
        return None

_jsonlike_elements = """
       self::object[property or not(node())]
    or self::array
    or self::property[@name]
    or self::identifier[parent::property]
    or self::string
    or self::number
    or self::boolean
    or self::null
    or self::undefined
    """
_jsonlike_xpath = """
    (self::object[property or not(node())] or self::array)
    and
    not(./descendant::*[not(%(elements)s)])
""" % {"elements": _jsonlike_elements}

_xp_jsonlike = lxml.etree.XPath(_jsonlike_xpath)

_alljsonlike_xpath = """
    ./descendant-or-self::*[self::object[property or not(node())] or self::array]
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

_nonjsonlike_xpath = """
    ./descendant-or-self::*[not(%(elements)s)]
""" % {"elements": _jsonlike_elements}

_xp_nonjsonlike = lxml.etree.XPath(_nonjsonlike_xpath)
# to help debugging
def getall_nonjsonlike(subtree):
    return _xp_nonjsonlike(subtree)

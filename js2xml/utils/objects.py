from lxml.etree import XPath


_jsobject = """
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
_jsobject_xpath = """
    (self::object[property or not(node())] or self::array)
    and
    not(./descendant::*[not(%(elements)s)])
""" % {"elements": _jsobject}

_xp_jsobject = XPath(_jsobject_xpath)

_alljsobjects_xpath = """
    ./descendant-or-self::*[self::object[property or not(node())] or self::array]
                           [not(./descendant::*[not(%(elements)s)])]
""" % {"elements": _jsobject}
_xp_alljsobjects = XPath(_alljsobjects_xpath)

_nonjsobjects_xpath = """
    ./descendant-or-self::*[not(%(elements)s)]
""" % {"elements": _jsobject}

_xp_nonjsobjects = XPath(_nonjsobjects_xpath)


def make(tree):
    if tree.tag == 'array':
        return [make(child) for child in tree.iterchildren()]
    elif tree.tag == 'object':
        return dict([make(child) for child in tree.iterchildren()])
    elif tree.tag == 'property':
        return (tree.get('name'), make(tree.find('./*')))
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


def is_object(subtree):
    return _xp_jsobject(subtree)


def findall(tree):
    candidates = _xp_alljsobjects(tree)
    out = []
    if candidates is not None:
        test_set = set(candidates)
        for candidate in candidates:
            # check if ancestors are also candidates ;
            # if so, this is not a top-level object
            if (set(candidate.iterancestors()) & test_set):
                continue
            out.append(candidate)
    return out


def getall(tree):
    return [make(obj) for obj in findall(tree)]


# to help debugging
def getall_nonjsobjects(subtree):
    return _xp_nonjsobjects(subtree)

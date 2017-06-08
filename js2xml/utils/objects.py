from lxml.etree import XPath


# base built-in objects (e.g. not functions definitions within Objects or Arrays)
_elements = [
    'object[property or not(node())]',  # an Object with a property, or an empty Object
    'array',
    'property[@name]',
    'identifier[parent::property]',
    'string',
    'number',
    'boolean',
    'null',
    'undefined',
]

_tagmap = {
    list: ['array'],
    dict: ['object[property or not(node())]'],
    str: ['string'],
    int: ['number'],
    float: ['number'],
    bool: ['boolean'],
    None: ['null', 'undefined'],
}


def one_of_xpath(elements):
    return ' or '.join('self::{}'.format(el) for el in elements)


def is_instance_xpath(types):
    _tags = {m for t in types for m in _tagmap[t]}
    xp = '''
        ({mapped})
        and
        not(./descendant::*[not(
            {elements}
    )])'''.format(
        mapped=one_of_xpath(_tags),
        elements=one_of_xpath(_elements))
    return xp

def _xp_all_of(types):
    xp = is_instance_xpath(types)
    return XPath('''./descendant-or-self::*[
        {predicate}
    ]'''.format(predicate=xp))


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


def findall(tree, types=None):
    if types is None:
        types = (dict, list)
    candidates = _xp_all_of(types)(tree)
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


def getall(tree, types=None):
    return [make(obj) for obj in findall(tree, types=types)]


def is_instance(tree, types=None):
    if types is None:
        types = (dict, list)
    return XPath(is_instance_xpath(types))(tree)

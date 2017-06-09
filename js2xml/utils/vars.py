from js2xml import parse, pretty_print as tostring
from js2xml.utils.objects import make as objects_make


MAKE_OBJECTS_TYPES = (
    # Types that can be handled by make_dict.
    'array',
    'object',
    'property',
    'string',
    'boolean',
    'number',
    'undefined',
)


def make_obj(tree, ignore_tags=(), _ignore=object()):
    if tree.tag == 'null':
        return

    if tree.tag == 'identifier':
        return tree.get('name')

    if tree.tag in MAKE_OBJECTS_TYPES:
        return objects_make(tree)

    if tree.tag == 'var':
        obj = {}
        children = tree.getchildren()
        # var can have no children if there is no value.
        if children:
            assert len(children) == 1
            value = make_obj(children[0], ignore_tags=ignore_tags, _ignore=_ignore)
            if value is not _ignore:
                obj[tree.attrib['name']] = value
        return obj

    if tree.tag == 'assign':
        assert tree.attrib['operator'] == '=', "only = operator supported"
        left_element = _xpath_one(tree, 'left/*')
        right_element = _xpath_one(tree, 'right/*')
        obj = {}
        name = make_varname(left_element)
        value = make_obj(right_element, ignore_tags=ignore_tags, _ignore=_ignore)
        if value is not _ignore:
            obj[name] = value
        return obj

    if '*' in ignore_tags or tree.tag in ignore_tags:
        return _ignore

    raise ValueError("Unknown tag: %s" % tree.tag)


def make_varname(tree):
    """
    <left> tree </left>
    """
    if tree.tag == 'identifier':
        return tree.attrib['name']

    if tree.tag in ('string', 'boolean'):
        return tree.text

    if tree.tag == 'number':
        return tree.attrib['value']

    if tree.tag in ('property', 'object'):
        return make_varname(_xpath_one(tree, '*'))

    if tree.tag.endswith('accessor'):
        kind = tree.tag[:-len('accessor')]
        obj = make_varname(_xpath_one(tree, 'object'))
        prop = make_varname(_xpath_one(tree, 'property'))
        if kind == 'dot':
            fmt = '%s.%s'
        elif kind == 'bracket':
            fmt = '%s[%s]'
        else:
            raise ValueError("Unknown accessor: %s" % tree.tag)
        return fmt % (obj, prop)

    raise ValueError("Unknown tag: %s" % tree.tag)


def get_vars(tree, doseq=False, ignore_tags=()):
    """

    >>> get_vars(parse('myobj.a = 42;'))
    {'myobj.a': 32}
    >>> get_vars(parse('''otherobj = [{a: 2, 3: "test"}];'''))
    {'otherobj': [{'a': 2, '3': 'test'}]}

    """
    vars = {}
    elements = tree.xpath('/program/*[self::var[@name] or self::assign[@operator="="]]')
    for el in elements:
        obj = make_obj(el, ignore_tags=ignore_tags)
        assert isinstance(obj, dict)
        if doseq:
            for key, val in obj.items():
                vars.setdefault(key, []).append(val)
        else:
            vars.update(obj)
    return vars


def _xpath_one(tree, xpath):
    elements = tree.xpath(xpath)
    if not elements:
        raise ValueError("no matching element")
    if len(elements) > 1:
        raise ValueError("more than one matching element")
    return elements[0]

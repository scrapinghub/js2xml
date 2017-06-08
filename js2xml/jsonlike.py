from functools import partial

from js2xml.utils.objects import findall, getall, is_instance, make


_jsonlike_types = (dict, list)

findall = partial(findall, types=_jsonlike_types)
getall = partial(getall, types=_jsonlike_types)
is_jsonlike = partial(findall, types=_jsonlike_types)
make_dict = make

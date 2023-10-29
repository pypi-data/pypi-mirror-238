from django import template

register = template.Library()


# filter
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def sentence_case(str_):
    if str_:
        return ". ".join([l.capitalize() for l in str_.split(". ")])
    else:
        return


@register.filter
def list_to_newline(list_):
    if isinstance(list_, list) and list_:
        return "\n".join(list_)
    else:
        return "---"


@register.filter
def ifinlist(value, list_):
    return value in list_


# simple tag
@register.simple_tag
def combine_url_lists(list1, list2):
    return list1 + list2

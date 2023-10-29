"""
How to reverse a name to a absolute url in django template

- https://stackoverflow.com/questions/19024159/how-to-reverse-a-name-to-a-absolute-url-in-django-template/34630561
"""
from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def abs_url(context, view_name, *args, **kwargs):
    # Could add except for KeyError, if rendering the template
    # without a request available.
    return context["request"].build_absolute_uri(
        reverse(view_name, args=args, kwargs=kwargs)
    )


@register.filter
def as_abs_url(path, request):
    return request.build_absolute_uri(path)

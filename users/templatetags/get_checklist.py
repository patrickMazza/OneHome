from django import template

register = template.Library()


@register.filter()
def getchecks(things, category):
    return things.filter(category=category)

from django import template

register = template.Library()

@register.simple_tag
def save(data):
    print("here")
    print(data)
    return len(data)
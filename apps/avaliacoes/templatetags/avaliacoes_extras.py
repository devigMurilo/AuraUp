from django import template

register = template.Library()

@register.filter
def stars(nota):
    try:
        n = int(nota)
        return '★' * n + '☆' * (5 - n)
    except:
        return '☆☆☆☆☆'

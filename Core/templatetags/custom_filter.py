from django import template

register = template.Library()

@register.filter
def millify(n):
    try:
        n = float(n)
        if n >= 1_000_000_000:
            return f'{n/1_000_000_000:.1f}B'
        elif n >= 1_000_000:
            return f'{n/1_000_000:.1f}M'
        elif n >= 1_000:
            return f'{n/1_000:.1f}K'
        else:
            return str(int(n))
    except (ValueError, TypeError) as e:
        return n  # In case of any exception, just return the original value

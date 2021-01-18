def delta(expr):
    return r'\Delta{%s}' % expr


def bar(expr):
    return r'\bar{%s}' % expr


def idx(expr, i='i'):
    return fr'{expr}_{{{i}}}'


d = delta
b = bar
i = idx
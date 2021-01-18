from decimal import Decimal

import sympy as sp


def big_r(values):
    return (max(values) - min(values)).normalize()


def big_u(values):
    v = sorted(values)
    return map(lambda a, b: (a - b).normalize(), v[1:], v[:-1])


def get_upn(n, p):
    return {1: Decimal(1.5), 2: Decimal('1.16'), 3: Decimal('0.94'), 4: Decimal('0.76'), 5: Decimal('0.64'), 7: Decimal('0.51'), 10: Decimal('0.41')}[n]


def get_tpn(n, p):
    return {2: Decimal('12.7'), 3: Decimal('4.3'), 4: Decimal('3.2'), 5: Decimal('2.8'), 6: Decimal('2.6'), 7: Decimal('2.5'), 8: Decimal('2.4'), 9: Decimal('2.3'), 10: Decimal('2.3'), 100: Decimal('2.0')}[n]


def get_bpn(n, p):
    return {2: Decimal('1.6'), 3: Decimal('1.3'), 4: Decimal('0.72'), 5: Decimal('0.51'), 6: Decimal('0.40'), 7: Decimal('0.33'), 10: Decimal('0.41')}[n]


def get_u(values, p=95):
    return (big_r(values) * get_upn(len(values), p)).normalize()


def exp_man(val, exp_l=None, r=None):
    def exp(number):
        (sign, digits, exponent) = Decimal(number).as_tuple()
        return len(digits) + exponent - 1

    def man(number):
        return Decimal(number).scaleb(-exp(number)).normalize()

    if r is None:
        if exp_l is None:
            return man(val).normalize(), exp(val)
        return Decimal(val).scaleb(exp_l).normalize(), exp_l
    if exp_l is None:
        return round(man(val), r).normalize(), exp(val)
    return round(Decimal(val).scaleb(exp_l), r).normalize(), exp_l


def fmt_exp_man(val, exp_l=None, r=None):
    if exp_l == 0:
        exp_l = None
    if val == 0:
        return str(0)
    man, exp = exp_man(val, exp_l=exp_l, r=r)
    if abs(exp) > 3:
        return r'%s \cdot 10^{%s}' % (man, exp)
    return str(val)


def derivatives(vals, expr, dv, mapper=sp.simplify):
    v = {k: sp.symbols(v) for k, v in vals.items()}
    f = eval(expr, v)
    return f, [mapper(f.diff(v[x])) for x in dv]


def inaccuracy(values, theta):
    v = list(map(Decimal, values))
    N = len(values)
    barx = sum(v) / len(v)

    sx = (sum(map(lambda x: (x - barx) ** 2, v)) / (N * (N - 1))).sqrt()
    dx = get_tpn(N, 95) * sx
    bar_dx = (dx ** 2 + Decimal(theta) ** 2).sqrt()

    return barx, bar_dx


if __name__ == '__main__':
    print(derivatives(
        {'r': r'\bar{\rho}', 'R': r'\bar{R}', 'l': r'\bar{l}', 'e': r'\varepsilon_0'},
        '(r*R**2)/(3*e*(R + l))',
        ['r', 'R', 'l']
    ))

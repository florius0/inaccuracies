# from sympy import *
import pandas as pd

import latex as lt
from helpers import *

FV_COLS = ['Формула', 'Значение']


def fwd_table1(vn, values, theta, fmt=lambda x: x):
    N = len(values)
    v = list(map(Decimal, values))
    h = lambda v: map(fmt, v)
    hh = fmt
    t = Decimal(theta)
    vals = [
        [lt.i(vn), *h(v), fr'\theta_{vn}={hh(t)}'],
        [lt.i(vn) + r'\uparrow', *h(sorted(v)),
         fr'{lt.i("R", i=vn)} = {lt.i(vn, i="N")} - {lt.i(vn)} = {hh(big_r(v))}'],
        [fr'U_{{ {vn} i}}', *h(big_u(v)), '-', fr'U_{vn} = U_{{P,N}} R_{vn} = {hh(get_u(v))}']  # TODO
    ]
    return pd.DataFrame([['$%s$' % x for x in v] for v in vals],
                        columns=['№', *map(lambda v: f'${v}$', range(1, N + 1)), fr'$\theta_{vn}$'])


def fwd_table2(vn, values, theta, fmt=lambda x: x, vertical=True):
    v = list(map(Decimal, values))
    N = len(values)
    barx = sum(v) / len(v)
    t = Decimal(theta)
    sx = (sum(map(lambda x: (x - barx) ** 2, v)) / (N * (N - 1))).sqrt()
    dx = get_tpn(N, 95) * sx
    bar_dx = (dx ** 2 + t ** 2).sqrt()

    h = fmt
    vals = [
        r'$%s$' % h(barx),
        r'$%s$' % h(sx),
        r'$%s$' % h(dx),
        r'$%s$' % h(big_r(v)),
        r'$%s$' % h(get_bpn(N, 95) * big_r(v)),
        r'$%s$' % h(t),
        r'$%s$' % h(bar_dx),
        r'$%s$' % fr'{h(barx)} \pm {h(bar_dx)}'
    ]
    cols = [
        r'$%s = \frac{1}{N} \sum{%s}$' % (lt.b(vn), lt.i(vn)),
        r'$S_{\bar{%s}} = \sqrt{ \frac{\sum{(%s - %s)^2}} {N(N-1)} }$' % (lt.b(vn), lt.i(vn), lt.b(vn)),
        r'$%s = t_{P,N} S_{%s}$' % (lt.d(vn), lt.b(vn)),
        r'$R_{%s} = %s_{max} - %s_{min}$' % (vn, vn, vn),
        r'$%s = \beta_{P,N} R_{%s}$' % (lt.d(lt.i(vn, i=r'\beta')), vn),
        r'$%s$' % lt.i(r'\theta', i=vn),
        r'$%s = \sqrt{%s ^ 2 + %s ^ 2}$' % (lt.b(lt.d(vn)), lt.d(vn), lt.i(r'\theta', i=vn)),
        r'$%s = %s \pm %s$' % (vn, lt.b(vn), lt.b(lt.d(vn)))
    ]
    cols2 = [
        r'$%s$' % lt.b(vn),
        r'$S_{%s}$' % lt.b(vn),
        r'$%s$' % lt.d(vn),
        r'$R_{%s}$' % vn,
        r'$%s$' % lt.d(lt.i(vn, i=r'\beta')),
        r'$%s$' % lt.i(r'\theta', i=vn),
        r'$%s$' % lt.b(lt.d(vn)),
        r'$%s$' % vn
    ]

    # print('\a')
    return pd.DataFrame(zip(cols, vals), columns=FV_COLS) if vertical else \
        pd.DataFrame([[FV_COLS[1], *vals]], columns=[FV_COLS[0], *cols])


def inacc_trans(fun_name=None, values_names=None, values=None, consts=None, expr='', fmt=lambda x: x, vertical=True):
    # v = {k: [Decimal(x) for x in v] for k, v in values.items()}
    vals_n = list(filter(lambda a: a not in consts.keys(), values_names.keys()))
    f, ds = derivatives(values_names, expr, vals_n)
    df_f = r'\left(\Delta{%s}\ \cdot %s \right)^2'

    values_inaccuracies = {values_names[k]: inaccuracy(v, t)[0] for k, (v, t) in values.items()}
    subs = dict(**values_inaccuracies, **{values_names[k]: v for k, v in consts.items()})
    # print(subs, f.subs(subs))
    fb = Decimal(str(f.subs(subs)))
    dsb = [Decimal(str(d.subs(subs).evalf())) for d in ds]

    values_inaccuracies_spread = [inaccuracy(v, t)[1] for _k, (v, t) in values.items()]
    dfb = sum(map(lambda a, b: (a * b) ** 2, dsb, values_inaccuracies_spread)).sqrt()

    percent_d = dfb / fb * 100

    cols = [
        fr'${lt.b(fun_name)} = {sp.latex(f)}$',
        fr'${lt.b(lt.d(fun_name))} = \sqrt{{' + ' + '.join(
            [df_f % (v, sp.latex(d)) for d, v in zip(ds, vals_n)]) + '}$',
        r'$%s = %s \pm %s$' % (fun_name, lt.b(fun_name), lt.d(lt.b(fun_name))),
        r'$\delta %s = \frac{%s}{%s}' % (fun_name, lt.d(lt.b(fun_name)), lt.b(fun_name)) + r'\cdot 100\%$'
    ]
    vals = [
        r'$%s$' % fmt(fb),
        r'$%s$' % fmt(dfb),
        r'$%s = %s \pm %s$' % (fun_name, fmt(fb), fmt(dfb)),
        f'${fmt(percent_d)}\%$'
    ]

    return pd.DataFrame(zip(cols, vals), columns=FV_COLS) if vertical else \
        pd.DataFrame([[FV_COLS[1], *vals]], columns=[FV_COLS[0], *cols])


def split_df(df, by):
    return filter(lambda d: not d.empty, [df.iloc[:, i * by:(i + 1) * by] for i in range(len(df.columns) // by + 1)])


if __name__ == '__main__':
    pd.set_option('display.max_colwidth', None)
    # formatting output
    # print(fwd_table1(r'\rho', ['3.1e-5', '3.2e-5', '3.6e-5', '3.4e-5', '3.2e-5'], '0.1e-5',
    #                  fmt=lambda x: fmt_exp_man(x, exp_l=5)).to_latex(index=False,
    #                                                              escape=False))

    # just output
    # print(fwd_table1(r'd', ['2.49', '2.51', '2.52', '2.54', '2.53'], '0.01').to_latex(index=False, escape=False))

    # rounding
    # print(fwd_table2(r'd', ['2.49', '2.51', '2.52', '2.54', '2.53'], '0.01',
    #                  fmt=lambda x: round(x, 4).normalize()).to_latex(index=False, escape=False))

    # splitting dataframe
    # print(*split_df(fwd_table2(r'd', ['2.49', '2.51', '2.52', '2.54', '2.53'], '0.01',
    #                           fmt=lambda x: round(x, 4).normalize()), 3), sep='\n')
    print(inacc_trans(
        fun_name=r'\varphi',
        values_names={'r': r'\rho', 'R': r'R', 'l': r'l', 'e': r'\varepsilon_0'},
        values={'r': (['3.1e-5', '3.2e-5', '3.6e-5', '3.4e-5', '3.2e-5'], '0'),
                'R': (['202', '203', '206', '208', '206'], '0'),
                'l': (['108', '109', '110', '112', '110'], '0')},
        expr='(r*R**2)/(3*e*(R + l))',
        consts={'e': Decimal('8.85e-12')},
        fmt=lambda x: fmt_exp_man(x, r=2)
    ).to_latex(index=False, escape=False))

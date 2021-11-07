import click
import pandas as pd
from pprint import pprint

import core as ia

# print(os.environ['PYTHONPATH'])
LATEX_KWARGS = dict(index=False, escape=False, longtable=False, caption='Таблица', bold_rows=True)
TO_LATEX = True


def frnd(x, rnd):
    if rnd is None:
        return x
    if ia.exp_man(x)[1] <= -rnd:
        return x
    return round(x, rnd)


def get_fmt(rnd, exp):
    return lambda x: ia.fmt_exp_man(frnd(x, rnd), r=exp) if exp is not None else frnd(x, rnd)


@click.group()
def main():
    pass


@main.command()
@click.argument('varname')
@click.option('--values', '-v', required=True)
@click.option('--theta', '-t', default='0')
@click.option('--exp', '-e', default=None, type=int)
@click.option('--rnd', '-r', default=None, type=int)
def fwd(*args, **kwargs):
    pd.options.display.max_colwidth = 10 ** 6
    _fwd(*args, **kwargs)


def _fwd(varname, values, theta, rnd=None, exp=None):
    fmt = get_fmt(rnd, exp)

    t1 = ia.fwd_table1(varname, values.split(), theta, fmt=fmt)
    t2 = ia.fwd_table2(varname, values.split(), theta, fmt=fmt)
    print(t1.to_latex(**LATEX_KWARGS) if TO_LATEX else t1.to_clipboard())
    print(t2.to_latex(**LATEX_KWARGS) if TO_LATEX else t2.to_clipboard())


def parse_dict(val):
    # print([x.split('=') for x in val.split()])
    return {k: v for k, v in [x.split('=') for x in val.split()]}


@main.command()
@click.option('--name', '-n', required=True)
@click.option('--values_names', '-vn', required=True)
@click.option('--values', '-v', required=True)
@click.option('--expr', '-ex', required=True)
@click.option('--const', '-c')
@click.option('--exp', '-e', default=None, type=int)
@click.option('--rnd', '-r', default=None, type=int)
@click.option('--all', '-a', default=False, type=bool, is_flag=True)
def trs(name, values_names, values, expr, rnd=None, exp=None, const=None, all=False):
    pd.options.display.max_colwidth = 10 ** 6
    fmt = get_fmt(rnd, exp)

    const = {} if const is None else parse_dict(const)
    vn = parse_dict(values_names)
    v = {k: (v.split(',')[:-1], v.split(',')[-1]) for k, v in parse_dict(values).items()}

    if all:
        for varname, (vals, t) in v.items():
            _fwd(vn[varname], ' '.join(vals), t, rnd=rnd, exp=exp)

    t = ia.inacc_trans(fun_name=name, expr=expr, values_names=vn, values=v, consts=const, fmt=fmt)
    print(t.to_latex(**LATEX_KWARGS) if TO_LATEX else t)

@main.command()
@click.option('--name', '-n', required=True)
@click.option('--values_names', '-vn', required=True)
@click.option('--values', '-v', required=True)
@click.option('--expr', '-ex', required=True)
@click.option('--const', '-c')
@click.option('--exp', '-e', default=None, type=int)
@click.option('--rnd', '-r', default=None, type=int)
@click.option('--all', '-a', default=False, type=bool, is_flag=True)
def sel(name, values_names, values, expr, rnd=None, exp=None, const=None, all=False):
    pd.options.display.max_colwidth = 10 ** 6
    fmt = get_fmt(rnd, exp)

    const = {} if const is None else parse_dict(const)
    vn = parse_dict(values_names)
    v = {k: (v.split(',')[:-1], v.split(',')[-1]) for k, v in parse_dict(values).items()}

    if all:
        for varname, (vals, t) in v.items():
            _fwd(vn[varname], ' '.join(vals), t, rnd=rnd, exp=exp)

    tables = ia.inacc_select(fun_name=name, expr=expr, values_names=vn, values=v, consts=const, fmt=fmt)

    for t in tables:
        print(t.to_latex(**LATEX_KWARGS) if TO_LATEX else t)


if __name__ == '__main__':
    main()

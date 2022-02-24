#!/usr/bin/env python3

import pandas as pd
import multiprocessing as mp

from typing import Iterable, List

# TODO: compare yield vs list materialization performance (about the same with a simple time test)

def generate_times(with_seconds:bool = False) -> Iterable[str]:
    freq = '1S' if with_seconds else '1T'
    format = '%H:%M:%S' if with_seconds else '%H:%M'
    return (pd.DataFrame(columns=[], index=pd.date_range('2000-01-01T00:00:00Z', '2000-01-01T23:59:59Z', freq=freq))
        .between_time('00:00:00', '23:59:59')
        .index.strftime(format)
        .tolist()
    )

def check_number(s: str) -> bool:
    # Skip over permutations with extra leading 0s
    if s[0] == '0' and s != '0':
        return False
    return s != ''  # assume that everything else is a number

ops = ['*', '/', '+', '-']  # could conceivably also handle **, %, etc.
def generate_expressions(s: str) -> Iterable[str]:
    # Start with no op.
    len_s = len(s)
    if check_number(s):
        yield s
    if len_s < 2:  # base case
        return
    for op in ops:
        for op_pos in range(1, len_s):
            l = s[0:op_pos]
            r = s[op_pos:]
            # Also try to break longer numbers up further.
            for l_expn in generate_expressions(l):
                for r_expn in generate_expressions(r):
                    yield f"({l_expn}{op}{r_expn})"

def generate_equations(s: str) -> Iterable[str]:
    cmps = ['==']   # could conceivably also handle <, <=, >, >=
    s = s.replace(':', '')
    for cmp in cmps:
        for cmp_pos in range(1, len(s)):
            # In different pivot positions, split the string into left and right sides.
            l = s[0:cmp_pos]
            r = s[cmp_pos:]
            # Try inserting operators between digits for each side as well.
            for l_expn in generate_expressions(l):
                for r_expn in generate_expressions(r):
                    yield l_expn + cmp + r_expn

def check_equation(s: str) -> bool:
    # TODO: improve the safety and/or perf of this by using ast?
    try:
        return eval(s)
    except ZeroDivisionError:
        return None

def _process_time_str(time_str: str) -> List[str]:
    eqs = []
    for equation in generate_equations(time_str):
        result = check_equation(equation)
        eqs.append(f"{time_str}\t{equation}\t{result}")
    return eqs

def _print_results(res: List[str]):
    print("\n".join(res))

def generate_equation_times(with_seconds: bool = False):
    # parallelize working on individual times
    with mp.Pool(mp.cpu_count()) as pool:
        results = [pool.apply_async(_process_time_str, (time_str,)) for time_str in generate_times(with_seconds)]
        for res in results:
            _print_results(res.get())

if __name__ == '__main__':
    generate_equation_times(with_seconds=False)

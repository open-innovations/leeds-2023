import ast
import re

def literal_converter(series):
    def convert(value):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value
    return series.apply(convert)


def standardise_columns(name):
    return re.sub(r'[\s\-/]+', '_', name.lower().strip())


def named_cumulative_sum(data):
    return data.cumsum().rename(columns=lambda c: f'cumulative_{c}')
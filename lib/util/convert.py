import ast

def literal_converter(series):
    def convert(value):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value
    return series.apply(convert)

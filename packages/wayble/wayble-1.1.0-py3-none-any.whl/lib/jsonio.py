import json
import functools


def jsonio(func):
    """
    A decorator that abstracts away the reading and writing of JSON data.
    """
    @functools.wraps(func)
    def wrapper(input_file, output_file, *args, **kwargs):
        with open(input_file, 'r') as f:
            data = json.load(f)

        result = func(data, *args, **kwargs)

        with open(output_file, 'w') as f:
            json.dump(result, f)

    return wrapper

from functools import reduce


def recursive_get(d: dict, keys, default=None):
    """Apply a get recursive to the dictionary.

    Args:
        d (dict): Dictionary.
        keys (str|list|tuple): If is a str keyA.keyB => [keyA, keyB].
        default (mixed): Not required.

    Returns:
        The return value.

    Examples:
        Run function.

        >>> recursive_get({'NUMBER': {'ONE': 1 }}, 'NUMBER.ONE')
        1
    """
    if isinstance(keys, str):
        keys = keys.split('.')
    result = reduce(lambda c, k: c.get(k, {}), keys, d)
    if default is not None and result == {}:
        return default
    return result

def format_numbers(value) -> str:
    if isinstance(value, (int, float)):
        '{:,.0f}'.format(value).replace(',', '.')
    return value

def format_str(value) -> str:
    if isinstance(value, (int, float, bool)):
        return str(value)
    return value
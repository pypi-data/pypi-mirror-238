"""Utilities"""

def si_postfix_unit_to_int(si_unit):
    """
    Converts a postfixed SI unit into an int
    Supports k, M and G postfix.

    :param si_unit: SI unit with postfix e.g. 1M, 11k
    :type si_unit: str
    :return: int representation SI unit
    """
    if si_unit[-1] == 'k':
        value = float(si_unit.strip('k')) * 1000
    elif si_unit[-1] == 'M':
        value = float(si_unit.strip('M')) * 1_000_000
    elif si_unit[-1] == 'G':
        value = float(si_unit.strip('G')) * 1e9
    else:
        value = float(si_unit)
    return int(value)

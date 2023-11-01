def cm2inch(*tupl):
    """
    length unit conversion： cm --> inch
    Parameters
    ----------
    tupl: tuple
        centimeter
    Returns
    -------
    tuple: inch
    """
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i / inch for i in tupl[0])
    else:
        return tuple(i / inch for i in tupl)

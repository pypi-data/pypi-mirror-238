from numpy import ndarray


def add(LHS: ndarray, RHS: ndarray) -> ndarray:
    """
    Simple function for adding to vectors
    :param LHS: left hand side of the sum
    :param RHS: right hand side of the sum
    :return the sum of the LHS and RHS
    """
    if len(LHS) != len(RHS):
        raise ValueError("Both data must be same length")
    if len(LHS) == 0:
        raise ValueError("no data to add")
    return LHS + RHS

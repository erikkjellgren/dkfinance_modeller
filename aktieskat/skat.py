def aktiebeskatning(dkk: float, progressionsgrænse: float = 55300) -> float:
    r"""Aktiebskatning.

    .. math::
       skat(k) = 0.27 \min(pg, k) + 0.42 \max(0, k - pg)

    :math:`k` er overskudskapital.\n
    :math:`pg` er progressionsgrænse.

    Beskatning, https://www.skat.dk/SKAT.aspx?oId=2035568, 20-10-2020

    Args:
      dkk: Kapital til beskatning.
      progressionsgrænse: Grænse hvor skatten skifter fra 0.27% til 0.42%

    Returns:
      Skat
    """
    return min(progressionsgrænse, dkk) * 0.27 + max(0, dkk - progressionsgrænse) * 0.42


def aktiesparekontobeskatning(dkk: float) -> float:
    """Akstiesparekontobeskatning.

    .. math::
       skat(k) = 0.17 k

    :math:`k` er overskudskapital.

    Beskatning, https://skat.dk/skat.aspx?oid=17119, 20-10-2020

    Args:
      dkk: Kapital til beskatning.

    Returns:
      Skat
    """
    return dkk * 0.17


def pensionsbeskatning(dkk: float) -> float:
    """Pensionsopsparingsbeskatning.

    .. math::
       skat(k) = 0.153 k

    :math:`k` er overskudskapital.

    Beskatning, https://skat.dk/SKAT.aspx?oid=2234743, 20-10-2020

    Args:
      dkk: Kapital til beskatning.

    Returns:
      Skat
    """
    return dkk * 0.153


def nulskat(dkk: float) -> float:  # pylint: disable=W0613
    """Ingen beskatning.

    Args:
      dkk: Kapital til beskatning.

    Returns:
      Skat = 0 DKK
    """
    return 0

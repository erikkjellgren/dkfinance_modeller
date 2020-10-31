def nulvalutakurtage(dkk: float) -> float:  # pylint: disable=W0613
    """
    Ingen kurtage.

    Args:
      dkk: kapital der skal betales valutakurtage af.

    Returns:
      kurtage = 0 DKK
    """
    return 0.0


def saxo_underkonto_kurtage(dkk: float) -> float:
    """
    Valutakurtage for Saxo underkonto.

    https://www.home.saxo/da-dk/rates-and-conditions/commissions-charges-and-margin-schedule, 31-10-2020.

    Args:
      dkk: kapital der skal betales valutakurtage af.

    Returns:
      kurtage
    """
    return dkk * 0.0015


def nordnet_valutakonto_kurtage(dkk: float) -> float:
    """
    Valutakurtage for Nordnet valutakonto.

    https://www.nordnet.dk/faq/2334-hvad-koster-veksling-hos-nordnet-vs-min-bank, 31-10-2020

    Args:
      dkk: kapital der skal betales valutakurtage af.

    Returns:
      kurtage
    """
    return dkk * 0.00075

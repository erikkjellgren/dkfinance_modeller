from functools import partial
from typing import Callable


def nulkurtage(dkk: float, kurs: float = 0.0) -> float:  # pylint: disable=W0613
    """
    Ingen kurtage.

    Args:
      dkk: kapital der skal betales kurtage af.
      kurs: kurs på værdipapir.

    Returns:
      kurtage = 0 DKK
    """
    return 0.0


def saxo_nordnet_kurtage(
    dkk: float,
    kurs: float,
    valutakurs: float,
    kurtageprocent: float,
    minimums_kurtage: float,
    valutakurtage: float,
    saxo_usd_type: bool,
) -> float:
    r"""
    Kurtage for Nordnet og Saxo bank.
    Kurtagen er givet ved,

    .. math::
       kurtage(k) = \max(m, kp) + kv

    :math:`k` er inversteringskapital.

    :math:`m` er minimumskurtage.

    :math:`p` er kurtageprocent.

    :math:`v` er valutakurtageprocent.

    Med mindre det er Amerikanske aktier til under 10 USD ved Saxo, så er kurtagen givet ved,

    .. math::
       kurtage(k) = \max(m, 0.02 N) + kv

    :math:`N` er antal købte værdipapirer, faktoren foran er i USD.

    Args:
      dkk: kapital der skal betales kurtage af.
      kurs: kurs på værdipapir i DKK.
      kurtageprocent: kurtageprocent.
      minimums_kurtage:  minimums kurtage givet i værdipapirets valuta.
      valutakurtage: valutakurtage.
      saxo_usd_type: Aktiver speciel kurtage for USD værdipapirer hos Saxo bank, hvis kurs under 10 USD.

    Returns:
      kurtage
    """
    if saxo_usd_type and kurs / valutakurs < 10 and kurs != 0.0:
        kurtage = max(minimums_kurtage, dkk // kurs * 0.02 * valutakurs) + dkk * valutakurtage
    else:
        kurtage = max(minimums_kurtage, dkk * kurtageprocent) + dkk * valutakurtage
    return kurtage


def lunar_kurtage(
    dkk: float,
    kurs: float,  # pylint: disable=W0613
    kurtageprocent: float,
    minimums_kurtage: float,
    valutakurtage: float,
) -> float:
    """
    Kurtage for Lunar invest.
    Kurtagen er givet ved,

    .. math::
       kurtage = m + H(k-50000)kp + kv

    :math:`k` er inversteringskapital.\n
    :math:`m` er minimumskurtage.\n
    :math:`p` er kurtageprocent.\n
    :math:`v` er valutakurtageprocent.\n
    :math:`H(x)` er Heaviside step funktionen.
    """
    kurtage = minimums_kurtage + valutakurtage * dkk
    if dkk > 50000:
        kurtage += dkk * kurtageprocent
    return kurtage


def saxo_kurtage_bygger(
    valuta: str = "DKK", valutakurs: float = 1.0, underkonto: bool = False
) -> Callable[[float, float], float]:
    """
    Bygger af Saxo kurtage funktion.

    https://www.home.saxo/da-dk/rates-and-conditions/stocks/commissions, 21-10-2020

    Args:
      valuta: valuta værdipapir handles i. Euro vil give XETRA børsen.
      valutakurs: omregningsfaktor til DKK.
      underkonto: handler foretages i underkonto i given valuta.
                  Valutakurtagen vil ikke være inkluderet i kurtagefunktionen.

    Returns:
      Kurtagefunktion.
    """
    if valuta.lower() in ["dkk", "kr"]:
        kurtagefunktion = partial(
            saxo_nordnet_kurtage,
            kurs=0.0,
            valutakurs=1.0,
            kurtageprocent=0.001,
            minimums_kurtage=14,
            valutakurtage=0,
            saxo_usd_type=False,
        )
    elif valuta.lower() in ["euro", "eur"]:
        if underkonto:
            kurtagefunktion = partial(
                saxo_nordnet_kurtage,
                kurs=0.0,
                valutakurs=valutakurs,
                kurtageprocent=0.001,
                minimums_kurtage=2 * valutakurs,
                valutakurtage=0.0,
                saxo_usd_type=False,
            )
        else:
            kurtagefunktion = partial(
                saxo_nordnet_kurtage,
                kurs=0.0,
                valutakurs=valutakurs,
                kurtageprocent=0.001,
                minimums_kurtage=2 * valutakurs,
                valutakurtage=0.005,
                saxo_usd_type=False,
            )
    elif valuta.lower() in ["usd"]:
        if underkonto:
            kurtagefunktion = partial(
                saxo_nordnet_kurtage,
                kurs=0.0,
                valutakurs=valutakurs,
                kurtageprocent=0.001,
                minimums_kurtage=3 * valutakurs,
                valutakurtage=0.0,
                saxo_usd_type=True,
            )
        else:
            kurtagefunktion = partial(
                saxo_nordnet_kurtage,
                kurs=0.0,
                valutakurs=valutakurs,
                kurtageprocent=0.001,
                minimums_kurtage=3 * valutakurs,
                valutakurtage=0.005,
                saxo_usd_type=True,
            )
    return kurtagefunktion


def nordnet_kurtage_bygger(
    valuta: str = "DKK", valutakurs: float = 1.0, valutakonto: bool = False
) -> Callable[[float, float], float]:
    """
    Bygger af Nordnet kurtage funktion.

    https://www.nordnet.dk/dk/kundeservice/prisliste/priser-aktiedepot, 21-10-2020

    Medregner ikke GDR-gebyr.

    Args:
      valuta: valuta værdipapir handles i. Euro vil give XETRA børsen.
      valutakurs: omregningsfaktor til DKK.
      valutakonto: handler foretages i underkonto i given valuta.
                   Valutakurtagen vil ikke være inkluderet i kurtagefunktionen.

    Returns:
      Kurtagefunktion.
    """
    if valuta.lower() in ["dkk", "kr"]:
        kurtagefunktion = partial(
            saxo_nordnet_kurtage,
            kurs=0.0,
            valutakurs=1.0,
            kurtageprocent=0.001,
            minimums_kurtage=29,
            valutakurtage=0,
            saxo_usd_type=False,
        )
    elif valuta.lower() in ["euro", "eur"]:
        if valutakonto:
            kurtagefunktion = partial(
                saxo_nordnet_kurtage,
                kurs=0.0,
                valutakurs=valutakurs,
                kurtageprocent=0.0015,
                minimums_kurtage=12 * valutakurs,
                valutakurtage=0.0,
                saxo_usd_type=False,
            )
        else:
            kurtagefunktion = partial(
                saxo_nordnet_kurtage,
                kurs=0.0,
                valutakurs=valutakurs,
                kurtageprocent=0.0015,
                minimums_kurtage=12 * valutakurs,
                valutakurtage=0.0025,
                saxo_usd_type=False,
            )
    elif valuta.lower() in ["usd"]:
        if valutakonto:
            kurtagefunktion = partial(
                saxo_nordnet_kurtage,
                kurs=0.0,
                valutakurs=valutakurs,
                kurtageprocent=0.0015,
                minimums_kurtage=13 * valutakurs,
                valutakurtage=0.0,
                saxo_usd_type=False,
            )
        else:
            kurtagefunktion = partial(
                saxo_nordnet_kurtage,
                kurs=0.0,
                valutakurs=valutakurs,
                kurtageprocent=0.0015,
                minimums_kurtage=13 * valutakurs,
                valutakurtage=0.0025,
                saxo_usd_type=False,
            )
    return kurtagefunktion


def lunar_kurtage_bygger(valuta: str = "DKK") -> Callable[[float, float], float]:
    """
    Bygger af Lunar invest kurtage funktion.

    https://static-assets.prod.lunarway.com/da/docs/prisliste-privat/, 21-10-2020

    Args:
      valuta: valuta værdipapir handles i.

    Returns:
      Kurtagefunktion.
    """
    if valuta.lower() in ["dkk", "kr"]:
        kurtagefunktion = partial(
            lunar_kurtage, kurs=0.0, kurtageprocent=0.001, minimums_kurtage=19, valutakurtage=0.0,
        )
    elif valuta.lower() in ["euro", "eur", "usd"]:
        kurtagefunktion = partial(
            lunar_kurtage, kurs=0.0, kurtageprocent=0.001, minimums_kurtage=19, valutakurtage=0.005,
        )
    return kurtagefunktion

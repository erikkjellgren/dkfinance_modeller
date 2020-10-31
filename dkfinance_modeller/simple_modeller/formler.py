def årlig_til_n_rente(r: float, n: int) -> float:
    r"""Omregn en årlig rente til en rente over :math:`n` gange.

    .. math::
       r_{n}=\left(1+r\right)^{1/n}-1

    :math:`r` årlig rente.

    :math:`n` antal gange renten bliver beregnet per år.

    :math:`r_{n}` rente for :math:`n` periode.

    Args:
      r: årlig rente.
      n: antal gange renten beregnes.

    Returns:
      Rente for :math:`n` periode.
    """
    return (1 + r) ** (1 / n) - 1


def opsparing(kstart: float, kmåned: float, r: float, n: int) -> float:
    r"""Opsparings formel.

    .. math::
       k_{n} = k_{\mathrm{start}}\left(1+r\right)^{n} +
       k_{\mathrm{måned}}\left(\left(\frac{1-\left(1+r\right)^{n}}{-r}\right)-1
       + \left(1+r\right)^{n}\right)

    :math:`r` rente.

    :math:`n` antal gange renten bliver beregnet.

    :math:`k_{n}` slut kapital.

    :math:`k_{start}` start kapital.

    :math:`k_{måned}` månedlig ydelse.

    Args:
      kstart: start kapital.
      kmåned: månedlig indskud.
      r: månedlig rente.
      n: antal måneder.

    Returns:
      Slut kapital af opsparingen.
    """
    return kstart * (1 + r) ** n + kmåned * ((1 - (1 + r) ** n) / (-r) - 1 + (1 + r) ** n)


def afbetalling(klån: float, r: float, n: int) -> float:
    r"""Beregn størrelse af afbetallings størrelse for at afbetale et lån over :math:`n` gange.

    .. math::
       k_{\mathrm{afbetalling}} = \frac{k_{\mathrm{lån}}\left(1+r\right)^{n}}
       {\left(\frac{1-\left(1+r\right)^{n}}{-r}\right) - 1+\left(1+r\right)^{n}}

    :math:`r` rente på lånet.

    :math:`n` antal gange der skal afbetales.

    :math:`k_{lån}` start kapital der skal afbetales.

    :math:`k_{\mathrm{afbetalling}}` månedlig ydelse.

    Args:
      klån: Kapital der skal tilbage betales.
      r: renten på lånet.
      n: antal afbetallinger.

    Returns:
      Ydelse for at afbetale lån over :math:`n` gange.
    """
    return klån * (1 + r) ** n / ((1 - (1 + r) ** n) / (-r) - 1 + (1 + r) ** n)
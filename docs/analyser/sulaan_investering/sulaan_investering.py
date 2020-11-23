from functools import partial
from typing import Tuple

from scipy import optimize

import dkfinance_modeller.simple_modeller.formler as formler


def SU_lån(år_uddanelse: int) -> Tuple[float, float, int]:
    """SU lån.

    Args:
      år_uddanelse: Antal år under uddannelse.

    Returns:
      Rentetab, månedligt afdrag og antal afdrags års.
    """
    # X årig uddannelse.
    rmåned = formler.årlig_til_n_rente(r=0.04, n=12)
    klånt = 3194.0 * 12 * år_uddanelse
    kskyld = formler.opsparing(kstart=0.0, kmåned=3194.0, r=rmåned, n=12 * år_uddanelse)
    # 18 måneder efter endt uddannelse uden afbetaling.
    rmåned = formler.årlig_til_n_rente(r=0.01, n=12)
    kskyld = formler.opsparing(kstart=kskyld, kmåned=0.0, r=rmåned, n=18)
    # Afdragsperiode
    if 100000 < klånt < 119999:
        år_afdrag = 11
    elif klånt > 180000:
        år_afdrag = 15
    else:
        raise ValueError("Afdrags periode for lånstørrelse er ikke programmeret.")
    kafdrag = formler.afbetalling(klån=kskyld, n=år_afdrag * 12, r=rmåned)
    # Total afdrag
    ktotalafdrag = kafdrag * år_afdrag * 12
    # Total rentetab
    tab = klånt - ktotalafdrag
    return tab, kafdrag, år_afdrag


def investering(
    årligt_afkast: float, kafdrag: float, år_uddanelse: int, år_afdrag: int, til_optimering: bool = False,
) -> float:
    """Simpel model for investering af SU lån.

    Simpel model for investering af SU lån.

    Antager at afkast i procent er det samme hver måned i hele perioden.

    Antager at der ikke skal betales skat.

    Args:
      årligt_afkast: Årligt afkast af investering.
      kafdrag: Månedligt afdrag af SU lån.
      år_uddanelse: Antal år under uddannelse.
      år_afdrag: Antal år afdraget er over.
      til_optimering: Bruges hvis mindste årligt afkast skal findes.

    Returns:
      kapital efter SU lån er tilbage betalt.
    """
    # Invester SU lån
    rmåned = formler.årlig_til_n_rente(r=årligt_afkast, n=12)
    kapital = formler.opsparing(kstart=0.0, kmåned=3194.0, r=rmåned, n=12 * år_uddanelse)
    # 18 måneder efter endt uddanelse
    kapital = formler.opsparing(kstart=kapital, kmåned=0.0, r=rmåned, n=18)
    # Afbetalling af lån
    kapital = formler.opsparing(kstart=kapital, kmåned=-kafdrag, r=rmåned, n=12 * år_afdrag)
    if til_optimering:
        kapital = abs(kapital)
    return kapital


uddannelse_antal_år = 3
_, kafdrags_sats, afdrag_antal_år = SU_lån(år_uddanelse=uddannelse_antal_år)
investering_baked = partial(
    investering,
    kafdrag=kafdrags_sats,
    år_uddanelse=uddannelse_antal_år,
    år_afdrag=afdrag_antal_år,
    til_optimering=True,
)
results = optimize.minimize(investering_baked, 0.01)
min_afkast_3år = results["x"][0]
print(min_afkast_3år)  # 0.015517570589908755

uddannelse_antal_år = 5
_, kafdrags_sats, afdrag_antal_år = SU_lån(år_uddanelse=uddannelse_antal_år)
investering_baked = partial(
    investering,
    kafdrag=kafdrags_sats,
    år_uddanelse=uddannelse_antal_år,
    år_afdrag=afdrag_antal_år,
    til_optimering=True,
)
results = optimize.minimize(investering_baked, 0.01)
min_afkast_5år = results["x"][0]
print(min_afkast_5år)  # 0.01681942428856252

import pytest  # isort:skip # noqa # pylint: disable=C0411,C0413

assert abs(min_afkast_3år - 0.015517570589908755) < 10 ** -6
assert abs(min_afkast_5år - 0.01681942428856252) < 10 ** -6
with pytest.raises(ValueError, match="Afdrags periode for lånstørrelse er ikke programmeret"):
    SU_lån(1)

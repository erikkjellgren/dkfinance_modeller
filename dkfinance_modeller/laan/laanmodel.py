from typing import Generator, Tuple

import dkfinance_modeller.utility.formler as formler


class SUlån:  # pylint: disable=R0902, R0903
    """
    Klasse for SU-lån.
    """

    def __init__(self, uddannelse_måneder: int, afdragsfrie_månder: int, rente: float) -> None:
        """Initializer for SUlån.

        Args:
          uddannelse_måneder: antal måneder uddannelse tager.
          afdragsfrie_månder: antal afdragsfrie måneder efter endt uddannelse.
          rente: rente i procent.
        """
        self._uddannelse_måneder = uddannelse_måneder
        self._afdragsfrie_månder = afdragsfrie_månder
        self._rente_månedelig = (1 + rente / 100) ** (1 / 12) - 1
        self._lånt = 0.0
        self._rente = 0.0
        self._skyldigt_beløb = 0.0
        # https://www.su.dk/su-laan/satser-for-su-laan/
        self.lån_per_måned = 3234
        self.uddannelse_rente_månedlig = (1 + 0.04) ** (1 / 12) - 1

    def propager_måned(self) -> Generator[Tuple[float, float], None, None]:
        """
        Propagere SU lån måned for måned.
        Positivt "afdrag" er lånte penge udbetalt.

        Returns:
          afdrag og fradrag.
        """
        for _ in range(self._uddannelse_måneder):
            self._skyldigt_beløb += self.lån_per_måned
            self._lånt += self.lån_per_måned
            self._skyldigt_beløb = self._skyldigt_beløb * (1 + self.uddannelse_rente_månedlig)
            self._rente += self._skyldigt_beløb * self.uddannelse_rente_månedlig
            yield self.lån_per_måned, 0.0
        for _ in range(self._afdragsfrie_månder):
            self._skyldigt_beløb = self._skyldigt_beløb * (1 + self._rente_månedelig)
            self._rente += self._skyldigt_beløb * self._rente_månedelig
            yield 0.0, 0.0
        afdragsmåneder, afdrag = self._beregn_afdrag()
        for _ in range(afdragsmåneder):
            self._skyldigt_beløb -= afdrag
            self._skyldigt_beløb = self._skyldigt_beløb * (1 + self._rente_månedelig)
            self._rente += self._skyldigt_beløb * self._rente_månedelig
            # 27% fradrag på renter.
            fradrag = 0.27 * min(afdrag, self._rente)
            self._rente -= min(afdrag, self._rente)
            yield -afdrag, fradrag

    def _beregn_afdrag(self) -> Tuple[int, float]:
        """
        Beregn månedlig afdrag og antal afdrags måneder.

        Returns:
          Antal afdrags måneder og månedlig afdrag.
        """
        # https://www.borger.dk/oekonomi-skat-su/SU-og-oekonomi-under-uddannelse/Studiegaeld-oversigt/Studiegaeld-tilbagebetaling
        afdrags_månder = 0
        if self._lånt < 40000:
            afdrags_månder = 7 * 12
        elif self._lånt < 60000:
            afdrags_månder = 8 * 12
        elif self._lånt < 80000:
            afdrags_månder = 9 * 12
        elif self._lånt < 100000:
            afdrags_månder = 10 * 12
        elif self._lånt < 120000:
            afdrags_månder = 11 * 12
        elif self._lånt < 140000:
            afdrags_månder = 12 * 12
        elif self._lånt < 160000:
            afdrags_månder = 13 * 12
        elif self._lånt < 160000:
            afdrags_månder = 14 * 12
        else:
            afdrags_månder = 15 * 12
        afdrag_dkk = formler.afbetalling(klån=self._skyldigt_beløb, n=afdrags_månder, r=self._rente_månedelig)
        return afdrags_månder, afdrag_dkk

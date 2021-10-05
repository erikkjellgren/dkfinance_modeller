class Skat:  # pylint: disable=R0903
    """Skat.

    :ivar float progressionsgrænse: Progressionsgrænse.
    :ivar List[float] skatteprocenter: Skatteprocenter.
    :ivar Callable[[float],float] skattefunktion: Skattefunktion.
    """

    def __init__(self, beskatningstype: str) -> None:
        """Setup skat.

        Args:
          beskatningstype: Hvilken beskatning der skal bruges, ['aktie', 'ask', 'pension', 'nul'].
        """
        beskatningstype = beskatningstype.lower()
        if beskatningstype not in ["aktie", "ask", "pension", "nul"]:
            raise ValueError(
                f"beskatningstype, {beskatningstype}, er ikke i ['aktie', 'ask', 'pension', 'nul']"
            )
        if beskatningstype == "aktie":
            # Beskatning, https://www.skat.dk/SKAT.aspx?oId=2035568, 20-10-2020
            self.progressionsgrænse = 55300.0
            self.skatteprocenter = [0.27, 0.42]
            self.skattefunktion = self._aktiebeskatning
        elif beskatningstype == "ask":
            # Beskatning, https://skat.dk/skat.aspx?oid=17119, 20-10-2020
            self.skatteprocenter = [0.17]
            self.skattefunktion = self._simpelbeskatning
        elif beskatningstype == "pension":
            # Beskatning, https://skat.dk/SKAT.aspx?oid=2234743, 20-10-2020
            self.skatteprocenter = [0.153]
            self.skattefunktion = self._simpelbeskatning
        elif beskatningstype == "nul":
            self.skattefunktion = _nulskat

    def beregn_skat(self, dkk: float) -> float:
        """Beregn skat.

        Args:
          dkk: Kapital til beskatning.

        Returns:
          Skat i DKK.
        """
        return self.skattefunktion(dkk)

    def _aktiebeskatning(self, dkk: float) -> float:
        r"""Aktiebskatning.

        .. math::
           skat(k) = p_1 \min(pg, k) + p_2 \max(0, k - pg)

        :math:`k` er overskudskapital.

        :math:`pg` er progressionsgrænse.

        :math:`p_1` er lave skatteprocent.

        :math:`p_2` er høje skatteprocent.

        Beskatning, https://www.skat.dk/SKAT.aspx?oId=2035568, 20-10-2020

        Args:
          dkk: Kapital til beskatning.

        Returns:
          Skat i DKK.
        """
        return (
            min(self.progressionsgrænse, dkk) * self.skatteprocenter[0]
            + max(0, dkk - self.progressionsgrænse) * self.skatteprocenter[1]
        )

    def _simpelbeskatning(self, dkk: float) -> float:
        """Akstiesparekontobeskatning.

        .. math::
           skat(k) = p k

        :math:`k` er overskudskapital.

        :math:`p` er skatteprocenten.

        Beskatning, https://skat.dk/skat.aspx?oid=17119, 20-10-2020
        Beskatning, https://skat.dk/SKAT.aspx?oid=2234743, 20-10-2020

        Args:
          dkk: Kapital til beskatning.

        Returns:
          Skat i DKK.
        """
        return dkk * self.skatteprocenter[0]


def _nulskat(dkk: float) -> float:  # pylint: disable=W0613
    """Ingen beskatning.

    Args:
      dkk: Kapital til beskatning.

    Returns:
      Skat = 0 DKK.
    """
    return 0.0

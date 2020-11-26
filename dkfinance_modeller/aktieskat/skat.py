from typing import List

class Skat():
    """Depot."""

    def __init__(self, beskatningstype: str) -> None:
        """Setup skat.

        Args:
          beskatningstype: Hvilken beskatning der skal bruges, ['aktie', 'ask', 'pension', 'nul'].
        """
        beskatningstype = beskatningstype.lower()
        if beskatningstype not in ["aktie", "ask", "pension", "nul"]:
            raise ValueError(f"beskatningstype, {beskatningstype}, er ikke i ['aktie', 'ask', 'pension', 'nul']")
        if beskatningstype == "aktie":
            # Beskatning, https://www.skat.dk/SKAT.aspx?oId=2035568, 20-10-2020
            self.progressionsgrænse = 55300
            self.skatteprocenter = [0.27, 0.42]
            self.skattefuntion = self._aktiebeskatning
        elif beskatningstype == "ask":
            # Beskatning, https://skat.dk/skat.aspx?oid=17119, 20-10-2020
            self.skatteprocenter = [0.17]
            self.skattefuntion = self._simpelbeskatning
        elif beskatningstype == "pension":
            # Beskatning, https://skat.dk/SKAT.aspx?oid=2234743, 20-10-2020
            self.skatteprocenter = [0.153]
            self.skattefuntion = self._simpelbeskatning
        elif beskatningstype == "nul":
            self.skattefuntion = self._nulskat
        
    def beregn_skat(self, dkk: float) -> float:
        return self.skattefuntion(dkk)

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
          Skat
        """
        return min(self.progressionsgrænse, dkk) * self.skatteprocenter[0] + max(0, dkk - self.progressionsgrænse) * self.skatteprocenter[1]


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
          Skat
        """
        return dkk * self.skatteprocenter[0]


    def _nulskat(self, dkk: float) -> float:  # pylint: disable=W0613
        """Ingen beskatning.

        Args:
          dkk: Kapital til beskatning.

        Returns:
          Skat = 0 DKK
        """
        return 0

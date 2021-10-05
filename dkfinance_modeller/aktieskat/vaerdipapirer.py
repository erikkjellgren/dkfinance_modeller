class ETF:
    """ETF og investeringsforening."""

    def __init__(self, kurs: float, åop: float, beskatningstype: str) -> None:
        """Setup lagerbeskatningsdepot.

        Args:
          kurs: kurs på investering.
          åop: årligomkostningsprocent på ETF/investeringsforening.
          beskatningstype: kan være "lager" eller "realisation".
        """
        self.kurs = kurs
        self.åop = åop
        self.beskattet_kurs = 0.0
        self._antal_værdipapirer = 0
        if "lager" in beskatningstype.lower():
            self.lagerbeskatning = True
            self.realisationsbeskatning = False
        elif "realisation" in beskatningstype.lower():
            self.lagerbeskatning = False
            self.realisationsbeskatning = True
        else:
            raise ValueError(f"Beskatningstype, {beskatningstype}, findes ikke.")

    @property
    def antal_værdipapirer(self) -> float:
        """Getter for antal_værdipapirer.

        Returns:
          Antal værdipapirer
        """
        return self._antal_værdipapirer

    @antal_værdipapirer.setter
    def antal_værdipapirer(self, antal: int) -> None:
        """Setter for antal_værdipapirer.

        Args:
          antal: antal værdipapirer
        """
        self._antal_værdipapirer = antal
        if self._antal_værdipapirer < 0:
            raise Exception(f"Antal værdipapirer er negativ, antal_værdipapirer = {self._antal_værdipapirer}")

    def lagerrealisering(self, ændre_kurs: bool = True) -> float:
        """Beregn overskud via lagerbeskatning.

        Args:
          ændre_kurs: Sætter beskattet_kurs til kurs.
                      False hvis skattepligtig beholdning skal haves,
                      uden at skatten antages betalt.

        Returns:
          Kapital der skal beskattes.
        """
        beholdnings_ændring = self._antal_værdipapirer * (self.kurs - self.beskattet_kurs)
        if ændre_kurs:
            self.beskattet_kurs = self.kurs
        return beholdnings_ændring

    def opdater_kurs(self, kursændring: float) -> None:
        """Opdaterer kursen.

        Args:
          kursændring: Ændring af kurs.
        """
        if self.kurs + kursændring < 0.0:
            raise ValueError(f"kursændring, {kursændring}, vil få kurs, {self.kurs}, til at være negativ.")
        self.kurs += kursændring

    def modregn_åop(self) -> None:
        r"""Trækker ÅOP fra kursen, for en måned.

        .. math::
           \left.a_{n}\right|_{n=12}= \left. 1 - \left(\sqrt[n]{1-a}\right)\right|_{n=12}

        :math:`n` antal gange ÅOP betales over per år.

        :math:`a_n` er ÅOP splittet op i :math:`n` dele.

        :math:`a` er ÅOP.
        """
        åop_12 = 1.0 - (1.0 - self.åop) ** (1 / 12)
        self.kurs = self.kurs * (1 - åop_12)

    def tilføj_enheder(self, antal: int) -> None:
        r"""Tilføj antal enheder af ETFen.

        ETF'er bliver beskattet via. gennemsnitsmetoden.
        Den nye gennemsnitskurs er derfor:

        .. math::
           k_\mathrm{avg, new} = \frac{n\cdot k + n_\mathrm{old}\cdot k_\mathrm{avg, old}}{n + n_\mathrm{old}}

        :math:`k` kurs.

        :math:`k_\mathrm{avg, new}` nye gennemsnitskurs.

        :math:`k_\mathrm{avg, old}` gammel gennemsnitskurs.

        :math:`n` antal værdipapirer der bliver tilføjet.

        :math:`n_\mathrm{old}` antal værdipapirer allerede i beholdningen.

        Args:
          antal: antal enheder at tilføje.
        """
        self.beskattet_kurs = (antal * self.kurs + self._antal_værdipapirer * self.beskattet_kurs) / (
            antal + self._antal_værdipapirer
        )
        self._antal_værdipapirer += antal

    def total_værdi(self) -> float:
        """Få total værdi af beholdning.

        Returns:
          Total værdi af beholdning.
        """
        return self.kurs * self._antal_værdipapirer

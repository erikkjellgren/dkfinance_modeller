from typing import Callable, List, Tuple


def køb_værdipapirer(
    kapital: float, kurs: float, kurtagefunktion: Callable[[float, float], float],
) -> Tuple[float, float, List[float]]:
    """Køb værdipapirer uden at gå i minus.

    Args:
      kaptital: kapital til at købe.
      kurs: pris på værdipapirer.
      kurtagefunktion: funktion der beksriver hvor meget kurtage der betales.

    Returns:
      Tilbageværende kapital.
      Kurtageudgifter.
      Liste af købteværdipapirer.
    """
    værdipapirer = []
    antal_værdipapirer = kapital // kurs
    total_pris = antal_værdipapirer * kurs + kurtagefunktion(antal_værdipapirer * kurs, kurs)
    for _ in range(10000):
        if total_pris > kapital:
            antal_værdipapirer -= 1
            total_pris = antal_værdipapirer * kurs + kurtagefunktion(antal_værdipapirer * kurs, kurs)
        else:
            break
    for _ in range(int(antal_værdipapirer)):
        værdipapirer.append(kurs)
    kapitalændring = -antal_værdipapirer * kurs - kurtagefunktion(antal_værdipapirer * kurs, kurs)
    kurtageudgift = kurtagefunktion(antal_værdipapirer * kurs, kurs)
    return kapitalændring, kurtageudgift, værdipapirer


def beholdningsværdi(værdipapirer: List[float]) -> float:
    """Udregn den totale værdi af værdipapirer.

    Args:
      værdipapirer: liste af værdi af værdipapirer.

    Returns:
      Akkumulerede værdi.
    """
    værdi = 0.0
    for kurs in værdipapirer:
        værdi += kurs
    return værdi


class Lagerbeskatning:
    """Depot med lagerbeskatning"""

    def __init__(
        self,
        kapital_: float,
        kurtagefunktion_: Callable[[float, float], float],
        skattefunktion_: Callable[[float], float],
        kurs_: float,
        åop_: float = 0.0,
    ) -> None:
        """Setup lagerbeskatningsdepot

        Args:
          kapital: start kapital (DKK)
          kurtagefunktion: funktion der beksriver hvor meget kurtage der betales.
          skattefunktion: funktion der beskriver hvordan skatten udregnes.
          kurs: kurs på inverstering.
          åop: årligomkostningsprocent på ETF/inversteringsforening.
        """
        self.skattefunktion = skattefunktion_
        self.kurtagefunktion = kurtagefunktion_
        self.kapital = kapital_
        self.kurs = kurs_
        self.åop = åop_
        self.ubeskattet = 0.0
        self.værdipapirer: List[float] = []
        # Køb værdipapirer
        kapitalændring, kurtageudgift, købte_værdipapirer = køb_værdipapirer(
            self.kapital, self.kurs, self.kurtagefunktion
        )
        self.kapital += kapitalændring
        self.ubeskattet -= kurtageudgift
        self.værdipapirer = self.værdipapirer + købte_værdipapirer

    def propager_afkast(self, kursgevinst: float, udbytte: float) -> None:
        """Propager afkast og kurser med et år.

        Args:
          kursgevinst: procent ændring af kursen på værdipapirer.
          udbytte: udbytteprocent af værdipapirer.
        """
        beholdning = beholdningsværdi(self.værdipapirer)
        # Udbytte
        self.kapital += beholdning * udbytte
        self.ubeskattet += beholdning * udbytte
        # Kursgevinst
        self.ubeskattet += beholdning * (kursgevinst - self.åop)
        for i, kurs in enumerate(self.værdipapirer):
            self.værdipapirer[i] = kurs * (1 + kursgevinst - self.åop)
        self.kurs = self.kurs * (1 + kursgevinst - self.åop)
        # Udregn skat
        if self.ubeskattet > 0.0:
            skat = self.skattefunktion(self.ubeskattet)
            self.ubeskattet = 0.0
        else:
            skat = 0
        # Betal skat
        if skat > 0.0:
            if self.kapital > skat:
                self.kapital -= skat
            else:
                værdi = 0.0
                kurtage = 0.0
                for i, kurs in reversed(list(enumerate(self.værdipapirer))):
                    if self.kapital + værdi > skat + kurtage:
                        break
                    værdi += kurs
                    self.værdipapirer.pop(i)
                    kurtage = self.kurtagefunktion(værdi, self.kurs)
                self.kapital += værdi - skat - kurtage
                self.ubeskattet -= kurtage
        # Geninverster hvis muligt
        kapitalændring, kurtageudgift, købte_værdipapirer = køb_værdipapirer(
            self.kapital, self.kurs, self.kurtagefunktion
        )
        self.kapital += kapitalændring
        self.ubeskattet -= kurtageudgift
        self.værdipapirer = self.værdipapirer + købte_værdipapirer

    def total_salgsværdi(self) -> float:
        """Værdi af beholdningen ved salg af alle værdipapirer.

        Returns:
          Den totale værdi af beholdningen.
        """
        beholdning = beholdningsværdi(self.værdipapirer)
        kurtage = self.kurtagefunktion(beholdning, self.kurs)
        return self.kapital + beholdning - kurtage

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
    for _ in range(100):
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


class Lagerbeskatning:
    """Depot med lagerbeskatning"""

    def __init__(
        self,
        kapital_: float,
        kurtagefunktion: Callable[[float, float], float],
        skattefunktion: Callable[[float], float],
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
        self.skat = skattefunktion
        self.kurtage = kurtagefunktion
        self.kapital = kapital_
        self.kurs = kurs_
        self.åop = åop_
        self.ubeskattet = 0.0
        self.værdipapirer: List[float] = []
        # Køb værdipapirer
        kapitalændring, kurtageudgift, købte_værdipapirer = køb_værdipapirer(
            self.kapital, self.kurs, self.kurtage
        )
        self.kapital += kapitalændring
        self.ubeskattet -= kurtageudgift
        self.værdipapirer = self.værdipapirer + købte_værdipapirer


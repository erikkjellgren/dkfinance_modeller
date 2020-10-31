from typing import Callable, List, Tuple

import numpy as np

from dkfinance_modeller.aktieskat.valuta import nulvalutakurtage
from dkfinance_modeller.aktieskat.værdipapirer import ETF


def køb_værdipapirer(
    kapital: float, kurs: float, kurtagefunktion: Callable[[float, float], float],
) -> Tuple[float, float, int]:
    """Køb værdipapirer uden at gå i minus.

    Args:
      kaptital: kapital til at købe.
      kurs: pris på værdipapirer.
      kurtagefunktion: funktion der beskriver hvor meget kurtage der betales.

    Returns:
      Brugt kapital.
      Kurtageudgifter.
      Antal værdipapirer.
    """
    if kapital < 0.0:
        raise ValueError("kapital er negativ i køb_værdipapirer")
    if kurs <= 0.0:
        raise ValueError("kurs er negativ eller nul i køb_værdipapirer")
    antal_værdipapirer = kapital // kurs
    total_pris = antal_værdipapirer * kurs + kurtagefunktion(antal_værdipapirer * kurs, kurs)
    while total_pris > kapital:
        antal_værdipapirer -= 1
        total_pris = antal_værdipapirer * kurs + kurtagefunktion(antal_værdipapirer * kurs, kurs)
    kapitalændring = -antal_værdipapirer * kurs - kurtagefunktion(antal_værdipapirer * kurs, kurs)
    kurtageudgift = kurtagefunktion(antal_værdipapirer * kurs, kurs)
    return kapitalændring, kurtageudgift, int(antal_værdipapirer)


class Lagerbeskatning:  # pylint: disable=R0902
    """Depot med lagerbeskatning"""

    def __init__(
        self,
        kapital: float,
        kurtagefunktion: Callable[[float, float], float],
        skattefunktion: Callable[[float], float],
        minimumskøb: float,
        ETFer: List[ETF],
        ETF_fordeling: List[float],
        valutafunktion: Callable[[float], float] = nulvalutakurtage,
    ) -> None:
        """Setup lagerbeskatningsdepot

        Args:
          kapital: start kapital (DKK)
          kurtagefunktion: funktion der beskriver hvor meget kurtage der betales.
          skattefunktion: funktion der beskriver hvordan skatten udregnes.
          minimumskøb: minimumskapital der skal være ledigt for at lave nye køb.
          ETFer: List af ETF i depotet.
          ETF_fordeling: Procentiel fordeling af ETFer.
          valutafunktion: funktion der beskriver kurtage forbundet med valuta.
                          skal kun bruges hvis depotet ikke er i DKK, og denne
                          kurtage kun kommer ved indsættelse eller udtrækkelse af kapital.
        """
        self.kapital = kapital
        self.kurtagefunktion = kurtagefunktion
        self.skattefunktion = skattefunktion
        self.valutafunktion = valutafunktion
        self.minimumskøb = minimumskøb
        self.ubeskattet = 0.0
        self.ETFer = ETFer
        self.ETF_target_fordeling = ETF_fordeling
        self.måned = 0
        # Valutakurtage hvis depot ikke er i DKK
        valutakurtage = self.valutafunktion(self.kapital)
        self.kapital -= valutakurtage
        self.ubeskattet -= valutakurtage
        # Køb værdipapirer
        for i, procent in enumerate(self.ETF_target_fordeling):
            if procent * kapital > self.minimumskøb:
                kapitalændring, kurtageudgift, antal_værdipapirer = køb_værdipapirer(
                    self.kapital * procent, self.ETFer[i].kurs, self.kurtagefunktion
                )
                self.ubeskattet -= kurtageudgift
                self.kapital += kapitalændring
                self.ETFer[i].tilføj_enheder(antal_værdipapirer)

    def afkast_månedlig(  # pylint: disable=R0914,R0912
        self, kursgevinster: List[float], udbytter: List[float]
    ) -> None:
        """Propager en måned frem.

        Args:
          kursgevinster: kursgevinster i procent.
          udbytter: udbytter i aktuelle termer per værdipapir,
                    f.eks. 10.0, for 10.0 DKK udbytte per værdipapir.
        """
        self.måned = (self.måned + 1) % 12
        # Udbytte
        for _, (etf, udbytte) in enumerate(zip(self.ETFer, udbytter)):
            self.kapital += etf.antal_værdipapirer * udbytte
            self.ubeskattet += etf.antal_værdipapirer * udbytte
        # Kursgevinst
        for _, (etf, kursgevinst) in enumerate(zip(self.ETFer, kursgevinster)):
            etf.updater_kurs(kursgevinst)
        # ÅOP omkostning
        for etf in self.ETFer:
            etf.modregn_åop()
        # Udregn skat
        if self.måned == 0:
            for etf in self.ETFer:
                self.ubeskattet += etf.lagerrealisering()
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
                    # Lige nu vil der kun blive solgt en type ETF for at betale skatten.
                    # Ved store beholdninger eller 0.0 DKK minimumskrutage, vil salg
                    # af flere forskellige kunne være bedre ifht. rebalancering.
                    # Vælger derfor den ETF der har den største totale værdi.
                    etf_værdi = []
                    for etf in self.ETFer:
                        etf_værdi.append(etf.total_værdi())
                    etf_idx = np.argmax(etf_værdi)
                    if etf_værdi[etf_idx] < skat * 1.1:
                        raise Exception("Værdien af den største ETF er ikke stor nok til at betale skatten")
                    kurtage = 0.0
                    # Hvis depot ikke er i DKK
                    valutakurtage = self.valutafunktion(skat)
                    while self.kapital + værdi < skat + kurtage + valutakurtage:
                        værdi += self.ETFer[etf_idx].kurs
                        self.ETFer[etf_idx].antal_værdipapirer -= 1
                        kurtage = self.kurtagefunktion(værdi, self.ETFer[etf_idx].kurs)
                    self.kapital += værdi - skat - kurtage - valutakurtage
                    self.ubeskattet += -kurtage - valutakurtage
        # Geninverster
        if self.kapital > self.minimumskøb:
            # Lige nu vil der kun blive købt en type ETF per geninversteringsrunde.
            # Ved store beholdninger eller 0.0 DKK minimumskrutage, vil køb
            # af flere forskellige kunne være bedre ifht. rebalancering.
            # Vælger derfor den ETF der er længst fra target-værdien.
            etf_fordelling = []
            for etf in self.ETFer:
                etf_fordelling.append(etf.total_værdi())
            etf_fordelling = np.array(etf_fordelling)
            etf_fordelling = self.ETF_target_fordeling - etf_fordelling / np.sum(etf_fordelling)
            etf_idx = np.argmax(etf_fordelling)
            kapitalændring, kurtageudgift, antal_værdipapirer = køb_værdipapirer(
                self.kapital, self.ETFer[etf_idx].kurs, self.kurtagefunktion
            )
            self.kapital += kapitalændring
            self.ubeskattet -= kurtageudgift
            self.ETFer[etf_idx].tilføj_enheder(antal_værdipapirer)

    def total_salgsværdi(self) -> float:
        """Værdi af beholdningen ved salg af alle værdipapirer.

        Returns:
          Den totale værdi af beholdningen.
        """
        beholdning = 0.0
        kurtage = 0.0
        ubeskattet = 0.0
        for etf in self.ETFer:
            beholdning += etf.total_værdi()
            kurtage += self.kurtagefunktion(beholdning, etf.kurs)
            ubeskattet += etf.lagerrealisering(ændre_kurs=False)
            # Hvis depot ikke er i DKK
            valutakurtage = self.valutafunktion(self.kapital + beholdning - kurtage)
        return self.kapital + beholdning - kurtage - self.skattefunktion(ubeskattet) - valutakurtage

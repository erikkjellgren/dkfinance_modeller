import os
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

import dkfinance_modeller.aktieskat.depotmodel as depotmodel
import dkfinance_modeller.aktieskat.kurtage as kurtage
import dkfinance_modeller.aktieskat.skat as skat
import dkfinance_modeller.aktieskat.vaerdipapirer as værdipapirer
import dkfinance_modeller.aktieskat.valuta as valuta
import dkfinance_modeller.simple_modeller.formler as formler


def depoter() -> Tuple[depotmodel.DepotModel, depotmodel.DepotModel]:
    """Definere depoter.

    Returns:
      Depot med realationsbeskatning
    """
    etf1 = værdipapirer.ETF(kurs=100, åop=0.12 / 100)
    etf2 = værdipapirer.ETF(kurs=100, åop=0.55 / 100)
    lagerbeskatning = depotmodel.DepotModel(
        kapital=300000.0,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44),
        skattefunktion=skat.aktiebeskatning,
        minimumskøb=5000,
        beskatningstype="lager",
        ETFer=[etf1],
        ETF_fordeling=[1.0],
        valutafunktion=valuta.saxo_underkonto_kurtage,
    )
    realisationsbeskatning = depotmodel.DepotModel(
        kapital=300000.0,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="Dkk"),
        skattefunktion=skat.aktiebeskatning,
        minimumskøb=5000,
        beskatningstype="realisation",
        ETFer=[etf2],
        ETF_fordeling=[1.0],
    )
    return lagerbeskatning, realisationsbeskatning


data = np.genfromtxt(f"{os.path.dirname(__file__)}/../SP500.csv", delimiter=";")
real: List[List[float]] = [[], [], [], []]
lager: List[List[float]] = [[], [], [], []]
for j, antal_år in enumerate([1, 5, 10, 20]):
    for start in range(0, len(data) - 950 - antal_år * 12):
        lagerdepot, realisationsdepot = depoter()
        udbytte_årlig = 0.0
        kursstigning_årlig = 0.0
        for i in range(start + 950, start + 950 + 12 * antal_år):
            udbytteafkast = realisationsdepot.ETFer[0].kurs * data[i + 1, 4]
            kursafkast = realisationsdepot.ETFer[0].kurs * data[i + 1, 3]
            if i % 12 == 0:
                effektivt_udbytte = udbytte_årlig + max(0, 0.3 * kursstigning_årlig)
                realisationsdepot.afkast_månedlig(
                    [udbytteafkast + kursafkast - effektivt_udbytte], [effektivt_udbytte]
                )
                udbytte_årlig = 0.0
                kursstigning_årlig = 0.0
            else:
                realisationsdepot.afkast_månedlig([udbytteafkast + kursafkast], [0.0])
            lagerdepot.afkast_månedlig([udbytteafkast + kursafkast], [0.0])
            udbytte_årlig += udbytteafkast
            kursstigning_årlig += kursafkast
        real[j].append(realisationsdepot.total_salgsværdi())
        lager[j].append(lagerdepot.total_salgsværdi())
real_1år = np.array(real[0])
real_5år = np.array(real[1])
real_10år = np.array(real[2])
real_20år = np.array(real[3])
lager_1år = np.array(lager[0])
lager_5år = np.array(lager[1])
lager_10år = np.array(lager[2])
lager_20år = np.array(lager[3])
real_carg_1år = formler.CARG(300000, real_1år, 1)
real_carg_5år = formler.CARG(300000, real_5år, 5)
real_carg_10år = formler.CARG(300000, real_10år, 10)
real_carg_20år = formler.CARG(300000, real_20år, 20)
lager_carg_1år = formler.CARG(300000, lager_1år, 1)
lager_carg_5år = formler.CARG(300000, lager_5år, 5)
lager_carg_10år = formler.CARG(300000, lager_10år, 10)
lager_carg_20år = formler.CARG(300000, lager_20år, 20)

SizeX = 6
SizeY = 10
SIZE = 12
plt.rc("font", size=SIZE)  # controls default text sizes
plt.rc("axes", titlesize=SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=SIZE)  # fontsize of the x any y labels
plt.rc("xtick", labelsize=SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=SIZE * 0.9)  # legend fontsize
plt.rc("figure", titlesize=SIZE)  # # size of the figure title

q_real: List[List[float]] = [[], [], [], []]
q_lager: List[List[float]] = [[], [], [], []]
for i in range(0, 21):
    q_real[0].append(np.quantile(real_carg_1år, i * 0.05))  # type: ignore
    q_real[1].append(np.quantile(real_carg_5år, i * 0.05))  # type: ignore
    q_real[2].append(np.quantile(real_carg_10år, i * 0.05))  # type: ignore
    q_real[3].append(np.quantile(real_carg_20år, i * 0.05))  # type: ignore
    q_lager[0].append(np.quantile(lager_carg_1år, i * 0.05))  # type: ignore
    q_lager[1].append(np.quantile(lager_carg_5år, i * 0.05))  # type: ignore
    q_lager[2].append(np.quantile(lager_carg_10år, i * 0.05))  # type: ignore
    q_lager[3].append(np.quantile(lager_carg_20år, i * 0.05))  # type: ignore

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(SizeX, SizeY), sharex=True)
for i, ax in enumerate([ax1, ax2, ax3, ax4]):
    ax.plot(np.linspace(0.0, 1, 21), q_real[i], label="Realisationsbeskatning", linewidth=3)
    ax.plot(np.linspace(0.0, 1, 21), q_lager[i], label="Lagerbeskatning", linewidth=3)
ax1.legend()
for ax, år in zip([ax1, ax2, ax3, ax4], [1, 5, 10, 20]):
    ax.set_xticks(np.linspace(0.0, 1.0, 11))
    ax.grid(which="minor")
    ax.grid(which="major")
    ax.set_ylabel(f"CARG")
    ax.set_title(f"{år:1.0f} år inverstering")
ax1.set_ylim(-0.45, 0.45)
ax2.set_ylim(-0.1, 0.22)
ax3.set_ylim(-0.06, 0.15)
ax4.set_ylim(0.01, 0.14)
ax4.set_xlabel("fraktil")
plt.tight_layout()
plt.savefig("fraktiler.svg")

assert abs(q_real[0][-1] - 0.38709653149381973) < 10 ** -6
assert abs(q_real[1][-1] - 0.2061982584274995) < 10 ** -6
assert abs(q_real[2][-1] - 0.13726171826822742) < 10 ** -6
assert abs(q_real[3][-1] - 0.12953685759662048) < 10 ** -6
assert abs(q_lager[0][-1] - 0.34340802063444453) < 10 ** -6
assert abs(q_lager[1][-1] - 0.161098623361156) < 10 ** -6
assert abs(q_lager[2][-1] - 0.10370519249275945) < 10 ** -6
assert abs(q_lager[3][-1] - 0.08071732072917315) < 10 ** -6

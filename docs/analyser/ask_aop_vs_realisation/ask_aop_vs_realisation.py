import os
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

import dkfinance_modeller.aktieskat.depotmodel as depotmodel
import dkfinance_modeller.aktieskat.kurtage as kurtage
import dkfinance_modeller.aktieskat.skat as skat
import dkfinance_modeller.aktieskat.vaerdipapirer as værdipapirer
import dkfinance_modeller.aktieskat.valuta as valuta
import dkfinance_modeller.utility.formler as formler


def depoter(
    start_kapital: float, lagerbeskatning_procent: float
) -> Tuple[depotmodel.DepotModel, depotmodel.DepotModel, depotmodel.DepotModel]:
    """Definere depoter.

    Args:
      start_kapital: Start kapital for depoterne.
      lagerbeskatning_procent: Procent for det lager beskattede depot.

    Returns:
      Depot med realationsbeskatning.
    """
    etf1 = værdipapirer.ETF(kurs=100, åop=0.0 / 100, beskatningstype="lager")
    etf2 = værdipapirer.ETF(kurs=100, åop=0.0 / 100, beskatningstype="realisation")
    etf3 = værdipapirer.ETF(kurs=100, åop=0.0 / 100, beskatningstype="realisation")
    skatter1 = skat.Skat(beskatningstype="ask")
    skatter1.skatteprocenter = [lagerbeskatning_procent]
    skatter2 = skat.Skat(beskatningstype="aktie")
    skatter3 = skat.Skat(beskatningstype="ask")
    skatter3.skatteprocenter = [0.42]
    ask = depotmodel.DepotModel(
        kapital=start_kapital,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44),
        skatteklasse=skatter1,
        minimumskøb=1000,
        ETFer=[etf1],
        ETF_fordeling=[1.0],
    )
    normal = depotmodel.DepotModel(
        kapital=start_kapital,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44, underkonto=True),
        skatteklasse=skatter2,
        minimumskøb=1000,
        ETFer=[etf2],
        ETF_fordeling=[1.0],
        valutafunktion=valuta.saxo_underkonto_kurtage,
    )
    normal_worst_case = depotmodel.DepotModel(
        kapital=start_kapital,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44, underkonto=True),
        skatteklasse=skatter3,
        minimumskøb=1000,
        ETFer=[etf3],
        ETF_fordeling=[1.0],
        valutafunktion=valuta.saxo_underkonto_kurtage,
    )
    return ask, normal, normal_worst_case


def kør_model(  # pylint: disable=R0914
    start_kapital: float, lagerbeskatning_procent: float
) -> Tuple[List[List[float]], List[List[float]], List[List[float]]]:
    """Definere depoter.

    Args:
      start_kapital: Start kapital for depoterne.
      lagerbeskatning_procent: Procent for det lager beskattede depot.

    Returns:
      Fraktiler for CAGR for forskellige depot typer.
    """
    data = np.genfromtxt(f"{os.path.dirname(__file__)}/../SP500.csv", delimiter=";")
    ask: List[List[float]] = [[], [], []]
    normal: List[List[float]] = [[], [], []]
    normal_worst_case: List[List[float]] = [[], [], []]
    for j, antal_år in enumerate([20, 30, 40]):
        for start in range(0, len(data) - 950 - antal_år * 12):
            askdepot, normaldepot, normaldepot_worst_case = depoter(start_kapital, lagerbeskatning_procent)
            for i in range(start + 950, start + 950 + 12 * antal_år):
                udbytteafkast = askdepot.ETFer[0].kurs * data[i + 1, 4]
                kursafkast = askdepot.ETFer[0].kurs * data[i + 1, 3]
                askdepot.afkast_månedlig([kursafkast], [udbytteafkast])
                normaldepot.afkast_månedlig([kursafkast], [udbytteafkast])
                normaldepot_worst_case.afkast_månedlig([kursafkast], [udbytteafkast])
                if i % 12 == 0:
                    normaldepot.skatteklasse.progressionsgrænse *= 1 + 0.02
            ask[j].append(askdepot.total_salgsværdi())
            normal[j].append(normaldepot.total_salgsværdi())
            normal_worst_case[j].append(normaldepot_worst_case.total_salgsværdi())

    ask_cagr = []
    normal_cagr = []
    normal_worst_case_cagr = []
    for år, depot1, depot2, depot3 in zip([20, 30, 40], ask, normal, normal_worst_case):
        ask_cagr.append(formler.CAGR(start_kapital, np.array(depot1), år))
        normal_cagr.append(formler.CAGR(start_kapital, np.array(depot2), år))
        normal_worst_case_cagr.append(formler.CAGR(start_kapital, np.array(depot3), år))
    ask_q = []
    normal_q = []
    normal_worst_case_q = []
    for cagr1, cagr2, cagr3 in zip(ask_cagr, normal_cagr, normal_worst_case_cagr):
        q1 = []
        q2 = []
        q3 = []
        for j in range(0, 1001):
            q1.append(np.quantile(cagr1, j * 0.001))
            q2.append(np.quantile(cagr2, j * 0.001))
            q3.append(np.quantile(cagr3, j * 0.001))
        ask_q.append(q1)
        normal_q.append(q2)
        normal_worst_case_q.append(q3)
    return ask_q, normal_q, normal_worst_case_q


SIZE = 12
plt.rc("font", size=SIZE)  # controls default text sizes
plt.rc("axes", titlesize=SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=SIZE)  # fontsize of the x any y labels
plt.rc("xtick", labelsize=SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=SIZE * 0.9)  # legend fontsize
plt.rc("figure", titlesize=SIZE)  # # size of the figure title

ask_fraktil, mormal_fraktil, normal_worst_case_fraktil = kør_model(10 ** 5, 0.17)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 8), sharex=True)
for depot, navn in zip([ask_fraktil, mormal_fraktil, normal_worst_case_fraktil], ["ASK", "27%/42%", "42%"]):
    for ax, serie in zip([ax1, ax2, ax3], depot):
        ax.plot(np.linspace(0.0, 1, 1001), serie, label=navn, linewidth=3)
ax1.legend()
for ax, år_inv in zip([ax1, ax2, ax3], [20, 30, 40]):
    ax.set_xticks(np.linspace(0.0, 1.0, 11))
    ax.grid(which="minor")
    ax.grid(which="major")
    ax.set_ylabel(f"CAGR")
    ax.set_title(f"{år_inv:1.0f} år investering")
ax3.set_xlabel("Fraktil")
plt.tight_layout()
plt.savefig("ask_vs_real.svg")

aop_fraktil, mormal_fraktil, normal_worst_case_fraktil = kør_model(5300, 0.153)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 8), sharex=True)
for depot, navn in zip([aop_fraktil, mormal_fraktil, normal_worst_case_fraktil], ["AOP", "27%/42%", "42%"]):
    for ax, serie in zip([ax1, ax2, ax3], depot):
        ax.plot(np.linspace(0.0, 1, 1001), serie, label=navn, linewidth=3)
ax1.legend()
for ax, år_inv in zip([ax1, ax2, ax3], [20, 30, 40]):
    ax.set_xticks(np.linspace(0.0, 1.0, 11))
    ax.grid(which="minor")
    ax.grid(which="major")
    ax.set_ylabel(f"CAGR")
    ax.set_title(f"{år_inv:1.0f} år investering")
ax3.set_xlabel("Fraktil")
plt.tight_layout()
plt.savefig("aop_vs_real.svg")


def gennemsnit_ask_vs_real(cagr):
    """
    Regner forskellen i depot størrelse mellem et lagerbeskattet,
    og et realisationsbeskattet depot.
    Dette er baseret på en gennemsnits model for afkast.

    Args:
      cagr: CAGR

    Returns:
      Forskellen mellem lagerbeskattet og realisationsbeskattet.
    """
    s = 0.17
    q = 0.42
    y = np.linspace(0, 200, 10000)
    return (1 + cagr - cagr * s) ** y - (1 + cagr) ** y * (1 - q) - q


As = []
years = []
for m in range(20, 201):
    As.append(m / 1000)
    f = gennemsnit_ask_vs_real(m / 1000)
    years.append(len(f[f - 10 ** -12 > 0]) / 10000 * 200)
fig, ax1 = plt.subplots(1, 1, figsize=(6, 4), sharex=True)
ax1.plot(As, years, linewidth=3)
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel("År")
ax1.set_xlabel("CAGR før skat")
plt.tight_layout()
plt.savefig("ask_vs_real_gennemsnit.svg")

assert abs(ask_fraktil[0][-1] - 0.14800362792549548) < 10 ** -6
assert abs(aop_fraktil[0][-1] - 0.146246775559008) < 10 ** -6
assert abs(years[0] - 152.78) < 10 ** -6

import os
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

import dkfinance_modeller.aktieskat.depotmodel as depotmodel
import dkfinance_modeller.aktieskat.kurtage as kurtage
import dkfinance_modeller.aktieskat.skat as skat
import dkfinance_modeller.aktieskat.vaerdipapirer as værdipapirer
import dkfinance_modeller.aktieskat.valuta as valuta
import dkfinance_modeller.laan.laanmodel as laanmodel


def depoter() -> Tuple[depotmodel.DepotModel, depotmodel.DepotModel]:
    """Definere depoter.

    Returns:
      Depot med realationsbeskatning
    """
    etf1 = værdipapirer.ETF(kurs=100, åop=0.12 / 100, beskatningstype="lager")
    etf2 = værdipapirer.ETF(kurs=100, åop=0.12 / 100, beskatningstype="lager")
    skatter1 = skat.Skat(beskatningstype="aktie")
    skatter2 = skat.Skat(beskatningstype="ask")
    skatter2.skatteprocenter = [0.42]
    normal_depot = depotmodel.DepotModel(
        kapital=0.0,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44, underkonto=True),
        skatteklasse=skatter1,
        minimumskøb=1000,
        ETFer=[etf1],
        ETF_fordeling=[1.0],
        valutafunktion=valuta.saxo_underkonto_kurtage,
    )
    normal_worst_case = depotmodel.DepotModel(
        kapital=0.0,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44, underkonto=True),
        skatteklasse=skatter2,
        minimumskøb=1000,
        ETFer=[etf2],
        ETF_fordeling=[1.0],
        valutafunktion=valuta.saxo_underkonto_kurtage,
    )
    return normal_depot, normal_worst_case


data = np.genfromtxt(f"{os.path.dirname(__file__)}/../SP500.csv", delimiter=";")
normal: List[List[float]] = [[], [], [], [], [], [], [], []]
worst_case: List[List[float]] = [[], [], [], [], [], [], [], []]
for k, uddannelse_længde in enumerate([3 * 12, 5 * 12]):
    for j, rente in enumerate([1.0, 3.0, 5.0, 7.0]):
        for start in range(0, len(data) - 950 - 22 * 12):
            depot, depot_worst_case = depoter()
            tab = [0.0, 0.0]
            sulån = laanmodel.SUlån(uddannelse_længde, 16, rente)
            i = start
            for afdrag, fradrag in sulån.propager_måned():
                if depot.total_salgsværdi() >= -min(0, afdrag + fradrag) and tab[0] == 0.0:
                    if afdrag + fradrag < 0.0:
                        depot.frigør_kapital(-(afdrag + fradrag))
                    depot.kapital += afdrag + fradrag
                    kursafkast = depot.ETFer[0].kurs * (data[i + 1, 4] + data[i + 1, 3])
                    depot.afkast_månedlig([kursafkast], [0.0])
                else:
                    if tab[0] == 0.0:
                        tab[0] = depot.total_salgsværdi()
                    tab[0] += afdrag + fradrag
                if depot_worst_case.total_salgsværdi() >= -min(0, afdrag + fradrag) and tab[1] == 0.0:
                    if afdrag + fradrag < 0.0:
                        depot_worst_case.frigør_kapital(-(afdrag + fradrag))
                    depot_worst_case.kapital += afdrag + fradrag
                    kursafkast = depot_worst_case.ETFer[0].kurs * (data[i + 1, 4] + data[i + 1, 3])
                    depot_worst_case.afkast_månedlig([kursafkast], [0.0])
                else:
                    if tab[1] == 0.0:
                        tab[1] = depot_worst_case.total_salgsværdi()
                    tab[1] += afdrag + fradrag
                if i % 12 == 0:
                    depot.skatteklasse.progressionsgrænse *= 1 + 0.02
                i += 1
            if tab[0] == 0.0:
                normal[4 * k + j].append(depot.total_salgsværdi())
            else:
                normal[4 * k + j].append(tab[0])
            if tab[1] == 0.0:
                worst_case[4 * k + j].append(depot_worst_case.total_salgsværdi())
            else:
                worst_case[4 * k + j].append(tab[1])

SIZE = 12
plt.rc("font", size=SIZE)
plt.rc("axes", titlesize=SIZE)
plt.rc("axes", labelsize=SIZE)
plt.rc("xtick", labelsize=SIZE)
plt.rc("ytick", labelsize=SIZE)
plt.rc("legend", fontsize=SIZE)
plt.rc("figure", titlesize=SIZE)

normal_q = []
worst_case_q = []
for i in range(8):
    q1 = []
    q2 = []
    for j in range(0, 1001):
        q1.append(np.quantile(normal[i], j * 0.001))
        q2.append(np.quantile(worst_case[i], j * 0.001))
    normal_q.append(q1)
    worst_case_q.append(q2)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 10), sharex=True)
ax1.plot(np.linspace(0.0, 1, 1001), normal_q[0], "tab:blue", label="1%", linewidth=3)
ax1.plot(np.linspace(0.0, 1, 1001), worst_case_q[0], "tab:blue", linestyle="--", linewidth=3)
ax1.plot(np.linspace(0.0, 1, 1001), normal_q[1], "tab:orange", label="3%", linewidth=3)
ax1.plot(np.linspace(0.0, 1, 1001), worst_case_q[1], "tab:orange", linestyle="--", linewidth=3)
ax1.plot(np.linspace(0.0, 1, 1001), normal_q[2], "tab:green", label="5%", linewidth=3)
ax1.plot(np.linspace(0.0, 1, 1001), worst_case_q[2], "tab:green", linestyle="--", linewidth=3)
ax1.plot(np.linspace(0.0, 1, 1001), normal_q[3], "tab:red", label="7%", linewidth=3)
ax1.plot(np.linspace(0.0, 1, 1001), worst_case_q[3], "tab:red", linestyle="--", linewidth=3)

ax2.plot(np.linspace(0.0, 1, 1001), normal_q[4], "tab:blue", label="1%", linewidth=3)
ax2.plot(np.linspace(0.0, 1, 1001), worst_case_q[4], "tab:blue", linestyle="--", linewidth=3)
ax2.plot(np.linspace(0.0, 1, 1001), normal_q[5], "tab:orange", label="3%", linewidth=3)
ax2.plot(np.linspace(0.0, 1, 1001), worst_case_q[5], "tab:orange", linestyle="--", linewidth=3)
ax2.plot(np.linspace(0.0, 1, 1001), normal_q[6], "tab:green", label="5%", linewidth=3)
ax2.plot(np.linspace(0.0, 1, 1001), worst_case_q[6], "tab:green", linestyle="--", linewidth=3)
ax2.plot(np.linspace(0.0, 1, 1001), normal_q[7], "tab:red", label="7%", linewidth=3)
ax2.plot(np.linspace(0.0, 1, 1001), worst_case_q[7], "tab:red", linestyle="--", linewidth=3)

ax1.legend()
ax1.set_title("3 årig uddannelse")
ax2.set_title("5 årig uddannelse")
ax1.grid(which="minor")
ax1.grid(which="major")
ax2.grid(which="minor")
ax2.grid(which="major")
ax1.set_ylim(-0.6 * 10 ** 5, 2 * 10 ** 5)
ax2.set_ylim(-1.2 * 10 ** 5, 3.5 * 10 ** 5)
ax2.set_xlabel("Fraktil")
ax1.set_ylabel("Profit DKK")
ax2.set_ylabel("Profit DKK")
plt.tight_layout()
plt.savefig("sulaan_profit.svg")

assert abs(normal_q[0][-1] - 175270.11825182455) < 10 ** -2
assert abs(worst_case_q[7][-1] - 56410.6188578673) < 10 ** -2

import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

import dkfinance_modeller.aktieskat.depotmodel as depotmodel
import dkfinance_modeller.aktieskat.kurtage as kurtage
import dkfinance_modeller.aktieskat.skat as skat
import dkfinance_modeller.aktieskat.vaerdipapirer as værdipapirer
import dkfinance_modeller.simple_modeller.formler as formler


def depoter() -> depotmodel.DepotModel:
    """Definere depoter.

    Returns:
      Depot med realationsbeskatning
    """
    etf = værdipapirer.ETF(kurs=100, åop=0.55 / 100, beskatningstype="realisation")
    skatter = skat.Skat(beskatningstype="aktie")
    realisationsbeskatning = depotmodel.DepotModel(
        kapital=300000.0,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="Dkk"),
        skatteklasse=skatter,
        minimumskøb=5000,
        ETFer=[etf],
        ETF_fordeling=[1.0],
    )
    return realisationsbeskatning


data = np.genfromtxt(f"{os.path.dirname(__file__)}/../SP500.csv", delimiter=";")
real: List[List[float]] = [[], [], [], [], [], [], [], [], [], [], []]
for j, udbytte_procent in enumerate(np.linspace(0, 1, 11)):
    for start in range(0, 50 * 12):
        realisationsdepot = depoter()
        udbytte_årlig = 0.0
        kursstigning_årlig = 0.0
        for i in range(start + 950, start + 950 + 12 * 20):
            udbytteafkast = realisationsdepot.ETFer[0].kurs * data[i + 1, 4]
            kursafkast = realisationsdepot.ETFer[0].kurs * data[i + 1, 3]
            if i % 12 == 0:
                effektivt_udbytte = udbytte_årlig + max(0, udbytte_procent * kursstigning_årlig)
                realisationsdepot.afkast_månedlig(
                    [udbytteafkast + kursafkast - effektivt_udbytte], [effektivt_udbytte]
                )
                udbytte_årlig = 0.0
                kursstigning_årlig = 0.0
            else:
                realisationsdepot.afkast_månedlig([udbytteafkast + kursafkast], [0.0])
            udbytte_årlig += udbytteafkast
            kursstigning_årlig += kursafkast
        real[j].append(realisationsdepot.total_salgsværdi())
real = np.array(real)
carg = formler.CAGR(300000, real, 20)  # type: ignore

SIZE = 12
plt.rc("font", size=SIZE)  # controls default text sizes
plt.rc("axes", titlesize=SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=SIZE)  # fontsize of the x any y labels
plt.rc("xtick", labelsize=SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=SIZE * 0.9)  # legend fontsize
plt.rc("figure", titlesize=SIZE)  # # size of the figure title

fig, ax1 = plt.subplots(1, 1, figsize=(5, 6))
for k, percent in enumerate(np.linspace(0, 1, 11)):
    density = scipy.stats.gaussian_kde(carg[k, :])  # type: ignore # pylint: disable=E1126
    density.covariance_factor = lambda: 0.15
    density._compute_covariance()  # pylint: disable=W0212
    ax1.plot(
        np.linspace(0.0, 0.16, 200),
        density(np.linspace(0.0, 0.16, 200)),
        linewidth=4,
        alpha=1 - k * 0.075,
        label=f"Udbytte = {percent*100:1.0f}%",
    )
ax1.set_ylim(0, 26)
ax1.set_xlim(0.0, 0.16)
ax1.set_ylabel("Arbitrær værdi")
ax1.set_xlabel("CAGR")
plt.legend()
plt.tight_layout()
plt.savefig("distributioner.svg")


q: List[List[float]] = [[], [], [], [], [], [], [], [], [], [], []]
for i in range(0, 21):
    for k in range(0, 11):
        q[k].append(np.quantile(carg[k, :], i * 0.05))  # type: ignore

fig, ax1 = plt.subplots(1, 1, figsize=(5, 6))
for k, percent in enumerate(np.linspace(0, 1, 11)):
    ax1.plot(np.linspace(0.0, 1, 21), q[k], label=f"Udbytte = {percent*100:1.0f}%", linewidth=3)
plt.legend()
ax1.set_xticks(np.linspace(0.0, 1.0, 11))
ax1.set_ylim(0.02, 0.14)
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel("CAGR")
ax1.set_xlabel("Fraktil")
plt.tight_layout()
plt.savefig("fraktiler.svg")

assert abs(q[0][-1] - 0.13724085145511444) < 10 ** -5
assert abs(q[1][-1] - 0.13458672458687504) < 10 ** -5
assert abs(q[2][-1] - 0.1318599365285087) < 10 ** -5
assert abs(q[3][-1] - 0.1290045325344671) < 10 ** -5
assert abs(q[4][-1] - 0.12624837675279044) < 10 ** -5
assert abs(q[5][-1] - 0.12348408205700934) < 10 ** -5
assert abs(q[6][-1] - 0.1206727361782085) < 10 ** -5
assert abs(q[7][-1] - 0.11815582092659183) < 10 ** -5
assert abs(q[8][-1] - 0.11569339680896817) < 10 ** -5
assert abs(q[9][-1] - 0.11329800951566482) < 10 ** -5
assert abs(q[10][-1] - 0.1109811982940192) < 10 ** -5

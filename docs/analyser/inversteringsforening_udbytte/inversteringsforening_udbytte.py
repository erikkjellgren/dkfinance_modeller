import os
from typing import List

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

import dkfinance_modeller.aktieskat.depotmodel as depotmodel
import dkfinance_modeller.aktieskat.kurtage as kurtage
import dkfinance_modeller.aktieskat.skat as skat
import dkfinance_modeller.aktieskat.vaerdipapirer as værdipapirer


def depoter() -> depotmodel.DepotModel:
    """Definere depoter.

    Returns:
      Depot med realationsbeskatning
    """
    etf = værdipapirer.ETF(kurs=100, åop=0.55 / 100)
    realisationsbeskatning = depotmodel.DepotModel(
        kapital=300000.0,
        kurtagefunktion=kurtage.saxo_kurtage_bygger(valuta="Dkk"),
        skattefunktion=skat.aktiebeskatning,
        minimumskøb=5000,
        beskatningstype="realisation",
        ETFer=[etf],
        ETF_fordeling=[1.0],
    )
    return realisationsbeskatning


data = np.genfromtxt(f"{os.path.dirname(__file__)}/../SP500.csv", delimiter=";")
real: List[List[float]] = [[], [], [], [], [], [], [], [], [], [], []]
for j, udbytte_procent in enumerate(np.linspace(0, 1, 11)):
    for start in range(0, 50 * 12):
        realisationsdepot = depoter()
        udbytte = 0.0
        for i in range(start + 950, start + 950 + 12 * 20):
            realisationafkast = realisationsdepot.ETFer[0].kurs * (data[i + 1, 5] - 1)
            if i % 12 == 0 and udbytte > 0.0:
                realisationsdepot.afkast_månedlig([realisationafkast - udbytte], [udbytte])
                udbytte = 0.0
            elif i % 12 == 0:
                realisationsdepot.afkast_månedlig([realisationafkast], [0.0])
                udbytte = 0.0
            else:
                realisationsdepot.afkast_månedlig([realisationafkast], [0.0])
            udbytte += udbytte_procent * realisationafkast
        real[j].append(realisationsdepot.total_salgsværdi())
real = np.array(real)

SizeX = 6
SizeY = 5
SIZE = 12
plt.rc("font", size=SIZE)  # controls default text sizes
plt.rc("axes", titlesize=SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=SIZE)  # fontsize of the x any y labels
plt.rc("xtick", labelsize=SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=SIZE * 0.9)  # legend fontsize
plt.rc("figure", titlesize=SIZE)  # # size of the figure title

fig, ax1 = plt.subplots(1, 1, figsize=(SizeX, SizeY))
for k, percent in enumerate(np.linspace(0, 1, 11)):
    density = scipy.stats.gaussian_kde(real[k, :])  # type: ignore # pylint: disable=E1126
    density.covariance_factor = lambda: 0.15
    density._compute_covariance()  # pylint: disable=W0212
    ax1.plot(
        np.linspace(10 ** 5, 10 ** 6.7, 200),
        density(np.linspace(10 ** 5, 10 ** 6.7, 200)),
        linewidth=4,
        alpha=1 - k * 0.075,
        label=f"Udbytte = {percent*100:1.0f}%",
    )
ax1.set_ylim(0, 2 * 10 ** -6)
ax1.set_xlim(10 ** 5, 10 ** 6.7)
ax1.set_ylabel("Arbitrær værdi")
ax1.set_xlabel("Depot salgsværdi [DKK]")
plt.legend()
plt.tight_layout()
plt.savefig("distributioner.svg")


q: List[List[float]] = [[], [], [], [], [], [], [], [], [], [], []]
for i in range(0, 21):
    for k in range(0, 11):
        q[k].append(np.quantile(real[k, :], i * 0.05))  # type: ignore

fig, ax1 = plt.subplots(1, 1, figsize=(SizeX, SizeY))
for k, percent in enumerate(np.linspace(0, 1, 11)):
    ax1.plot(np.linspace(0.0, 1, 21), q[k], label=f"Udbytte = {percent*100:1.0f}%", linewidth=3)
plt.legend()
ax1.set_xticks(np.linspace(0.0, 1.0, 11))
ax1.set_yscale("log")
ax1.set_yticks([], minor=True)
ax1.set_yticks(np.logspace(5.7, 6.8, 8))
ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax1.set_ylim(10 ** 5.65, 10 ** 6.7)
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.set_ylabel("Depot salgsværdi [DKK]")
ax1.set_xlabel("Fraktil")
plt.tight_layout()
plt.savefig("fraktiler.svg")

Q = np.array(q)
assert abs(Q[0, -1] - 4329082.05425461) < 10 ** -5
assert abs(Q[1, -1] - 4183317.339325505) < 10 ** -5
assert abs(Q[2, -1] - 3991460.3806166155) < 10 ** -5
assert abs(Q[3, -1] - 3773356.1970679183) < 10 ** -5
assert abs(Q[4, -1] - 3547351.3249716433) < 10 ** -5
assert abs(Q[5, -1] - 3336763.6602458763) < 10 ** -5
assert abs(Q[6, -1] - 3143758.647937869) < 10 ** -5
assert abs(Q[7, -1] - 2962879.7267771782) < 10 ** -5
assert abs(Q[8, -1] - 2796463.5459343432) < 10 ** -5
assert abs(Q[9, -1] - 2640784.525736788) < 10 ** -5
assert abs(Q[10, -1] - 2499040.3567459085) < 10 ** -5

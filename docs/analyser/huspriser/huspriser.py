import os

import matplotlib.pyplot as plt
import numpy as np

import dkfinance_modeller.utility.formler as formler

huspris = np.genfromtxt(f"{os.path.dirname(__file__)}/huspriser_danmark.txt")
huspris_indeks = huspris / huspris[0]

labels = np.genfromtxt(f"{os.path.dirname(__file__)}/labels.txt", dtype=str, delimiter=",")

diskonto = np.genfromtxt(f"{os.path.dirname(__file__)}/diskonto.txt", delimiter=",")
diskonto_min = np.zeros(len(diskonto))
mindste = 10
for i, rente in enumerate(diskonto):
    mindste = min(mindste, rente)
    diskonto_min[i] = mindste

lønstigning = np.genfromtxt(f"{os.path.dirname(__file__)}/loenstigning.txt")
lønstigning = (1 + lønstigning / 100) ** (3 / 12) - 1
løn_indeks = [1]
for stigning in lønstigning[1:]:
    løn_indeks.append(løn_indeks[-1] * (1 + stigning))

husomkostninger = []
husomkostninger_min = []
for rente, rente_min, pris in zip(diskonto, diskonto_min, huspris):
    husomkostninger.append(
        formler.afbetalling(klån=pris * 0.8, n=30, r=rente / 100 + 10 ** -6) * 30 + 0.2 * pris
    )
    husomkostninger_min.append(
        formler.afbetalling(klån=pris * 0.8, n=30, r=rente_min / 100 + 10 ** -6) * 30 + 0.2 * pris
    )
husomkostninger_indeks = husomkostninger / husomkostninger[0]
husomkostninger_min_indeks = husomkostninger_min / husomkostninger_min[0]

plt.rc("font", size=10)
plt.rc("axes", titlesize=10)
plt.rc("axes", labelsize=10)
plt.rc("xtick", labelsize=10)
plt.rc("ytick", labelsize=10)
plt.rc("legend", fontsize=10)
plt.rc("figure", titlesize=10)

fig, (ax2, ax1) = plt.subplots(2, 1, figsize=(5.5, 7), sharex=True)
ax1.plot(labels, husomkostninger_min_indeks, "r--", label="Huskøbsomkostninger indeks (minimum diskonto)")
ax1.plot(labels, husomkostninger_indeks, "k-", label="Huskøbsomkostninger indeks")
ax1.plot(labels, huspris_indeks, "m-", label="Huspris indeks")
ax1.plot(labels, løn_indeks, "g-", label="Løn indeks")
ax1.legend(frameon=False)

ax2.plot(labels, diskonto_min, "r--", label="Diskonto minimum")
ax2.plot(labels, diskonto, "k--", label="Diskonto")
ax2.set_ylim(-0.2, 5.5)
ax2.set_ylabel("Diskonto")
ax2.legend(frameon=False)

for i, tick in enumerate(ax1.get_xticklabels()):
    tick.set_rotation(90)
    if i % 4 != 0:
        tick.set_fontsize(0)
        tick.set_color("white")

ax1.set_xlim(-1, len(labels) + 1)
ax1.set_ylim(0.9, 4.0)
ax1.set_ylabel("Indeks værdi")
plt.tight_layout()
plt.savefig("indekser.svg")

huspris = np.genfromtxt(f"{os.path.dirname(__file__)}/huspriser_danmark.txt")
københavn = np.genfromtxt(f"{os.path.dirname(__file__)}/huspriser_koebenhavn.txt")
odense = np.genfromtxt(f"{os.path.dirname(__file__)}/huspriser_odense.txt")
aarhus = np.genfromtxt(f"{os.path.dirname(__file__)}/huspriser_aarhus.txt")
aalborg = np.genfromtxt(f"{os.path.dirname(__file__)}/huspriser_aalborg.txt")
langeland = np.genfromtxt(f"{os.path.dirname(__file__)}/huspriser_langeland.txt")
lolland = np.genfromtxt(f"{os.path.dirname(__file__)}/huspriser_lolland.txt")
fig, ax1 = plt.subplots(1, 1, figsize=(5.5, 4), sharex=True)
ax1.plot(labels, huspris_indeks, "m-", label="Danmark indeks")
ax1.plot(labels, københavn / københavn[0], "k--", label="København indeks")
ax1.plot(labels, odense / odense[0], "b--", label="Odense indeks")
ax1.plot(labels, aarhus / aarhus[0], "g--", label="Aarhus indeks")
ax1.plot(labels, aalborg / aalborg[0], "r--", label="Aalborg indeks")
ax1.plot(labels, langeland / langeland[0], "c--", label="Langeland indeks")
ax1.plot(labels, lolland / lolland[0], "y--", label="Lolland indeks")
ax1.legend(frameon=False)

for i, tick in enumerate(ax1.get_xticklabels()):
    tick.set_rotation(90)
    if i % 4 != 0:
        tick.set_fontsize(0)
        tick.set_color("white")

ax1.set_xlim(-1, len(labels) + 1)
ax1.set_ylim(0.8, 8)
ax1.set_ylabel("Indeks værdi")
plt.tight_layout()
plt.savefig("geografiske_forskelle.svg")


relativ_huspris = []
for rente in np.linspace(0, 10, 1000):
    relativ_huspris.append(
        (formler.afbetalling(klån=1, n=30, r=rente / 100 + 10 ** -6) * 30 * 0.8 + 0.2) ** (-1)
    )

fig, ax1 = plt.subplots(1, 1, figsize=(5.5, 4))
ax1.plot(np.linspace(0, 10, 1000), relativ_huspris, linewidth=4)
ax1.set_ylabel("Relativ Huspris")
ax1.set_xlabel("Rente %")
ax1.grid(which="minor")
ax1.grid(which="major")
plt.tight_layout()
plt.savefig("huspris_rente_funktion.svg")

assert abs(husomkostninger_indeks[20] - 1.2570706075051732) < 10 ** -4

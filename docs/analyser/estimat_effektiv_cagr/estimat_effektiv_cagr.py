import matplotlib.pyplot as plt
import numpy as np


def effektiv_cagr_realisation(cagr: float, skatteprocent: float, åop: float, år: int) -> float:
    """Udregn CAGR efter skat og ÅOP for et realisationsbeskattet depot.

    Args:
      cagr: CAGR før skat og ÅOP.
      skatteprocent: Skatteprocent.
      åop: ÅOP.
      år: Antal år.

    Returns:
      Effektiv CAGR efter skat og ÅOP.
    """
    return ((1 - skatteprocent) * (1 + cagr - åop) ** år + skatteprocent) ** (1 / år) - 1


def effektiv_cagr_lager(cagr: float, skatteprocent: float, åop: float) -> float:
    """Udregn CAGR efter skat og ÅOP for et lagerbeskattet depot.

    Args:
      cagr: CAGR før skat og ÅOP.
      skatteprocent: Skatteprocent.
      åop: ÅOP.
      år: Antal år.

    Returns:
      Effektiv CAGR efter skat og ÅOP.
    """
    return (cagr - åop) * (1 - skatteprocent)


plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

q = np.linspace(0, 1, 1000)

fig, ax1 = plt.subplots(1, 1, figsize=(6, 6))
ax1.plot([0.27, 0.27], [0.0, 0.07], "k--")
ax1.plot([0.42, 0.42], [0.0, 0.07], "k--")
for antal_år in range(10, 60, 10):
    real = effektiv_cagr_realisation(7 / 100, q, 0.12 / 100, antal_år)
    ax1.plot(q, real, label=f"real, {antal_år} år", linewidth=3)
lager = effektiv_cagr_lager(7 / 100, q, 0.12 / 100)
ax1.plot(q, lager, label=f"lager", linewidth=3)
ax1.set_xlabel(r"$q_\mathrm{effektiv}$")
ax1.set_ylabel(r"$\mathrm{CAGR}_\mathrm{effektiv}$")
ax1.set_title("CAGR 7%")
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.legend()
plt.tight_layout()
plt.savefig("cagr7.svg")

fig, ax1 = plt.subplots(1, 1, figsize=(6, 6))
ax1.plot([0.27, 0.27], [0.0, 0.15], "k--")
ax1.plot([0.42, 0.42], [0.0, 0.15], "k--")
for antal_år in range(10, 60, 10):
    real = effektiv_cagr_realisation(15 / 100, q, 0.12 / 100, antal_år)
    ax1.plot(q, real, label=f"real, {antal_år} år", linewidth=3)
lager = effektiv_cagr_lager(15 / 100, q, 0.12 / 100)
ax1.plot(q, lager, label=f"lager", linewidth=3)
ax1.set_xlabel(r"$q_\mathrm{effektiv}$")
ax1.set_ylabel(r"$\mathrm{CAGR}_\mathrm{effektiv}$")
ax1.set_title("CAGR 15%")
ax1.grid(which="minor")
ax1.grid(which="major")
ax1.legend()
plt.tight_layout()
plt.savefig("cagr15.svg")

assert abs(effektiv_cagr_realisation(7 / 100, 42 / 100, 0.12 / 100, 10) - 0.044679732098822145) < 10 ** -6
assert abs(effektiv_cagr_lager(7 / 100, 42 / 100, 0.12 / 100) - 0.039904) < 10 ** -6

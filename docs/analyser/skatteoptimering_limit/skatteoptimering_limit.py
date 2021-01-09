import matplotlib.pyplot as plt
import numpy as np


def y(q: float, m: float, a_bar: float) -> float:
    """Udregn øvregrænse for hvornår skatteoptimering kan betale sig.

    Args:
       q: Øvre skattesats for aktiebeskatning.
       m: Skattesats for realiseret situation.
       a_bar: Middel årligt afkast.

    Returns:
      Antal år hvor efter skatteoptimering ikke kan betale sig.
    """
    return np.log(q * m / (1 - q - m + q * m)) / np.log(1 + a_bar)


x = np.linspace(0.04, 0.14, 1000)
f = np.zeros(np.shape(x))

for i, xi in enumerate(x):
    f[i] = y(0.42, 0.73, xi)

plt.rc("font", size=12)
plt.rc("axes", titlesize=12)
plt.rc("axes", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.rc("ytick", labelsize=12)
plt.rc("legend", fontsize=12)
plt.rc("figure", titlesize=12)

fig, ax1 = plt.subplots(1, 1, figsize=(5, 5))
ax1.plot(x, f, linewidth=3)
ax1.set_ylim(0, 20)
ax1.set_xlim(0.035, 0.145)
ax1.set_ylabel("År")
ax1.set_xlabel(r"$\bar{a}$")
ax1.grid(which="minor")
ax1.grid(which="major")
plt.tight_layout()
plt.savefig("oevregraense_skatteoptimering.svg")

assert abs(f[0] - 17.129958352753754) < 10 ** -6

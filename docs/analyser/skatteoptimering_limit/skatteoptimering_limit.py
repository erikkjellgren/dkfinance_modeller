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

SIZE = 12
plt.rc("font", size=SIZE)  # controls default text sizes
plt.rc("axes", titlesize=SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=SIZE)  # fontsize of the x any y labels
plt.rc("xtick", labelsize=SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=SIZE * 0.9)  # legend fontsize
plt.rc("figure", titlesize=SIZE)  # # size of the figure title

fig, ax1 = plt.subplots(1, 1, figsize=(5, 5))
ax1.plot(x, f)
ax1.set_ylim(0, 20)
ax1.set_xlim(0.035, 0.145)
ax1.set_ylabel("År")
ax1.set_xlabel(r"$\bar{a}$")
plt.tight_layout()
plt.savefig("oevregraense_skatteoptimering.svg")

assert abs(f[0] - 17.129958352753754) < 10 ** -6

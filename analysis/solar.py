from labtool_ex2 import Project
from sympy import exp, pi, sqrt, Abs, pi
import numpy as np

# from numpy.typing import NDArray
import pandas as pd
import matplotlib.pyplot as plt  # noqa
import os
from uncertainties import ufloat

# pyright: reportUnboundVariable=false
# pyright: reportUndefinedVariable=false


def Voltmeter(V):
    return V * 0.0015 + 0.002


def Amperemeter(current):
    return current * 0.01 + 0.003


def createStromSpannungsKennlinie(P: Project, file: str):
    P.figure.clear()
    P.figure.set_size_inches((10, 6))
    P.data = pd.DataFrame(None)
    axs = P.figure.subplots(1, 2)
    ax = axs[0]

    filepath = os.path.join(os.path.dirname(__file__), file)
    P.load_data(filepath, loadnew=True)
    P.vload()
    P.data["dU"] = U.data.apply(Voltmeter)
    P.data["dI"] = I.data.apply(Amperemeter)

    P.vload()

    P.plot(
        ax,
        U,
        I,
        label="Gemessene Daten",
        style="#1cb2f5",
        errors=True,
        marker="o",
        markersize=4,
        markeredgecolor="#1cb2f5",
        markerfacecolor="#1cb2f5",
    )

    power = U * I
    P.resolve(power)
    maxpower = max(power.data)
    pmask = P.data["power"] == maxpower
    umask = P.data["U"] == 0
    imask = P.data["I"] == 0
    maxpower = P.data[pmask]
    kurzSchlussStrom = P.data[umask]
    leerLaufSpannung = P.data[imask]
    ax.plot(
        kurzSchlussStrom.U,
        kurzSchlussStrom.I,
        marker="o",
        markersize=4,
        markeredgecolor="orange",
        markerfacecolor="orange",
        label="Kurzschlussstrom",
        color="None",
    )
    ax.plot(
        leerLaufSpannung.U,
        leerLaufSpannung.I,
        marker="v",
        markersize=4,
        markeredgecolor="blue",
        markerfacecolor="blue",
        label="Leerlaufspannung",
        color="None",
    )
    ax.plot(
        maxpower.U,
        maxpower.I,
        marker="D",
        markersize=4,
        markeredgecolor="red",
        markerfacecolor="red",
        label="MPP",
        color="None",
    )
    ax.legend()
    ax.set_title("Strom-Spannungs-Kennlinie")
    ax = axs[1]
    P.plot(
        ax,
        U,
        power,
        label="Gemessene Daten",
        style="#1cb2f5",
        errors=True,
        marker="o",
        markersize=4,
        markeredgecolor="#1cb2f5",
        markerfacecolor="#1cb2f5",
    )
    ax.plot(
        maxpower.U,
        maxpower.power,
        marker="D",
        markersize=4,
        markeredgecolor="red",
        markerfacecolor="red",
        label="MPP",
        color="None",
    )
    P.data = P.data.u.com
    maxpower = P.data[pmask]
    kurzSchlussStrom = P.data[umask]
    leerLaufSpannung = P.data[imask]
    kv = {
        "pmax": maxpower.power.values[0],
        "umax": maxpower.U.values[0],
        "imax": maxpower.I.values[0],
        "UL": leerLaufSpannung.U.values[0],
        "Ik": kurzSchlussStrom.I.values[0],
    }
    print(kv)
    P.add_text(ax, keyvalue=kv, offset=[20, -10], color="#A6F")
    ax.legend()
    ax.set_title("Leistungkennlinie")
    return ax


def test_solar_protokoll():
    gm = {
        "U": r"U",
        "UL": r"U_L",
        "I": r"I",
        "Ik": r"I_k",
        "DT": r"\Delta T",
        "t": r"t",
        "power": r"P",
        "pmax": r"P_\text{MPP}",
        "umax": r"U_\text{MPP}",
        "imax": r"I_\text{MPP}",
        "eta": r"\eta",
        "eps": r"\epsilon",
    }
    gv = {
        "U": r"\si{\volt}",
        "UL": r"\si{\volt}",
        "I": r"\si{\milli\ampere}",
        "Ik": r"\si{\milli\ampere}",
        "t": r"\si{\second}",
        "power": r"\si{\milli\watt}",
        "pmax": r"\si{\milli\watt}",
        "umax": r"\si{\volt}",
        "imax": r"\si{\milli\ampere}",
        "DT": r"\si{\kelvin}",
        "eta": r"1",
        "eps": r"1",
    }

    pd.set_option("display.max_columns", None)
    plt.rcParams["axes.axisbelow"] = True
    P = Project("Solar", global_variables=gv, global_mapping=gm, font=13)
    P.output_dir = "./"
    P.figure.set_size_inches((8, 6))
    ax: plt.Axes = P.figure.add_subplot()
    schieflagedersolarzellen = ufloat(5, 1)  # grad
    quellenAbstand = ufloat(284, 2)  # mm ist Abstand bis Lampenglas

    # Aufgabe 1
    ax = createStromSpannungsKennlinie(P, "../data/solarSerieOhneAbdeckung.csv")
    P.figure.suptitle("Serienschaltung von Solarzellen")
    P.figure.tight_layout()
    # P.ax_legend_all(loc=0)
    ax = P.savefig("serienschaltung.pdf")

    # Aufgabe 2
    ax = createStromSpannungsKennlinie(P, "../data/solarParallelOhneAbdeckung.csv")
    P.figure.suptitle("Parallelschaltung von Solarzellen")
    P.figure.tight_layout()
    # P.ax_legend_all(loc=0)
    ax = P.savefig("parallelschaltung.pdf")

    # Aufgabe 3
    ax = createStromSpannungsKennlinie(P, "../data/solarSerieMitAbdeckung.csv")
    P.figure.suptitle("Serienschaltung von Solarzellen abgedeckt")
    P.figure.tight_layout()
    # P.ax_legend_all(loc=0)
    ax = P.savefig("serienschaltungAbgedeckt.pdf")

    # Aufgabe 4
    solarzelleFlaeche = ufloat(2 * 4, 0)
    duchrmesserPower = ufloat(1.5, 0)

    # Aufgabe 5
    hellwattlampe = ufloat(0.63, 0.01)
    hellwattlampe2 = ufloat(3.4, 0.1)
    hellwattled = ufloat(0.264, 0.003)
    # Thomas Monet


if __name__ == "__main__":
    test_solar_protokoll()

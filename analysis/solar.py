from labtool_ex2 import Project
from sympy import exp, pi, sqrt, Abs, conjugate, pi, acos, asin, atan
import numpy as np
from numpy.typing import NDArray
import pandas as pd
import matplotlib.pyplot as plt  # noqa
import os
from uncertainties import ufloat

# pyright: reportUnboundVariable=false
# pyright: reportUndefinedVariable=false


def Voltmeter(V):
    return V * 0.0015 + 0.002


def Amperemeter(I):
    return I * 0.01 + 0.003


def createStromSpannungsKennlinie(P: Project, file: str):
    filepath = os.path.join(
        os.path.dirname(__file__), "../data/solarSerieOhneAbdeckung.csv"
    )
    P.load_data(filepath, loadnew=True)
    P.vload()
    P.data["dU"] = U.data.apply(Amperemeter)
    P.data["dI"] = I.data.apply(Voltmeter)

    P.figure.set_size_inches((8, 6))
    ax: plt.Axes = P.figure.add_subplot()
    print(I.data)
    print(U.data)

    P.plot_data(
        ax,
        U,
        I,
        label="Gemessene Daten",
        style="#1cb2f5",
        errors=True,
    )

    # power = U * I
    # P.resolve(power)
    # maxpower = max(power.data)
    # maxpower = P.data[P.data["power"] == maxpower]
    # kurzSchlussStrom = P.data[P.data["U"] == 0]
    # leerLaufSpannung = P.data[P.data["I"] == 0]
    # ax.plot(
    #     kurzSchlussStrom.U,
    #     kurzSchlussStrom.I,
    #     marker="o",
    #     markersize=20,
    #     markeredgecolor="red",
    #     markerfacecolor="red",
    #     label="Kurzschlussstrom",
    # )
    # ax.plot(
    #     leerLaufSpannung.U,
    #     leerLaufSpannung.I,
    #     marker="o",
    #     markersize=20,
    #     markeredgecolor="red",
    #     markerfacecolor="red",
    #     label="Leerlaufspannung",
    # )
    # ax.plot(
    #     maxpower.U,
    #     maxpower.I,
    #     marker="o",
    #     markersize=20,
    #     markeredgecolor="red",
    #     markerfacecolor="red",
    #     label="MPP",
    # )

    ax.set_title("Serienschaltung")
    P.ax_legend_all(loc=4)
    ax = P.savefig("serienschaltung.pdf")


def test_solar_protokoll():
    gm = {
        "U": r"U",
        "UL": r"U_L",
        "I": r"I",
        "Ik": r"I_k",
        "DT": r"\Delta T",
        "t": r"t",
        "power": r"P",
        "eta": r"\eta",
        "eps": r"\epsilon",
    }
    gv = {
        "U": r"\si{\volt}",
        "UL": r"U_L",
        "I": r"\si{\milli\ampere}",
        "Ik": r"I_k",
        "t": r"\si{\second}",
        "power": r"\si{\watt}",
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
    # createStromSpannungsKennlinie(P, "../data/solarSerieOhneAbdeckung.csv")
    filepath = os.path.join(
        os.path.dirname(__file__), "../data/solarSerieOhneAbdeckung.csv"
    )
    P.load_data(filepath, loadnew=True)

    flaechesolarzelle = ufloat(10 * 8, 1)
    bagedeagtflaechesolarzelle = ufloat(10 * 7, 1)

    P.plot_data(
        ax,
        U,
        I,
        label="Gemessene Daten",
        style="#1cb2f5",
        errors=True,
    )

    ax.set_title(f"Serienschaltung")
    P.ax_legend_all(loc=4)
    ax = P.savefig(f"serienschaltung.pdf")

    # Aufgabe 2
    filepath = os.path.join(
        os.path.dirname(__file__), "../data/solarParallelOhneAbdeckung.csv"
    )
    P.load_data(filepath, loadnew=True)

    # Aufgabe 3
    filepath = os.path.join(
        os.path.dirname(__file__), "../data/solarSerieMitAbdeckung.csv"
    )
    P.load_data(filepath, loadnew=True)

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

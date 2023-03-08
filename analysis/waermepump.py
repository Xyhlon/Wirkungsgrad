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


def Thermometer(T):
    return T * 0 + 0.1


def test_waermepumpe_protokoll():
    gm = {
        "pk": r"p_k",
        "pw": r"p_w",
        "Tw": r"T_k",
        "Tk": r"T_w",
        "DT": r"\Delta T",
        "t": r"t",
        "eta": r"\eta",
        "eps": r"\epsilon",
    }
    gv = {
        "pk": r"\si{\bar}",
        "pw": r"\si{\bar}",
        "Tw": r"\si{\degreeCelsius}",
        "Tk": r"\si{\degreeCelsius}",
        "t": r"\si{\second}",
        "DT": r"\si{\kelvin}",
        "eta": r"1",
        "eps": r"1",
    }

    pd.set_option("display.max_columns", None)
    plt.rcParams["axes.axisbelow"] = True
    P = Project("Waermepumpe", global_variables=gv, global_mapping=gm, font=13)
    P.output_dir = "./"
    P.figure.set_size_inches((8, 6))
    ax: plt.Axes = P.figure.add_subplot()
    kuebelvolumen = ufloat(4000, 20)
    leistungKompressor = ufloat(118, 2)

    # Aufgabe 3
    filepath = os.path.join(os.path.dirname(__file__), "../data/waermeDruck.csv")
    P.load_data(filepath, loadnew=True)


if __name__ == "__main__":
    test_waermepumpe_protokoll()

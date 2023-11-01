import os
from itertools import cycle

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import rcParams

from hplot.config import default_cfg
from hplot.utils import cm2inch


class PloterBox:
    def __init__(
        self,
        data,
        fname=None,
        *,
        width=0.5,
        linewidth=1.0,
        xlabel=None,
        ylabel=None,
        display=True,
        fig_size=None,
        usetex=False,
        dpi=None,
        pad=None,
        theme=None,
        tick_size=None,
        tick_label_font=None,
        legend_font_dict=None,
        label_font_dict=None,
    ) -> None:
        self.data = data
        self.fname = fname
        self.width = width
        self.linewidth = linewidth
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.display = display
        self.fig_size = fig_size
        self.dpi = dpi
        self.pad = pad
        self.theme = theme
        self.usetex = usetex
        self.tick_size = tick_size
        self.tick_label_font = tick_label_font
        self.legend_font_dict = legend_font_dict
        self.label_font_dict = label_font_dict
        plt.cla()
        plt.clf()
        plt.close()
        self.ax = None
        self.fig = None
        self.__preprocess()

    def __preprocess(self):
        rcParams.update({"mathtext.fontset": "stix"})
        assert isinstance(self.data, (dict, list, tuple))

        if isinstance(self.data, dict):
            self.data = [self.data]
        self.num_data = len(self.data)

        if self.fig_size is None:
            self.fig_size = default_cfg.fig_size
        if self.dpi is None:
            self.dpi = default_cfg.dpi
        if self.pad is None:
            self.pad = default_cfg.pad
        if self.tick_size is None:
            self.tick_size = default_cfg.tick_size
        if self.tick_label_font is None:
            self.tick_label_font = default_cfg.tick_label_font
        if self.legend_font_dict is None:
            self.legend_font_dict = default_cfg.legend_font
        if self.label_font_dict is None:
            self.label_font_dict = default_cfg.label_font

        # use tex to render fonts, tex install required
        if self.usetex:
            from matplotlib import rc

            rc("font", **{"family": "serif", "serif": ["Times New Roman"]})
            rc("text", usetex=True)

    def plot(self):
        if self.theme is not None:
            sns.set_theme(style=self.theme)
        self.fig, self.ax = plt.subplots(figsize=cm2inch(*self.fig_size), dpi=self.dpi)

        data_dict = dict()

        for subdata in self.data:
            data_dict[subdata["label"]] = subdata["y"]

        df = pd.DataFrame(data_dict)
        sns.boxplot(data=df, width=self.width, linewidth=self.linewidth)

        # tick
        plt.tick_params(labelsize=self.tick_size)
        labels = self.ax.get_xticklabels() + self.ax.get_yticklabels()
        [label.set_fontname(self.tick_label_font) for label in labels]

        # label
        if self.xlabel is not None:
            plt.xlabel(self.xlabel, fontdict=self.label_font_dict)
        if self.ylabel is not None:
            plt.ylabel(self.ylabel, fontdict=self.label_font_dict)

    def save(self):
        plt.tight_layout(pad=self.pad)
        if self.fname is None:
            pass
        else:
            dir_path = os.path.dirname(self.fname)
            os.makedirs(dir_path, exist_ok=True)
            plt.savefig(self.fname)

    def show(self):
        self.fig.set_tight_layout(True)
        plt.tight_layout(pad=self.pad)
        plt.show()

    def close(self):
        sns.set_theme(style="white")
        plt.close()


def plot_box(
    data,
    fname=None,
    *,
    width=0.5,
    linewidth=1.0,
    xlabel=None,
    ylabel=None,
    display=True,
    fig_size=None,
    usetex=False,
    dpi=None,
    pad=None,
    theme=None,
    tick_size=None,
    tick_label_font=None,
    legend_font_dict=None,
    label_font_dict=None,
    **kwargs,
):
    """

    Args:
        data (list of dict): each dict with keys "label" and "y"
        fname (str, optional): figure save path. Defaults to None.
        width (float, optional): width of each box. Defaults to 0.5.
        linewidth (float, optional): linewidth of box boundary. Defaults to 1.0.
        theme (str, optional): theme of seaborn. Defaults to None. darkgrid, whitegrid, dark, white, ticks
    """
    ploter = PloterBox(
        data,
        fname=fname,
        width=width,
        linewidth=linewidth,
        xlabel=xlabel,
        ylabel=ylabel,
        display=display,
        fig_size=fig_size,
        usetex=usetex,
        dpi=dpi,
        pad=pad,
        theme=theme,
        tick_size=tick_size,
        tick_label_font=tick_label_font,
        legend_font_dict=legend_font_dict,
        label_font_dict=label_font_dict,
        **kwargs,
    )

    ploter.plot()

    if fname is not None:
        ploter.save()
    if display:
        ploter.show()
    ploter.close()

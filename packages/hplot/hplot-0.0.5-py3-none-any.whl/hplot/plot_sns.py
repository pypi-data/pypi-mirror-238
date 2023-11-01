import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import rcParams

from hplot.config import default_cfg
from hplot.utils import cm2inch


class PloterSns:
    def __init__(
        self,
        data,
        fname,
        *,
        xlabel=None,
        ylabel=None,
        legend=None,
        ncol=None,
        legend_loc="best",
        legend_frameon=False,
        xlim=None,
        ylim=None,
        xticks=None,
        yticks=None,
        xtick_labels=None,
        ytick_labels=None,
        usetex=False,
        display=False,
        fig_size=None,
        dpi=None,
        pad=None,
        tick_size=None,
        tick_label_font=None,
        legend_font_dict=None,
        label_font_dict=None,
        style="white",
        ticklabel_style=None,
        show_legend=True,
    ):
        self.data = data
        self.fname = fname
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.legend = legend
        self.legend_loc = legend_loc
        self.legend_frameon = legend_frameon
        self.xlim = xlim
        self.ylim = ylim
        self.xticks = xticks
        self.yticks = yticks
        self.xtick_labels = xtick_labels
        self.ytick_labels = ytick_labels
        self.usetex = usetex
        self.ncol = ncol
        self.display = display
        self.fig_size = fig_size
        self.dpi = dpi
        self.pad = pad
        self.tick_size = tick_size
        self.tick_label_font = tick_label_font
        self.legend_font_dict = legend_font_dict
        self.label_font_dict = label_font_dict
        self.ticklabel_style = ticklabel_style
        self.show_legend = show_legend
        plt.cla()
        plt.clf()
        plt.close()
        self.num_data = None
        self.fig = None
        self.ax = None
        sns.set_style(style)
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

    def _ppc_data(self, d):
        x = d["x"]
        y = d["y"]
        label = d["label"]
        if isinstance(x, np.ndarray):
            x = [x]
        if isinstance(y, np.ndarray):
            y = [y]

        assert len(x) == len(y)

        for i in range(len(x)):
            x[i] = x[i].reshape(-1)
            y[i] = y[i].reshape(-1)
            assert x[i].shape == y[i].shape
        x = np.stack(x)
        y = np.stack(y)

        x = x.reshape(-1)
        y = y.reshape(-1)
        return x, y, label

    def plot(self):
        self.fig, self.ax = plt.subplots(figsize=cm2inch(*self.fig_size), dpi=self.dpi)
        # plot figure
        for i, d in enumerate(self.data):
            x, y, label = self._ppc_data(d)
            sns.lineplot(x=x, y=y, label=label)

        # tick
        plt.tick_params(labelsize=self.tick_size)
        labels = self.ax.get_xticklabels() + self.ax.get_yticklabels()
        [label.set_fontname(self.tick_label_font) for label in labels]

        # set legend
        legend_handles, legend_labels = self.ax.get_legend_handles_labels()
        legend_dict = dict()
        legend_dict["handles"] = legend_handles
        legend_dict["labels"] = self.legend if self.legend is not None else legend_labels
        legend_dict["columnspacing"] = 0.3
        legend_dict["loc"] = "best" if self.legend_loc is None else self.legend_loc
        legend_dict["frameon"] = self.legend_frameon
        legend_dict["prop"] = default_cfg.legend_font
        if self.ncol is not None:
            legend_dict["ncol"] = self.ncol

        if self.show_legend:
            self.ax.legend(**legend_dict)
        else:
            plt.legend([], [], frameon=False)

        #  label
        plt.xlabel(self.xlabel, self.label_font_dict)
        plt.ylabel(self.ylabel, self.label_font_dict)

        if self.xlim is not None:
            plt.xlim(self.xlim)
        if self.ylim is not None:
            plt.ylim(self.ylim)
        if self.xticks is not None and self.xtick_labels is not None:
            plt.xticks(self.xticks, self.xtick_labels)
        if self.yticks is not None and self.ytick_labels is not None:
            plt.yticks(self.yticks, self.ytick_labels)
        if self.ticklabel_style:
            plt.ticklabel_format(style=self.ticklabel_style, axis="x", scilimits=(0, 0))
            
    def save(self):
        if self.fname is None:
            pass
        else:
            dir_path = os.path.dirname(self.fname)
            os.makedirs(dir_path, exist_ok=True)
            self.fig.set_tight_layout(True)
            plt.tight_layout(pad=self.pad)
            plt.savefig(self.fname)

    def show(self):
        self.fig.set_tight_layout(True)
        plt.tight_layout(pad=self.pad)
        plt.show()

    def close(self):
        plt.close()


def plot_sns(
    data,
    fname,
    *,
    xlabel=None,
    ylabel=None,
    legend=None,
    legend_loc="best",
    legend_frameon=False,
    xlim=None,
    ylim=None,
    xticks=None,
    yticks=None,
    xtick_labels=None,
    ytick_labels=None,
    display=False,
    fig_size=None,
    dpi=None,
    style="white",
    ticklabel_style=None,
    show_legend=True,
    **kwargs,
):
    """
    plot a curve using seaborn
    :param data: data: list[dict]:
        data used to plot figures,
        example: [dict(x=x1_list, y=y1_list, label=label1), dict(x=x2_list, y=y2_list, label=label2)]
        when there is no repeat experiment data, xi_list=x, shape of x is [d,],
                                                 yi_list=y, shape of y is [d,],
                                                 lableli str,
        when there is repeat experiment data, xi_list=[x1, x2, ..., xd], shape of xi is [d,],
                                              yi_list=[y1, y2, ..., yd], shape of y is [d,],
                                              lableli str,

    :param fname: fname: str,
        the figure will be saved here,
        example: "./path_to_file/figure.png"
    :param xlabel:  str
    :param ylabel:  str
    :param legend:
    :param legend_loc: "best", "upper right", "upper left", "lower left", "lower right", "right", "center left",
        "center right", "lower center", "upper center", "center"
    :param legend_frameon: whether legend has background frame
    :param xlim:
    :param ylim:
    :param xticks:
    :param yticks:
    :param xtick_labels:
    :param ytick_labels:
    :param display:
    :param fig_size:
    :param dpi:
    :param kwargs:
    :style: "white", "dark", "whitegrid", "darkgrid"
    :ticklabel_style: "sci" or "plain"
    :return:
    """
    ploter = PloterSns(
        data,
        fname,
        xlabel=xlabel,
        ylabel=ylabel,
        legend=legend,
        legend_loc=legend_loc,
        legend_frameon=legend_frameon,
        xlim=xlim,
        ylim=ylim,
        xticks=xticks,
        yticks=yticks,
        xtick_labels=xtick_labels,
        ytick_labels=ytick_labels,
        display=display,
        fig_size=fig_size,
        dpi=dpi,
        style=style,
        ticklabel_style=ticklabel_style,
        show_legend=show_legend,
        **kwargs,
    )
    ploter.plot()
    if fname is not None:
        ploter.save()
    if display:
        ploter.show()

    ploter.close()

import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import rcParams
from typing import Union, List
from hplot.config import default_cfg
from hplot.utils import cm2inch


class PloterHeatmap:
    def __init__(
        self,
        x,
        y,
        z,
        fname,
        *,
        cmap,
        vmin,
        vmax,
        center=None,
        levels=None,
        level_colors=None,
        xlabel=None,
        ylabel=None,
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
    ):
        self.x = x
        self.y = y
        self.z = z
        self.fname = fname
        self.cmap = cmap
        self.vmin = vmin
        self.vmax = vmax
        self.center = center
        self.levels = levels
        self.level_colors = level_colors
        self.xlabel = xlabel
        self.ylabel = ylabel
 
        self.xtick_labels = xtick_labels
        self.ytick_labels = ytick_labels
        self.usetex = usetex

        self.display = display
        self.fig_size = fig_size
        self.dpi = dpi
        self.pad = pad
        self.tick_size = tick_size
        self.tick_label_font = tick_label_font
        self.legend_font_dict = legend_font_dict
        self.label_font_dict = label_font_dict
        plt.cla()
        plt.clf()
        plt.close()
        self.num_data = None
        self.fig = None
        self.ax = None
        self.__preprocess()

    def __preprocess(self):
        rcParams.update({"mathtext.fontset": "stix"})

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
        self.fig, self.ax = plt.subplots(figsize=cm2inch(*self.fig_size), dpi=self.dpi)
        # plot figure
        if isinstance(self.cmap, str):
            cmap = plt.get_cmap(self.cmap)
        else:
            cmap = self.cmap
        self.ax = sns.heatmap(
            self.z,
            cmap=cmap,
            vmin=self.vmin,
            vmax=self.vmax,
            center=self.center,
        )

        cbar = self.ax.collections[0].colorbar
        cbar.ax.tick_params(labelsize=default_cfg.tick_size)
        labels = cbar.ax.get_yticklabels()
        [label.set_fontname(default_cfg.tick_label_font) for label in labels]
        if self.levels:
            plt.contour(self.z, colors=self.level_colors, levels=self.levels)

        if self.xtick_labels is not None:
            pos_list_x = self._tick2pos(self.xtick_labels, self.x)
            plt.xticks(pos_list_x, self.xtick_labels, rotation=0)
        if self.ytick_labels is not None:
            pos_list_y = self._tick2pos(self.ytick_labels, self.y)
            plt.yticks(pos_list_y, self.ytick_labels)
        
        if self.xlabel:
            plt.xlabel(self.xlabel, self.label_font_dict)
        if self.ylabel:
            plt.ylabel(self.ylabel, self.label_font_dict)

        plt.tick_params(labelsize=default_cfg.tick_size)
        labels = self.ax.get_xticklabels() + self.ax.get_yticklabels()
        [label.set_fontname(default_cfg.tick_label_font) for label in labels]
        plt.ylabel(self.ylabel, self.label_font_dict)
        self.ax.invert_yaxis()
        
    def _tick2pos(
        self,
        tick: Union[np.ndarray, List[float]],
        anchor: Union[np.ndarray, List[float]],
    ) -> List[int]:
        pos = []

        if isinstance(anchor, list):
            anchor = np.array(anchor).reshape(-1)

        for t in tick:
            t = float(t)
            dist = (anchor - t) ** 2
            label = np.argmin(dist)
            pos.append(int(label))
        return pos

            
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


def plot_heatmap(
    x,
    y,
    z,
    fname,
    *,
    cmap,
    vmin,
    vmax,
    center=None,
    levels=None,
    level_colors=None,
    xlabel=None,
    ylabel=None,
    xtick_labels=None,
    ytick_labels=None,
    display=False,
    fig_size=None,
    dpi=None,
    **kwargs,
):

    ploter = PloterHeatmap(
        x,
        y,
        z,
        fname,
        xlabel=xlabel,
        ylabel=ylabel,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        center=center,
        levels=levels,
        level_colors=level_colors,
        xtick_labels=xtick_labels,
        ytick_labels=ytick_labels,
        display=display,
        fig_size=fig_size,
        dpi=dpi,

        **kwargs,
    )
    ploter.plot()
    if fname is not None:
        ploter.save()
    if display:
        ploter.show()

    ploter.close()

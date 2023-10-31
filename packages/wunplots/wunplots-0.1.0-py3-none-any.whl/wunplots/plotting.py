import os
from typing import Sequence

import matplotlib as mpl
from cycler import Cycler, cycler
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from wuncolors import Color, RGB
from wunplots.utils import pop


class Plotting:
    small_fontsize = 8
    medium_fontsize = 12
    large_fontsize = 20

    def __init__(self, save: bool = False, save_directory: str | None = None) -> None:
        if save and save_directory is None:
            raise ValueError("Set save directory if you want to save plots")
        self.save = save
        self.save_directory = save_directory

        self.background_color: Color = Color("White", RGB(255, 255, 255))
        self.spines_color: Color = Color("Black", RGB(1., 1., 1.))
        self.font_color: Color = Color("Black", RGB(1., 1., 1.))
        self.font = "Arial"
        self.cycler_colors: list[Color] = []

    def new(
        self,
        width: float = 8,
        heigth: float = 5,
        nrows: int = 1,
        ncols: int = 1,
        **kwargs,
    ):
        plt.rc("font", size=pop(kwargs, "fontsize") or self.small_fontsize)
        plt.rc("axes", titlesize=pop(kwargs, "axes_titlesize") or self.medium_fontsize)
        plt.rc("axes", labelsize=pop(kwargs, "axes_labelsize") or self.small_fontsize)
        plt.rc("xtick", labelsize=pop(kwargs, "xtick_labelsize") or self.small_fontsize)
        plt.rc("ytick", labelsize=pop(kwargs, "ytick_labelsize") or self.small_fontsize)
        plt.rc("legend", fontsize=pop(kwargs, "legend_fontsize") or self.small_fontsize)
        plt.rc("figure", titlesize=pop(kwargs, "figure_titlesize") or self.large_fontsize)

        # Setting Cycler
        if len(self.cycler_colors):
            plt.rc("axes", prop_cycle=self.cycler())

        mpl.rcParams["text.color"] = self.font_color.decimal_rgba()
        mpl.rcParams["axes.labelcolor"] = self.font_color.decimal_rgba()
        mpl.rcParams["xtick.color"] = self.font_color.decimal_rgba()
        mpl.rcParams["ytick.color"] = self.font_color.decimal_rgba()

        mpl.rcParams["font.sans-serif"] = self.font
        mpl.rcParams["font.family"] = "sans-serif"
        mpl.rcParams["savefig.dpi"] = 300

        fig, axes = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            figsize=(width, heigth),
            facecolor=self.background_color.decimal_rgba(),
            **kwargs,
        )
        self.apply_axes_colors(axes)
        return fig, axes

    def apply_axes_colors(self, axes: Axes | Sequence[Axes]) -> None:
        axes = [axes] if isinstance(axes, Axes) else axes.flat

        for ax in axes:
            ax.set_facecolor(self.background_color.decimal_rgba())
            for axis in ["top", "bottom", "left", "right"]:
                ax.spines[axis].set_color(self.spines_color.decimal_rgba())

    def cycler(self) -> Cycler:
        return cycler(
            color=[
                c.decimal_rgba()
                for c in self.cycler_colors
                if c != self.background_color
            ]
        )

    @classmethod
    def clear(cls) -> None:
        plt.cla()
        plt.clf()

    def show(self, name: str = None) -> None:
        plt.tight_layout()
        if self.save:
            assert name is not None
            self.save_current(name)

        plt.show()

    def save_current(self, name: str, clear_all: bool = False) -> None:
        plt.tight_layout()
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

        plt.savefig(f"{self.save_directory}/{name}.png")
        if clear_all:
            self.clear()

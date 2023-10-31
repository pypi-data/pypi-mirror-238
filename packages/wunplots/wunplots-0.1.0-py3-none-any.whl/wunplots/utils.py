from typing import Sequence

import numpy as np
from matplotlib.axes import Axes

from wuncolors import Color, RGB


def pop(d: dict, key, default=None):
    try:
        return d.pop(key)
    except KeyError:
        return default


def weighted_rgb(v: np.ndarray, color: Color) -> list[Color]:
    r, g, b = color.rgb()
    color = [Color("f{color}({alpha})", RGB(r, g, b, alpha)) for alpha in v / np.max(v)]
    return color


def weighted_size(v: np.ndarray, factor: float = 20.0) -> np.ndarray:
    return v / np.max(v) * factor


def annotate_values(
    x: Sequence[float | int] | int | float,
    y: Sequence[float | int],
    text: Sequence[float | int | str],
    ax: Axes,
    overlap_scale: float = 0.03,
    **kwargs,
):
    if isinstance(x, (float, int)):
        x = [x] * len(y)

    last = -1000000
    rng = max(y) - min(y)
    rng = rng if rng > 0 else 1
    for ix, iy, txt in zip(x, y, text):
        if abs((iy - last) / rng) < overlap_scale:
            continue
        txt = f"{txt:.2f}" if isinstance(x, (float, int)) else txt
        ax.text(ix, iy, txt, **kwargs)
        last = iy

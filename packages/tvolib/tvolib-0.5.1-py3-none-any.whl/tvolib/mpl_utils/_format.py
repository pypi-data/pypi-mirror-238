__all__ = [
    "add_colorbar",
    "add_text",
    "format_datetime_axis",
]

import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1 import make_axes_locatable


def add_colorbar(axis, where="right", pad=0.05, size="2%"):
    r"""Adds colorbar next to an axis"""
    divider = make_axes_locatable(axis)
    return divider.append_axes(where, size=size, pad=pad)


def add_text(axis, x, y, text, **kwargs):
    transform = axis.transAxes
    box_format = dict(facecolor="wheat", alpha=0.9)
    axis.text(x, y, text, transform=transform, bbox=box_format, **kwargs)


def format_datetime_axis(axis):
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    axis.xaxis.set_major_formatter(formatter)

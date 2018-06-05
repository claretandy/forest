"""Forest colorbar helpers

A colorbar should re-render as plots update. Since ForestPlot holds
references to matplotlib pcolormesh or imshow return values, a mapping
must be provided between matplotlib.colors.ListedColorMap and a
bokeh.models.ColumnDataSource.

The ColumnDataSource is used as the driving data for bokeh.plotting.Figure
instance call to rect()
"""
import numpy as np
import bokeh.models
import bokeh.plotting


__all__ = [
    "Colorbar",
    "rgb",
    "source_dict",
    "colorbar_figure"
]

class Colorbar(object):
    """Forest colorbar widget"""
    def __init__(self, color_map, x_min, x_max, figure=None):
        """Helper to generate a bokeh widget that acts like a colorbar
        """
        if figure is None:
            self.figure = colorbar_figure()
        else:
            self.figure = figure

        # Relationship between data and colors
        source = bokeh.models.ColumnDataSource(source_dict(color_map,
                                                           x_min,
                                                           x_max))
        figure.rect(x="x",
                    y=0.5,
                    height=1.,
                    width="width",
                    color="color",
                    source=source)
        self.source = source

    def update(self, color_map, x_min, x_max):
        """Re-render colorbar using different color map and limits"""
        self.source.data = source_dict(color_map,
                                       x_min,
                                       x_max)
        self.figure.xaxis.range = bokeh.models.Range1d(x_min, x_max)


def source_dict(color_map, x_min, x_max):
    """Create a ColumnDataSource dict from color map and x range"""
    x = np.linspace(x_min, x_max, color_map.N)
    return {
        "x": x,
        "width": np.diff(x),
        "color": rgb(color_map.colors)
    }


def colorbar_figure():
    """Colorbar bokeh figure with appropriate hover tool"""
    # Make a figure suitable to contain a colorbar
    figure = bokeh.plotting.figure(tools="",
                                   plot_width=500,
                                   plot_height=60)
    figure.yaxis.visible = False
    figure.toolbar_location = None
    figure.min_border = 20

    # Hover tooltip
    hover = bokeh.models.HoverTool()
    hover.tooltips = [
        ("value", "$value"),
        ("color", "$color[hex, swatch]:fill_color")
    ]
    figure.add_tools(hover)
    return figure


def rgb(colors):
    """Map color map colors to RGB Hexadecimal values"""
    return ["#{:02x}{:02x}{:02x}".format(int(255 * r), int(255 * g), int(255 * b))
            for r, g, b in colors]
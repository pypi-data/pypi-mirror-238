import altair as alt

from persist_ext.internals.vis.plot_helpers import base_altair_plot
from persist_ext.internals.widgets.trrackable_output.output_with_trrack_widget import (
    OutputWithTrrackWidget,
)
from persist_ext.internals.widgets.vegalite_chart.vegalite_chart_widget import (
    VegaLiteChartWidget,
)


def scatterplot(
    data,
    x,
    y,
    color=None,
    circle=False,
    interaction=True,
    selection_type="interval",
    height=400,
    width=400,
):
    """
    Args:
        data (): url to a altair compatible dataset or a pandas dataframe
        x (): field to encode for x axis; can also be a altair axis object
        y (): field to encode for y axis; can also be a ltair axis object
        interaction (): enable 2d brush interactions
    Raises:
        TypeError: if data is not a url string or a dataframe

    Returns:
        altair chart object
    """
    chart, data = base_altair_plot(data, height=height, width=width)

    if circle:
        chart = chart.mark_circle()
    else:
        chart = chart.mark_point()

    chart = chart.encode(x=x, y=y)

    if color:
        chart.encode(color=color)

    if not interaction:
        return chart

    selection = None

    if selection_type == "point":
        selection = alt.selection_point(name="selector", encodings=["x", "y"])
    else:
        selection = alt.selection_interval(name="selector", encodings=["x", "y"])

    chart = chart.add_params(selection)

    if color:
        chart = chart.encode(color=alt.condition(selection, color, alt.value("gray")))
    else:
        chart = chart.encode(
            color=alt.condition(selection, alt.value("steelblue"), alt.value("gray"))
        )

    return OutputWithTrrackWidget(
        body_widget=VegaLiteChartWidget(chart=chart, data=data), data=data
    )

#! /usr/bin/env python

import os
import sys
import tempfile

import click
import pandas as pd
import plotly.express as px
from _plotly_utils.colors.qualitative import Plotly as colors
from plotly.graph_objs.scatter import ErrorY


def get_df(input):
    with tempfile.TemporaryDirectory() as tmpdir:
        input_ = os.path.join(tmpdir, "_")
        with open(input_, "w") as out:
            # needed to cache when reading from stdin
            out.write(input.read())
        try:
            return pd.read_json(input_, lines=True)
        except ValueError:
            pass

        try:
            df = pd.read_csv(input_)
            if len(df.columns) < 2:
                if len(df.head(1).values[0][0].split()) == 2:
                    # for space seperated values with no header
                    return pd.read_csv(input_, header=None, sep=None, names=["x", "y"])
            else:
                return df
        except ValueError:
            pass


def get_line_fig(df, title, xcol, ycols):
    # breakpoint()
    fig = px.line(
        df,
        x=xcol,
        y=ycols,
    )

    return fig


def get_mean_fig(df, title, xcol, ycols, nbins):

    try:
        df_binned = df.groupby(pd.cut(df[xcol], nbins)).mean()
        for _ycol in ycols:
            df_binned[f"{_ycol}_sem"] = df.groupby(pd.cut(df[xcol], nbins)).sem()[_ycol]
    except TypeError:  # if cut doesn't work assume time_range
        df[xcol] = pd.to_datetime(df[xcol])
        time_range = df[xcol].max() - df[xcol].min()
        interval = time_range / nbins
        df_binned = df.resample(interval, on=xcol).mean()
        df_binned[xcol] = (
            df.resample(interval, on=xcol).min()[xcol]
            + (
                df.resample(interval, on=xcol).max()[xcol]
                - df.resample(interval, on=xcol).min()[xcol]
            )
            / 2.0
        )
        for _ycol in ycols:
            df_binned[f"{_ycol}_sem"] = df.resample(interval, on=xcol).sem()[_ycol]

    fig = px.line(
        df_binned,
        x=xcol,
        y=ycols,
    )
    for idx, _ycol in enumerate(ycols):
        fig.data[idx].error_y = ErrorY(array=df_binned[f"{_ycol}_sem"].to_numpy())

    return fig


def get_quant_fig(df, title, xcol, ycols, nbins, quantile):
    _quantile = quantile / 100.0
    try:
        df_binned = df.groupby(pd.cut(df[xcol], nbins)).quantile(q=_quantile)
    except TypeError:  # if cut doesn't work assume time_range
        df[xcol] = pd.to_datetime(df[xcol])
        time_range = df[xcol].max() - df[xcol].min()
        interval = time_range / nbins
        df_binned = df.resample(interval, on=xcol).quantile(q=_quantile)
        df_binned[xcol] = (
            df.resample(interval, on=xcol).min()[xcol]
            + (
                df.resample(interval, on=xcol).max()[xcol]
                - df.resample(interval, on=xcol).min()[xcol]
            )
            / 2.0
        )

    return px.line(
        df_binned,
        x=xcol,
        y=ycols,
    )


@click.command()
@click.option(
    "-i", "--input", type=click.File(), default="-", help="Input file, default stdin"
)
@click.option(
    "-o", "--output", type=click.File("wb"), help="Output file, default stdout"
)
@click.option("-t", "--title", type=str, help="Title, default input filename")
@click.option("-x", "--xcol", type=str, help="x column, default first column")
@click.option("-y", "--ycol", type=str, help="y column, default second column")
@click.option("-n", "--nbins", type=int, default=60, help="number of bins")
@click.option("-q", "--quantile", type=int, default=50, help="quantile, aka percentile")
@click.option(
    "--line", "plot", flag_value="line", default=True, help="draw line plot (default)"
)
@click.option("--mean", "plot", flag_value="mean", help="draw means of bins")
@click.option("--quant", "plot", flag_value="quant", help="draw quantiles of bins")
@click.option("--gui", is_flag=True, help="show output in a gui")
@click.option("--dualy", is_flag=True, help="two y axes for two lines")
def main(input, output, title, xcol, ycol, nbins, quantile, plot, gui, dualy):
    df = get_df(input)
    _xcol = xcol if xcol else df.columns[0]
    ycols = ycol.split(",") if ycol else [df.columns[1]]
    if dualy and len(ycols) != 2:
        print("exactly 2 y columns are required for dual y axes")
        return

    if plot == "mean":
        fig = get_mean_fig(df, title, _xcol, ycols, nbins)
    elif plot == "quant":
        fig = get_quant_fig(df, title, _xcol, ycols, nbins, quantile)
    else:
        fig = get_line_fig(df, title, _xcol, ycols)

    fig.update_layout(title=title if title else input.name, title_x=0.5)
    if dualy:
        fig.data[1].yaxis = "y2"
        fig.update_layout(
            yaxis1={
                "side": "left",
                "title": ycols[0],
                "tickfont": {"color": colors[0]},
                "titlefont": {"color": colors[0]},
            },
            yaxis2={
                "side": "right",
                "title": ycols[1],
                "tickfont": {"color": colors[1]},
                "titlefont": {"color": colors[1]},
                "overlaying": "y",
            },
        )

    if gui:
        fig.show()
        return
    img_bytes = fig.to_image(format="png")
    if output:
        output.write(img_bytes)
    else:
        sys.stdout.buffer.write(img_bytes)


if __name__ == "__main__":
    main()

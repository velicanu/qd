#! /usr/bin/env python

import json
import os
import sys
import tempfile

import click
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from _plotly_utils.colors.qualitative import Plotly as colors

# from plotly.graph_objs.scatter import ErrorY as sErrorY

# from plotly.graph_objs.histogram.ErrorY import as hErrorY


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


def get_line_fig(df, xcol, ycols):
    fig = px.line(
        df,
        x=xcol,
        y=ycols,
    )

    return fig


def get_hist_fig(df, xcols, nbins):
    binned_dfs = []
    for col in xcols:
        try:
            df_binned = df.groupby(pd.cut(df[col], nbins)).mean()
            if col not in df_binned.columns:
                raise TypeError
            df_binned["__count"] = df.groupby(pd.cut(df[col], nbins)).count()[col]
            df_binned["__rootn"] = df_binned["__count"] ** (1 / 2)
            binned_dfs.append(df_binned)
        except TypeError:  # if cut doesn't work assume time_range
            df[col] = pd.to_datetime(df[col])
            time_range = df[col].max() - df[col].min()
            interval = time_range / nbins
            df_binned = df.resample(interval, on=col).count()
            df_binned[col] = (
                df.resample(interval, on=col).min()[col]
                + (
                    df.resample(interval, on=col).max()[col]
                    - df.resample(interval, on=col).min()[col]
                )
                / 2.0
            )
            df_binned["__count"] = df.groupby(
                df.resample(interval, on=col).count()
            ).count()[col]
            df_binned["__rootn"] = df_binned["__count"] ** (1 / 2)
            binned_dfs.append(df_binned)

    fig = px.line(binned_dfs[0], x=xcols[0], y="__count", error_y="__rootn")
    for idx, (col, df_) in enumerate(zip(xcols[1:], binned_dfs[1:])):
        fig.add_trace(
            go.Scatter(
                x=df_[col],
                y=df_["__count"],
                error_y=go.scatter.ErrorY(array=df_["__rootn"].to_numpy()),
            )
        )
    return fig


def get_mean_fig(df, xcol, ycols, nbins):
    try:
        df_binned = df.groupby(pd.cut(df[xcol], nbins)).mean()
        if xcol not in df_binned.columns:
            raise TypeError
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
        fig.data[idx].error_y = go.scatter.ErrorY(
            array=df_binned[f"{_ycol}_sem"].to_numpy()
        )

    return fig


def get_quant_fig(df, xcol, ycols, nbins, quantile):
    _quantile = quantile / 100.0
    try:
        df_binned = df.groupby(pd.cut(df[xcol], nbins)).quantile(q=_quantile)
        if xcol not in df_binned.columns:
            raise TypeError
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
@click.version_option()
@click.option(
    "-i", "--input", type=click.File(), default="-", help="Input file, default stdin"
)
@click.option(
    "-o", "--output", type=click.File("wb"), help="Output file, default stdout"
)
@click.option("-t", "--title", type=str, help="Title, default input filename")
@click.option("-x", "--xcol", type=str, help="x column, default first column")
@click.option("-y", "--ycol", type=str, help="y column, default second column")
@click.option("-n", "--nbins", type=int, default=60, help="number of bins [60]")
@click.option(
    "-q",
    "--quantile",
    type=int,
    default=50,
    help="quantile, aka percentile [50]",
)
@click.option(
    "--line", "plot", flag_value="line", default=True, help="draw line plot (default)"
)
@click.option("--mean", "plot", flag_value="mean", help="draw means of bins")
@click.option("--quant", "plot", flag_value="quant", help="draw quantiles of bins")
@click.option("--hist", "plot", flag_value="hist", help="draw histgram of values")
@click.option("--gui", is_flag=True, help="show output in a gui")
@click.option("--dualy", is_flag=True, help="two y axes for two lines")
def main(input, output, title, xcol, ycol, nbins, quantile, plot, gui, dualy):
    df = get_df(input)
    xcols = xcol.split(",") if xcol else [df.columns[0]]
    if len(df.columns) > 1:
        ycols = ycol.split(",") if ycol else [df.columns[1]]
    else:
        ycols = []

    columns = set(df.columns)
    missing_cols = [col for col in (xcols + ycols) if col not in columns]
    if missing_cols:
        print(f"error columns: {json.dumps(missing_cols)} not in {columns}")
        return

    if len(ycols) >= 2 and len(xcols) >= 2:
        print(
            "error more than 1 x-column is not supported when there are multiple y-columns"
        )
        return

    if dualy and len(ycols) != 2:
        print("exactly 2 columns are required for dual y axes")
        return

    if plot == "mean":
        fig = get_mean_fig(df, xcols[0], ycols, nbins)
    elif plot == "quant":
        fig = get_quant_fig(df, xcols[0], ycols, nbins, quantile)
    elif plot == "hist":
        fig = get_hist_fig(df, xcols, nbins)
    else:
        fig = get_line_fig(df, xcols[0], ycols)

    fig.update_layout(title=title if title else input.name, title_x=0.5)
    fig.update_layout(yaxis1={"title": ycols[0]})
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

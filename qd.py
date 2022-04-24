#! /usr/bin/env python

import os
import sys
import tempfile

import click
import pandas as pd
import plotly.express as px


def get_df(input):
    with tempfile.TemporaryDirectory() as tmpdir:
        input_ = os.path.join(tmpdir, "_")
        with open(input_, "w") as out:
            out.write(input.read())
        try:
            return pd.read_json(input_, lines=True)
        except ValueError:
            pass

        try:
            return pd.read_csv(input_)
        except ValueError:
            pass


def get_line_fig(df, title, xcol, ycol, xlabel, ylabel):
    _xcol = xcol if xcol else df.columns[0]
    _ycol = ycol if xcol else df.columns[1]
    return px.line(
        df,
        x=_xcol,
        y=_ycol,
        labels={
            _xcol: (xlabel if xlabel else _xcol),
            _ycol: (ylabel if ylabel else _ycol),
        },
    )


def get_dist_fig(df, title, xcol, ycol, xlabel, ylabel, nbins):
    _xcol = xcol if xcol else df.columns[0]
    _ycol = ycol if xcol else df.columns[1]

    try:
        df_binned = df.groupby(pd.cut(df[_xcol], nbins)).mean()
        df_binned["__sem__"] = df.groupby(pd.cut(df[_xcol], nbins)).sem()[_ycol]
    except TypeError:  # if cut doesn't work assume time_range
        df[_xcol] = pd.to_datetime(df[_xcol])
        time_range = df[_xcol].max() - df[_xcol].min()
        interval = time_range / nbins
        df_binned = df.resample(interval, on=_xcol).mean()
        df_binned[_xcol] = (
            df.resample(interval, on=_xcol).min()[_xcol]
            + (
                df.resample(interval, on=_xcol).max()[_xcol]
                - df.resample(interval, on=_xcol).min()[_xcol]
            )
            / 2.0
        )
        df_binned["__sem__"] = df.resample(interval, on=_xcol).sem()[_ycol]

    return px.line(
        df_binned,
        x=_xcol,
        y=_ycol,
        labels={
            _xcol: (xlabel if xlabel else _xcol),
            _ycol: (ylabel if ylabel else _ycol),
        },
        error_y="__sem__",  # standard error of mean
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
@click.option("-xl", "--xlabel", type=str, help="x label, default x column")
@click.option("-yl", "--ylabel", type=str, help="x label, default x column")
@click.option("-n", "--nbins", type=int, default=60, help="number of bins")
@click.option("--line", "plot", flag_value="line", default=True)
@click.option("--dist", "plot", flag_value="dist")
@click.option("--gui", is_flag=True)
def main(input, output, title, xcol, ycol, xlabel, ylabel, nbins, plot, gui):
    df = get_df(input)

    if plot == "dist":
        fig = get_dist_fig(df, title, xcol, ycol, xlabel, ylabel, nbins)
    else:
        fig = get_line_fig(df, title, xcol, ycol, xlabel, ylabel)

    fig.update_layout(title=title if title else input.name, title_x=0.5)
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

# qd

quick-draw: a cli plotting tool

`qd` is a command line tool to quickly make plots from csv and json files or
streams. It is built on top of the `pandas` and `plotly` libraries.

## Installation and usage

`qd` can be installed via `pip install quick-draw`. It requires Python 3.7+.

## Basic usage

Make a quick plot using the first columns available and display the output right in the
terminal.

```bash
cat data/trig.json | qd | imgcat
```
<img src="https://raw.githubusercontent.com/velicanu/qd/master/media/qd_basic.gif" width="600">

In addition to reading from stdin and writing to stdout, files can also be passed in as
arguments.

```bash
qd -i data/trig.json -o trig.png
```

The output can also be shown in an interactive gui.

```bash
qd -i data/trig.json --gui
```

All the cli functionality available can be seen via the `--help` option.

```bash
qd --help
```

### More examples

#### Mean in bins

Plot the mean values in some bins specifying the x and y columns.

```bash
cat data/trig.json | qd -x x -y sin,cos --mean | imgcat
```
<img src="https://raw.githubusercontent.com/velicanu/qd/master/media/qd_mean.gif" width="600">

#### Percentile in bins

Plot the 95th percentile values in 20 bins

```bash
cat data/trig.json | qd -x x -y sin --quant -q 95 --nbins 20  | imgcat
```
<img src="https://raw.githubusercontent.com/velicanu/qd/master/media/qd_quant.gif" width="600">

#### Histogram of values

Make a histogram from two sets of data using 20 bins.

```bash
cat data/dists.csv | qd -x gauss,expo --hist -n20 | imgcat
```
<img src="https://raw.githubusercontent.com/velicanu/qd/master/media/qd_hist.gif" width="600">

## Local Development

Clone this repo from github and in a virtual environment do the following:

```bash
pip install .  # installs qd based on local code changes
pip install -r requirements-dev.txt  # installs extra packages for dev and testing
```

Tests can be run via:

```bash
pytest -n4
```

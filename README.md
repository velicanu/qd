# qd

quick-draw: a cli plotting tool

`qd` is a command line tool to quickly make plots from csv and json files or
streams. It is built on top of the `pandas` and `plotly` libraries.

## Installation and usage

`qd` can be installed via `pip install qd-plot`. It requires Python 3.7+.

## Basic usage

Make a quick plot using the first columns available and display the output in a gui
(default web browser).

```bash
cat data/trig.json | qd --gui
```
![qd basic](/media/qd_basic.gif)

By default `qd` reads data from `stdin` and writes image bytes to `stdout`, however it
also accepts input and output files as arguments, as well as the `--gui` option shown
above.

```bash
qd -i data/trig.json -o trig.png
```

All the cli functionality available can be seen via the `--help` option.

```bash
qd --help
```

### MacOS + iTerm2

Since `qd` writes to stdout by default, the images can be displayed right in the
terminal window if using a compatible terminal, such as iTerm2 with `imgcat`:

```bash
cat data/trig.json | qd | imgcat
```
<img src="https://raw.githubusercontent.com/velicanu/qd/master/media/qd_basic_imgcat.gif" width="600">


### More examples

#### Mean in bins

Plot the mean values in some bins specifying the x and y columns.

```bash
cat data/trig.json | qd -x x -y sin,cos --mean --gui
```
![qd mean](/media/qd_mean.gif)

#### Percentile in bins

Plot the 95th percentile values in 20 bins

```bash
cat data/trig.json | qd -x x -y sin --quant -q 95 --nbins 20 --gui
```
![qd quant](/media/qd_quant.gif)

#### Histogram of values

Make a histogram from two sets of data using 20 bins.

```bash
cat data/dists.csv | qd -x gauss,expo --hist -n20 --gui
```
![qd hist](/media/qd_hist.gif)

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

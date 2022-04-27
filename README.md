# qd

quick-draw: a cli plotting tool



## Installation and usage

_qd_ can be installed via `pip install quick-draw`. It requires Python 3.7+.

## Examples

### Basic usage

Make a quick plot using the first columns available and display the output right in the
terminal.

```bash
cat data/trig.json | qd | imgcat
```
<!-- https://raw.githubusercontent.com/velicanu/qd/master/media/qd_basic.gif -->
<img src="https://raw.githubusercontent.com/velicanu/qd/master/media/qd_basic.gif" width="600">
<!-- <a>![qd-basic](./media/qd_basic.gif)</a> -->

In addition to reading from stdin and writing to stdout, files can also be passed in as
arguments.

```bash
qd -i data/trig.json -o trig.png
```

The output can also be shown in an interactive gui (due to plotly under the hood).

```bash
qd -i data/trig.json --gui
```

### Mean in bins

Plot the mean values in some bins specifying the x and y columns.

![qd-mean](./media/qd_mean.gif)

### Percentile in bins

Plot the 95th percentile values in 20 bins

![qd-quant](./media/qd_quant.gif)

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

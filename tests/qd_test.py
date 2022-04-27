import json
import os
import subprocess
import tempfile

import pytest
from qd import get_df


@pytest.fixture
def tmpfile():
    with tempfile.TemporaryDirectory() as _tmpdir:
        yield os.path.join(_tmpdir, "file.png")


def test_get_df_json():
    input_ = """
{"x": 0.0, "cos": 11.3, "sin": -0.7}
{"x": 0.06, "cos": 10.6, "sin": -0.04}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "_")
        with open(filename, "w") as f:
            f.write(input_)
        df = get_df(open(filename))

    actual = json.loads(df.to_json(orient="records"))
    expected = [
        {"x": 0.0, "cos": 11.3, "sin": -0.7},
        {"x": 0.06, "cos": 10.6, "sin": -0.04},
    ]

    assert actual == expected


def test_get_df_csv():
    input_ = """
x,cos,sin
0.0,11.3,-0.7
0.06,10.6,-0.04
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "_")
        with open(filename, "w") as f:
            f.write(input_)
        df = get_df(open(filename))

    actual = json.loads(df.to_json(orient="records"))
    expected = [
        {"x": 0.0, "cos": 11.3, "sin": -0.7},
        {"x": 0.06, "cos": 10.6, "sin": -0.04},
    ]

    assert actual == expected


def test_cli_no_args():
    proc = subprocess.run("qd -i data/trig.json".split())
    assert proc.returncode == 0


def test_cli_line(tmpfile):
    subprocess.run(f"qd -i data/trig.json -y cos,sin -o {tmpfile}".split())
    assert os.path.exists(tmpfile)


def test_cli_mean(tmpfile):
    subprocess.run(f"qd -i data/trig.json -y cos,sin --mean -o {tmpfile}".split())
    assert os.path.exists(tmpfile)


def test_cli_quant(tmpfile):
    subprocess.run(f"qd -i data/trig.json -y cos,sin --quant -o {tmpfile}".split())
    assert os.path.exists(tmpfile)


def test_cli_line_dualy(tmpfile):
    subprocess.run(f"qd -i data/trig.json -y cos,sin --dualy -o {tmpfile}".split())
    assert os.path.exists(tmpfile)


def test_cli_mean_dualy(tmpfile):
    subprocess.run(
        f"qd -i data/trig.json -y cos,sin --mean --dualy -o {tmpfile}".split()
    )
    assert os.path.exists(tmpfile)


def test_cli_quant_dualy(tmpfile):
    subprocess.run(
        f"qd -i data/trig.json -y cos,sin --quant --dualy -o {tmpfile}".split()
    )
    assert os.path.exists(tmpfile)


def test_cli_quant_75(tmpfile):
    subprocess.run(
        f"qd -i data/trig.json -y cos,sin --quant -q 75 -o {tmpfile}".split()
    )
    assert os.path.exists(tmpfile)


def test_cli_mean_nbins(tmpfile):
    subprocess.run(
        f"qd -i data/trig.json -y cos,sin --mean --nbins 9 -o {tmpfile}".split()
    )
    assert os.path.exists(tmpfile)


def test_cli_xcol(tmpfile):
    subprocess.run(f"qd -i data/trig.json -x cos -y sin -o {tmpfile}".split())
    assert os.path.exists(tmpfile)


def test_cli_stdin(tmpfile):
    cat = subprocess.Popen(("cat", "data/trig.json"), stdout=subprocess.PIPE)
    subprocess.check_output(("qd", "-o", tmpfile), stdin=cat.stdout)
    assert os.path.exists(tmpfile)


def test_cli_stdin_stdout(tmpfile):
    cat = subprocess.Popen(("cat", "data/trig.json"), stdout=subprocess.PIPE)
    with open(tmpfile, "w") as f:
        subprocess.Popen("qd", stdin=cat.stdout, stdout=f)
    assert os.path.exists(tmpfile)


def test_cli_hist_csv(tmpfile):
    subprocess.run(
        f"qd -i data/dists.csv -x gauss,expo --hist --nbins 9 -o {tmpfile}".split()
    )
    assert os.path.exists(tmpfile)

import json
import os
import tempfile

from qd import get_df


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

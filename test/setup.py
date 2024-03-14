import os
import shutil
import unittest
import pandas as pd
from typing import Tuple
from src.schema import NycuOsccSchema


def get_dirs(py_path: str) -> Tuple[str, str]:
    indir = os.path.relpath(path=py_path[:-3], start=os.getcwd())
    basedir = os.path.dirname(indir)
    outdir = os.path.join(basedir, 'outdir')
    return indir, outdir


class TestCase(unittest.TestCase):

    def set_up(self, py_path: str):
        self.indir, self.outdir = get_dirs(py_path=py_path)
        os.makedirs(self.outdir, exist_ok=True)
        self.schema = NycuOsccSchema

    def tear_down(self):
        shutil.rmtree(self.outdir)

    def assertFileEqual(self, first: str, second: str):
        with open(first) as fh1:
            with open(second) as fh2:
                self.assertEqual(fh1.read(), fh2.read())

    def assertDataFrameEqual(self, first: pd.DataFrame, second: pd.DataFrame):
        self.assertListEqual(list(first.columns), list(second.columns))
        self.assertListEqual(list(first.index), list(second.index))
        for c in first.columns:
            for i in first.index:
                a, b = first.loc[i, c], second.loc[i, c]
                if pd.isna(a) and pd.isna(b):
                    continue
                self.assertAlmostEqual(a, b)

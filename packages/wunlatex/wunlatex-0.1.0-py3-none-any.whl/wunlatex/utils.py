import collections
import os
import shutil
from pathlib import Path

import pandas as pd


def copy_and_overwrite(from_path: Path, to_path: Path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path.parent)
    os.makedirs(to_path)
    shutil.copy2(from_path, to_path / from_path.name)


class Pandas2Latex:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.col_n_lvl = df.columns.nlevels
        self.index_n_lvl = self.df.index.nlevels

    def create_multicolumns(self, roots, lvl, lst):
        lst[lvl] += (self.index_n_lvl - 1) * "&"
        for root in roots:
            count_dict = collections.Counter(self.df[[root]].columns.get_level_values(lvl))
            for name, n in count_dict.items():
                lst[lvl] += " & \\multicolumn{{{}}}{{c}}{{{}}}".format(n, name)
        lst[lvl] += " \\\\\n"

        lvl += 1
        if lvl < self.col_n_lvl:
            self.create_multicolumns(roots, lvl, lst)

    def write_tex(self, caption: str, long: bool = False, **kwargs):
        if long:
            return self.df.to_latex(**kwargs)
        col_idx = "".join(["l"] * self.index_n_lvl)
        tex = ""
        tex += "\\begin{table}[H]\\tiny\n"
        tex += "\\centering\n"
        tex += "\\caption{{{}}}\n".format(caption)
        tex += "\\begin{adjustbox}{max width=\\textwidth}\n"
        tex += "\\begin{{tabular}}{{{}|".format(col_idx) + "".join(["r"] * self.df.shape[1]) + "}\n"

        tex += "\\toprule \n"

        multi = [""] * self.col_n_lvl
        roots = self.df.columns.unique(0)
        lvl = 0
        self.create_multicolumns(roots, lvl, multi)
        for line in multi:
            tex += line

        tex += "\\midrule \n"

        for idx, row in self.df.iterrows():
            if isinstance(idx, tuple):
                idx = " & ".join(idx)
            elif not isinstance(idx, str):
                idx = str(idx)
            tex += idx + " & " + " & ".join([str(x) for x in row.values.tolist()]) + "\\\\\n"
        tex += "\\bottomrule \n"
        tex += "\\end{tabular}\n"
        tex += "\\end{adjustbox}\n"
        tex += "\\end{table}\n"

        return tex

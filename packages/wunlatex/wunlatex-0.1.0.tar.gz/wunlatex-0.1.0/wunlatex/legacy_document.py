import collections
import os
import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd

from wunlatex.utils import copy_and_overwrite, Pandas2Latex


class LegacyDocument:
    def __init__(self, name: str) -> None:
        self.tex = ""
        self.background_color = 1, 1, 1
        self.name = name
        self.template_name = "template.tex"
        self.pdf_cmd = "pdflatex"  # Mac
        self.cmd_params = "--synctex=1"  # Mac
        
    def compile(self, pdf_path: Path, filename: str, date: datetime = None):
        temp_path = pdf_path / "tmp_report"
        tex_path = temp_path / "latex"
        
        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)

        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
            
        os.makedirs(temp_path)
        os.makedirs(tex_path)
        
        copy_and_overwrite(Path(__file__).parent / "templates", tex_path)
        
        self.tex = "\\fancyhead[L]{{{}}}\n".format(self.name) + self.tex
        
        r, g, b = self.background_color
        
        with open(tex_path / "core.tex", "w") as f:
            self.tex = """
\definecolor{bg}{rgb}{""" + f"{r}, {g}, {b}" + """}
\pagecolor{bg}
            """ + self.tex
            f.write(self.tex)

        run_tex = f'{self.pdf_cmd} {self.cmd_params} {self.template_name}'
        tex_directory = str(tex_path)
        cmd_line = "cd " + " && ".join((tex_directory.replace('\\', '/'), run_tex))
        os.system(cmd_line)
        
        if date:
            pdf_path = pdf_path / f"{date.date()}"
            if not os.path.exists(pdf_path):
                os.makedirs(pdf_path)
        
        pdf_name = self.template_name.replace("tex", "pdf")
        shutil.move(tex_path / pdf_name, pdf_path/pdf_name)
        shutil.rmtree(temp_path)
        
        full_filename = f"{filename}_{datetime.now().strftime('%Y%m%d_%H_%M%S')}.pdf"
        os.rename(pdf_path / pdf_name, pdf_path/full_filename)
        
    def add_section(self, name: str):
        tex = "\\section{{{}}}\n".format(name.replace("_", " "))
        self.tex += tex
        
    def add_subsection(self, name: str):
        tex = "\\subsection{{{}}}\n".format(name.replace("_", " "))
        self.tex += tex
        
    def add_figure(self, figure_path: Path, scale: float):
        tex = "\\begin{figure}[H]\n"
        tex += "\\centering\n"
        tex += "\\includegraphics[scale={}]{{{}}}\n".format(
            scale, str(figure_path).replace('\\', '/')
        )
        tex += "\\end{figure}\n"
        self.tex += tex
        
    def add_text(self, text: str):
        self.tex += text
        
    def newline(self):
        self.tex += "\\newline\n"
        
    def newpage(self):
        self.tex += "\\newpage\n"
        
    def add_table(self, df: pd.DataFrame, caption: str = "", long: bool = False, **kwargs):
        self.tex += Pandas2Latex(df).write_tex(caption=caption, long=long, **kwargs)


import os
import shutil
from datetime import datetime
from pathlib import Path

from wuncolors import Color, RGB

from wunlatex.components import Section, Component
from wunlatex.utils import copy_and_overwrite


class Document(Section):
    def __init__(self, name: str, components: list[Component] | None = None, template_path: str | Path | None = None) -> None:
        super().__init__(name=name, components=components)
        self.background_color = Color("White", RGB(255, 255, 255))
        self.name = name
        self.template_path = template_path or Path(__file__).parent / "templates" / "template.tex"
        self.pdf_cmd: str = "pdflatex"  # Mac
        self.cmd_params: str = "--synctex=1"  # Mac

    def to_tex(self, **kwargs) -> str:
        tex = ""
        for component in self.components:
            tex += component.to_tex()
        return tex

    def compile(self, pdf_path: Path, filename: str, timestamp_suffix: bool = False):
        tex_str = self.to_tex()

        temp_path = pdf_path / "tmp_report"
        tex_path = temp_path / "latex"

        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)

        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)

        os.makedirs(temp_path)
        os.makedirs(tex_path)

        if not self.template_path.is_file() or self.template_path.name[-4:] != ".tex":
            raise ValueError(f"Template path ({self.template_path}) is not a file or is not a .tex file")

        template_name = self.template_path.name

        copy_and_overwrite(self.template_path, tex_path)

        tex_str = "\\fancyhead[L]{{{}}}\n".format(self.name) + tex_str

        r, g, b = self.background_color.decimal_rgb()

        with open(tex_path / "core.tex", "w") as f:
            tex_str = """
\definecolor{bg}{rgb}{""" + f"{r}, {g}, {b}" + """}
\pagecolor{bg}
            """ + tex_str
            f.write(tex_str)

        run_tex = f'{self.pdf_cmd} {self.cmd_params} {template_name}'
        tex_directory = str(tex_path)
        cmd_line = "cd " + " && ".join((tex_directory.replace('\\', '/'), run_tex))
        os.system(cmd_line)

        pdf_name = template_name.replace("tex", "pdf")
        shutil.move(tex_path / pdf_name, pdf_path / pdf_name)
        shutil.rmtree(temp_path)

        suffix = "" if not timestamp_suffix else f"_{datetime.now().strftime('%Y%m%d_%H_%M%S')}"
        full_filename = f"{filename}{suffix}.pdf"
        os.rename(pdf_path / pdf_name, pdf_path / full_filename)

from pathlib import Path

import pandas as pd

from wunlatex.utils import Pandas2Latex


class Component:
    def __init__(self, name: str):
        self.name = name

    def to_tex(self, **kwargs) -> str:
        ...

    def fmt_name(self) -> str:
        return self.name.replace("_", "")


class Table(Component):
    def __init__(self, name: str, df: pd.DataFrame):
        super().__init__(name)
        self.df = df

    def to_tex(self) -> str:
        return Pandas2Latex(self.df).write_tex(caption=self.name, long=False)


class Figure(Component):
    def __init__(self, name: str, path: Path | str, scale: float | int = 1.):
        super().__init__(name)
        self.path = path
        self.scale = scale

    def to_tex(self, **kwargs) -> str:
        tex = "\\begin{figure}[H]\n"
        tex += "\\centering\n"
        tex += "\\includegraphics[scale={}]{{{}}}\n".format(
            self.scale, str(self.path).replace('\\', '/')
        )
        tex += "\\end{figure}\n"
        return tex


class Section(Component):
    def __init__(self, name: str, components: list[Component] | None = None):
        super().__init__(name)
        self.components = components or []

    def to_tex(self, **kwargs) -> str:
        lvl = kwargs.get("level", "section")
        tex = f"\\begin" + "{" + lvl + "}" + "{" + self.fmt_name() + "}"
        for component in self.components:
            if isinstance(component, Section):
                tex += component.to_tex(level="sub"+lvl)
            else:
                tex += component.to_tex()
        return tex + "\\end" + "{" + lvl + "}"

    def add_component(self, component: Component):
        self.components.append(component)



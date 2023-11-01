# wunlatex

Library for LaTeX document writing

```python
from pathlib import Path

import wunlatex
import pandas as pd
from matplotlib import pyplot as plt


doc = wunlatex.Document("Test")

df = pd.DataFrame([(1, 2, 3 , 4)], columns=["One", "JJJ", "LKAS", "ONENEE"])
tbl = wunlatex.components.Table("Random Numbers", df)
doc.add_component(tbl)

# Sections within other sections are subsections, then subsubsections etc.
doc.add_component(
    wunlatex.components.Section("First", components=[
        wunlatex.components.Section("Subsection 1", components=[tbl]),
        wunlatex.components.Section("Subsection 2", components=[
            wunlatex.components.Section("SubSubSection 3")
        ])
    ])
)

fig, ax = plt.subplots()
ax.plot([1, 1], [0, 1])
figname = Path(__file__).parent / "testfig.png"
plt.savefig(figname)
f = wunlatex.components.Figure("Test Fig", path=figname)
doc.add_component(f)

doc.compile(Path(__file__).parent, filename="Testpdf.pdf")
```
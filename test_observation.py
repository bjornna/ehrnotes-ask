# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from app.classifiy import observation
from app.train import main
import spacy

from tabulate import tabulate
from spacy import displacy

nlp = main.load_spacy()
doc = nlp("Temperatur: 45 C")
extr = observation.ObservationExtractor(doc)
print(extr.extract_observations())

# %%
corpuses = ["BT: 120/80 mmHg", "Puls 40 /min", "Temp: 39 C"]
for corpus in corpuses:
    print("\n----")
    print(f"## {corpus} ## ")
    doc = nlp(corpus)
    extr = observation.ObservationExtractor(doc, True)
    print("|- Observations")
    print(extr.extract_observations())
    print("|- Explore ")
    print(extr.explore())


# %%

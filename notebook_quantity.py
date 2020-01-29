# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import spacy
import main
from tabulate import tabulate
from spacy import displacy

nlp = main.load_spacy()


# %%
def explore(doc):
    result = [
        {"start": ent.start_char, "end": ent.end_char,
         "label": ent.label_, "id": ent.ent_id_, "text": ent.text}
        for ent in doc.ents
    ]
    print(tabulate(result))


def emit(doc):
    print(doc)


def sentence(doc):
    for sent in doc.sents:
        print(sent.text)


def noun_chunks(doc):
    print("NOUN CHECKS - START")
    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.text,
              chunk.root.dep_, chunk.root.head.text)
    print("NOUN CHECKS - END ")


def tokens_doc(doc):
    for token in doc:
        print(token.text, token.dep_, token.head.text,
              token.head.pos_, [child for child in token.children])


# %%
def extract_quantity(doc):
    print("Go")
    for ent in doc.ents:
        if "OBSERVATION"in ent.label_:
            print("Found observation")
            head = ent.root.head
            rs = head.rights
            print(rs)


# %%

table_format = "psql"  # plain, html, grid, github,


def extract_observations(doc, debug=False):

    S_COLLECT_OBSERVATION = 0
    S_START_OBSERVATION = 1
    S_INIT = -1
    state = S_INIT
    obs = None
    obs_val = None
    obs_unit = None
    table = []
    observations = []
    for n in doc:
        table.append([n.text, n.ent_iob_, n.ent_type_,
                      n.ent_id_, n.pos_, n.tag_])
        ent = n.ent_iob_
        ent_type = n.ent_type_
        ent_id = n.ent_id_
        if "B" == ent and "OBSERVATION" == ent_type:
            state = S_START_OBSERVATION
            if obs:
                if debug:
                    print(f"Previous was {obs} = {obs_val} {obs_unit}")
                observations.append([obs, obs_val, obs_unit])

            obs = ent_id

            obs_val = None
            obs_unit = None
            if debug:
                print(f"Start observation {obs}")
        elif "I" == ent:
            state = S_START_OBSERVATION
        else:
            if state == S_START_OBSERVATION:
                state = S_COLLECT_OBSERVATION
                if debug:
                    print(f"Collect obs {obs}")
                if "NUM" == n.pos_:
                    obs_val = n.text
                if "UNIT" == ent_type:
                    obs_unit = n.text

            elif state == S_COLLECT_OBSERVATION:
                if debug:
                    print(f"Collect obs {obs}")
                if "NUM" == n.pos_:
                    obs_val = n.text
                if "UNIT" == ent_type:
                    obs_unit = n.text

    observations.append([obs, obs_val, obs_unit])
    return [observations, table]


# %%
def write_results(result, PRINT_OBSERVATIONS=True, PRINT_NLP_TABLE=True):
    observations = result[0]
    table = result[1]

    if PRINT_OBSERVATIONS:
        print(tabulate(observations, headers=[
              "ID", "VALUE", "UNIT"], tablefmt=table_format))

    if PRINT_NLP_TABLE:
        print(tabulate(table, headers=[
              "Text", "Ent", "Type", "Pos", "Speech", "Speech details"], tablefmt=table_format))


# %%

doc = nlp("Puls: 72 regelmessig. BP 120/80 mmHg. Temp 38 C. Resp. 45.  Smerte i venstre skulder. Redd for å dø. Ernæring må passes på.")
result = extract_observations(doc, False)
write_results(result, True, False)


# %%
doc = nlp("Puls: 60 /min regelmessig. BP 120/80  mmHg. Temp 38 C. Resp. 22.")
result = extract_observations(doc, False)
write_results(result, True, False)


# %%
doc = nlp("Hun kommer nå inn etter å ha hatt feber siste dagene, også svettetokter. Har målt temperatur så høy som 39,5 C . Nå afebril, men virker varm.")
result = extract_observations(doc, False)
write_results(result, True, False)
print("  ENTITETER   ")
explore(doc)
print(" DISPLACY  ")
displacy.render(doc, style="ent")


# %%
doc = nlp("Pasienten har feber fordi temp er 37")
result = extract_observations(doc, False)
write_results(result, True, False)
explore(doc)


# %%
corpus = """Pasient med langtkomment malignt melanom, innlegges grunnet redusert allmenntilstand og feber. Man mistenker infeksjon, muligens etter et gammelt sår hvor det i september var innlagt plauradren som det da gikk infeksjon i. Vi har funn av gule stafylokokker i sårsekretet, samme som sist gang. Hun ble behandet med cloxacillin og 	, med god effekt av behandlingen. Satt på Bactrim før utreise, skal ha dette i 2 uker. Transfundert med blod 2 ganger under oppholdet grunnet kjent kronisk anemi. Hb 10.3 ved utreise, stabilt økende. Hun ble jevnlig tilsett palliativt team under oppholdet grunnet kvalme.
Hun reiser til eget hjem for palliativ behandling i regi av kommunen, dette etter eget ønske.

Temperatur er 39,2  . 

Medikamenter:
Simvastatin 20mg x1 vesp
Laktulose 15ml x2
Paracet 1gr x4
Bactrim 2tbl x2 i 2 uker
"""
doc = nlp(corpus)
result = extract_observations(doc, False)
write_results(result, True, False)
# explore(doc)
displacy.render(doc, style="ent")


# %%

corpus = """
Sterke smerter fra venstre kne etter fall. 
Blødende sår på leggen medio distalt.
"""
doc = nlp(corpus)
result = extract_observations(doc, False)
write_results(result, True, False)
out = []
for d in doc:
    out.append([repr(d), d.lemma_, d.ent_type_])
print(tabulate(out, headers=["Org", "Lemma", "Ent"]))
displacy.render(doc, style="ent")

# %%
corpus = """
Fiktiv Pasientcase skrevet av Linn

Dame 78 år

09. November 2011
Epikrise
A49.9 Bakterieinfeksjon
C43.5 Malignt melanom, flere lokalisasjoner
N19   Nyresvikt
Z51.5 Palliativ behandling

|
"""

# %%

doc = nlp(corpus)
displacy.render(doc, style="ent")

# %%
doc = nlp("""
Kommer med temperatur på 38 C .
Måler puls til 55.
""")
displacy.render(doc, style="ent")
#displacy.render(doc, style="dep")
arr = []
for token in doc:
    tt = (f"{token.i}", token.text)
    print(tt)

tabulate(arr)

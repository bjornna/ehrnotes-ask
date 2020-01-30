from fastapi import FastAPI
import spacy
from spacy.matcher import Matcher
from app.train import main
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from IPython.core.display import display, HTML
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = main.load_spacy()


class Query(BaseModel):
    corpus: str


def get_model_desc(nlp):
    """Get human-readable model name, language name and version."""
    lang_cls = spacy.util.get_lang_class(nlp.lang)
    lang_name = lang_cls.__name__
    model_version = nlp.meta["version"]
    model_name = "nb_core_news_sm"
    return "{} - {} (v{})".format(lang_name, model_name, model_version)


@app.get("/")
def read_root():
    return get_model_desc(nlp)


@app.post("/dep")
def dep(item: Query):
    doc = nlp(item.corpus)
    collapse_punctuation = False
    collapse_phrases = False
    options = {
        "collapse_punct": collapse_punctuation,
        "collapse_phrases": collapse_phrases

    }
    return spacy.displacy.parse_deps(doc, options)


@app.post("/entview")
def dep_view(item: Query):
    doc = nlp(item.corpus)
    html = spacy.displacy.render(doc, style="ent")
    return HTML(html)


@app.post("/ent")
def ent_query(item: Query):
    """Query for entitities in the given attribute corpus. """
    doc = nlp(item.corpus)
    return [
        {"start": ent.start_char, "end": ent.end_char,
         "label": ent.label_, "id": ent.ent_id_, "text": ent.text}
        for ent in doc.ents
    ]

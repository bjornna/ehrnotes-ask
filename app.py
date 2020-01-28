# coding: utf8
from __future__ import unicode_literals

import main
import hug
from hug_middleware_cors import CORSMiddleware
import spacy
from spacy.matcher import Matcher
nlp = main.load_spacy()


def get_model_desc(nlp):
    """Get human-readable model name, language name and version."""
    lang_cls = spacy.util.get_lang_class(nlp.lang)
    lang_name = lang_cls.__name__
    model_version = nlp.meta["version"]
    model_name = "nb_core_news_sm"
    return "{} - {} (v{})".format(lang_name, model_name, model_version)


@hug.get("/model")
def model():
    return get_model_desc(nlp)


@hug.post("/dep")
def dep(
    text: str,
    model: str,
    collapse_punctuation: bool = False,
    collapse_phrases: bool = False,
):
    """Get dependencies for displaCy visualizer."""

    doc = nlp(text)
    options = {
        "collapse_punct": collapse_punctuation,
        "collapse_phrases": collapse_phrases,
    }
    return spacy.displacy.parse_deps(doc, options)


@hug.post("/ent")
def ent(text: str, model: str):
    """Get entities for displaCy ENT visualizer."""

    doc = nlp(text)
    return [
        {"start": ent.start_char, "end": ent.end_char,
            "label": ent.label_, "id": ent.ent_id_, "text": ent.text}
        for ent in doc.ents
    ]

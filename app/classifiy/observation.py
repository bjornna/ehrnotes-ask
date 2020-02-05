from tabulate import tabulate
import spacy
from spacy.tokens import Token


class Observation:
    def __init__(self, id: str,  type=None, quantity=None, unit=None):
        super().__init__()
        self.id = id
        self.type = type
        self.quantity = quantity
        self.unit = unit

    def __repr__(self):
        res = {"id": self.id, "type": self.type,
               "quantity": self.quantity, "unit": self.unit}
        return repr(res)


class ObservationExtractor:
    table_format = "psql"  # plain, html, grid, github,

    def __init__(self, doc, debug=False):
        super().__init__()
        self.doc = doc
        self.debug = debug
        self.observations = []
        self.current_observation: Observation = None

    def extract_observations(self):
        result = []
        for n in self.doc:
            self.handle_token(n)
        self.add_current()
        return self.observations

    def add_current(self):
        if self.current_observation is not None:
            self.observations.append(self.current_observation)
            self.current_observation = None

    def handle_token(self, n):
        ent = n.ent_iob_
        ent_type = n.ent_type_
        ent_id = n.ent_id_
        if self.debug:
            print(f"Handle token n.post={n.pos_}")
        if "B" == ent and "OBSERVATION" == ent_type:
            if self.debug:
                print(
                    f"NEW Observation detected - try add current and start filling the new one")
            self.add_current()
            self.current_observation = Observation(ent_id, ent_type)
        else:
            if self.current_observation is not None:
                if "NUM" == n.pos_:
                    self.current_observation.quantity = n.text
                elif "UNIT" == ent_type:
                    self.current_observation.unit = n.text

    def explore(self):
        """Extract entities from corpus and return a tabular string"""
        result = [
            {"start": ent.start_char, "end": ent.end_char,
             "label": ent.label_, "id": ent.ent_id_, "text": ent.text}
            for ent in self.doc.ents
        ]
        return tabulate(result)


if __name__ == "__main__":
    from app.train import main
    nlp = main.load_spacy()
    doc = nlp("Temperatur: 45 C")
    extr = ObservationExtractor(doc)
    print(extr.extract_observations())

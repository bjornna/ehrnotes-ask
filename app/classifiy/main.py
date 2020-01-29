import spacy
from spacy.tokens import Token, Doc


class HealthTokenizer:

    def __init__(self, doc: Doc):
        super().__init__()
        self.doc = doc

    def tokenize(self):
        for token in self.doc:
            self.handle_token(token)

    def handle_token(self, token: Token):
        if token.ent_iob:
            """IOB code of named entity tag. 
            3 means the token begins an entity, 
            2 means it is outside an entity, 
            1 means it is inside an entity, and 
            0 means no entity tag is set."""
            print(f"{token} is ENTITY {token.ent_iob} --> {token.ent_type_}")

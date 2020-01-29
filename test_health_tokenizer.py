from app.train import main
from app.classifiy.main import HealthTokenizer

nlp = main.load_spacy()
doc = nlp("BT: 180/80 mmHg. Puls: 44")
ht = HealthTokenizer(doc)
ht.tokenize()

import unittest
from app.classifiy import observation
from app.train import main
import spacy

nlp = None


class TestObservationExtractor(unittest.TestCase):

    def assert_observation(self, corpus, id: str, value: str, unit: str):
        """Verify that the corpus has attribute id, value and unit correct"""
        doc = nlp(corpus)
        extr = observation.ObservationExtractor(doc)
        observations = extr.extract_observations()
        self.assertEqual(1, len(observations),
                         "Antall observations skal være 1 ")
        obs: observation.Observation = observations[0]
        self.assertEqual(id, obs.id)
        self.assertEqual(value, obs.quantity)
        self.assertEqual(unit, obs.unit)

    def test_bp_01(self):
        corpus = "BP: 120/80 mmHg"
        self.assert_observation(corpus, "BLOOD_PRESSURE", "120/80", "mmHg")

    def test_temp_01(self):
        """Temperature - NOTE that we do not detect the unit here """
        corpus = "Temp: 39 C"
        self.assert_observation(corpus, "BODY_TEMP", "39", None)


if __name__ == "__main__":
    nlp = main.load_spacy()
    unittest.main()

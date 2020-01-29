
from observation import Observation


def load_nlp():
    print("OK")
    obs = Observation("the given id")
    print(f"Observation.id={obs.id}")


if __name__ == "__main__":

    print("Classify main")
    load_nlp()

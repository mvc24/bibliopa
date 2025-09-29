from rapidfuzz import fuzz
from pathlib import Path
from pprint import pp
import re
import unicodedata



def normalise_text(text):

    text = unicodedata.normalize("NFC", text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()

    # pp(f"text: {text}")
    return text

# normalise_text(t2)

def test_similarity(text1, text2):
    text1 = normalise_text(text1)
    text2 = normalise_text(text2)

    score = fuzz.ratio(text1, text2)
    score_part = fuzz.partial_ratio(text1, text2)
    # print(f"Similarity: {score}")
    # print(f"Similarity part: {score_part}")
    return score
# test_similarity(tColl, tDisc)

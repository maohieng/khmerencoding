
from khmerencoding.encoding import encode_text

def test_encode_text():
    txt = "ខ្ញំុជាស្រ្តីខ្មែរ"
    lang="km"
    assert encode_text(txt, lang) == "ខ្ញុំជាស្ត្រីខ្មែរ"

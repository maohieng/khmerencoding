# Khmer Encoding
Khmer character encoding based on the [khmer character specification](https://github.com/sillsdev/khmer-character-specification).

This work is cloned from [specification's python script](https://github.com/sillsdev/khmer-character-specification/tree/master/python/scripts) to be released as python package.

### Installation
```sh
pip install khmerencoding
```

### Usage
To encode a khmer text.
```python
from khmerencoding import encode_text

text = "ខ្ញំុជាស្រ្តីខ្មែរ" # wrong encoding ordering

encoded_text = encode_text(text)

print(encoded_text) # correct encoding ordering, according to the specification
```

Further more, you can print out each unicode character to see what has been changed, as following:
```python
def get_hex_code_points(sentence):
    """
    Get the Unicode code points of each character in the token.
    """
    return [f"U+{ord(char):04X}" for char in sentence]

text = "ខ្ញំុជាស្រ្តីខ្មែរ"
# Print the text
print(text)

# Print unicode code of each character
print(get_hex_code_points(text))

# Encode the text
encoded_text = encode_text(text)

# Print the encoded text
print(encoded_text)

# Print the unicode code of each encoded character
print(get_hex_code_points(encoded_text))
```

### Contribution
You are welcomed to contribute to this project so long as you abide by the license below. You can either create issues for us to fix or a PR for us to review. 

### License
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Khmer Character Specification/Usages</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://sil.org" property="cc:attributionName" rel="cc:attributionURL">SIL</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
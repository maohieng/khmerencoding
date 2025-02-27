#!/usr/bin/python3
# Copyright (c) 2021-2024, SIL Global.
# Licensed under MIT license: https://opensource.org/licenses/MIT

import enum, re

class Cats(enum.Enum):
    Other = 0; Base = 1; Robat = 2; Coeng = 3;
    Shift = 4; Z = 5; VPre = 6; VB = 7; VA = 8;
    VPost = 9; MS = 10; MF = 11; ZFCoeng = 12

categories =  ([Cats.Base] * 35     # 1780-17A2
            + [Cats.Other] * 2      # 17A3-17A4
            + [Cats.Base] * 15      # 17A5-17B3
            + [Cats.Other] * 2      # 17B4-17B5
            + [Cats.VPost]          # 17B6
            + [Cats.VA] * 4         # 17B7-17BA
            + [Cats.VB] * 3         # 17BB-17BD
            + [Cats.VPre] * 8       # 17BE-17C5
            + [Cats.MS]             # 17C6
            + [Cats.MF] * 2         # 17C7-17C8
            + [Cats.Shift] * 2      # 17C9-17CA
            + [Cats.MS]             # 17CB
            + [Cats.Robat]          # 17CC
            + [Cats.MS] * 5         # 17CD-17D1
            + [Cats.Coeng]          # 17D2
            + [Cats.MS]             # 17D3
            + [Cats.Other] * 9      # 17D4-17DC
            + [Cats.MS])            # 17DD

khres = {   # useful regular sub expressions used later
    # All bases
    "B":       "[\u1780-\u17A2\u17A5-\u17B3\u25CC]",
    # All consonants excluding Ro
    "NonRo":   "[\u1780-\u1799\u179B-\u17A2\u17A5-\u17B3]",
    # All consonants exclude Bo
    "NonBA":   "[\u1780-\u1793\u1795-\u17A2\u17A5-\u17B3]",
    # Series 1 consonants
    "S1":      "[\u1780-\u1783\u1785-\u1788\u178A-\u178D\u178F-\u1792"
               "\u1795-\u1797\u179E-\u17A0\u17A2]",
    # Series 2 consonants
    "S2":      "[\u1784\u1780\u178E\u1793\u1794\u1798-\u179D\u17A1\u17A3-\u17B3]",
    # Simple following Vowel in Modern Khmer
    "VA":      "(?:[\u17B7-\u17BA\u17BE\u17BF\u17DD]|\u17B6\u17C6)",
    # Above vowel (as per shifter rules) with vowel sequences
    "VAX":     "(?:[\u17C1-\u17C5]?{VA})",
    # Above vowel with samyok (modern khmer)
    "VAS":     "(?:{VA}|[\u17C1-\u17C3]?\u17D0)",
    # Above vowel with samyok (middle khmer)
    "VASX":    "(?:{VAX}|[\u17C1-\u17C3]?\u17D0)",
    # Below vowel (with Middle Khmer prefix)
    "VB":      "(?:[\u17C1-\u17C3]?[\u17BB-\u17BD])",
    # contains series 1 and no BA
    "STRONG":  """  {S1}\u17CC?                 # series 1 robat?
                    (?:\u17D2{NonBA}            # nonba coengs
                       (?:\u17D2{NonBA})?)?
                  | {NonBA}\u17CC?              # nonba robat?
                    (?:  \u17D2{S1}               # series 1 coeng
                         (?:\u17D2{NonBA})?       #   + any nonba coeng
                       | \u17D2{NonBA}\u17D2{S1}  # nonba coeng + series 1 coeng
                    )""",
    # contains BA or only series 2
    "NSTRONG": """(?:{S2}\u17CC?(?:\u17D2{S2}(?:\u17D2{S2})?)? # Series 2 + series 2 coengs
                     |\u1794\u17CC?(?:{COENG}(?:{COENG})?)?    # or ba with any coeng
                     |{B}\u17CC?(?:\u17D2{NonRo}\u17D2\u1794   # or ba coeng
                                  |\u17D2\u1794(?:\u17D2{B}))
                  )""",
    "COENG":   "(?:(?:\u17D2{NonRo})?\u17D2{B})",
    # final coeng
    "FCOENG":  "(?:\u200D(?:\u17D2{NonRo})+)",
    # Allowed shifter sequences in Modern Khmer
    "SHIFT":   """(?:  (?<={STRONG}) \u17CA\u200C (?={VA})     # strong + triisap held up
                     | (?<={NSTRONG})\u17C9\u200C (?={VAS})    # weak + muusikatoan held up
                     | [\u17C9\u17CA]                          # any shifter
                  )""",
    # Allowed shifter sequences in Middle Khmer
    "SHIFTX":  """(?:(?<={STRONG}) \u17CA\u200C (?={VAX})      # strong + triisap held up
                    | (?<={NSTRONG})\u17C9\u200C (?={VASX})    # weak + muusikatoan held up
                    | [\u17C9\u17CA]                           # any shifter
                   )""",
    # Modern Khmer vowel
    "V":       "[\u17B6-\u17C5]?",
    # Middle Khmer vowel sequences (not worth trying to unpack this)
    "VX":      "(?:\u17C1[\u17BC\u17BD]?[\u17B7\u17B9\u17BA]?|"
               "[\u17C2\u17C3]?[\u17BC\u17BD]?[\u17B7-\u17BA]\u17B6|"
               "[\u17C2\u17C3]?[\u17BB-\u17BD]?\u17B6|\u17BE[\u17BC\u17BD]?\u17B6?|"
               "[\u17C1-\u17C5]?\u17BB(?![\u17D0\u17DD])|"
               "[\u17BF\u17C0]|[\u17C2-\u17C5]?[\u17BC\u17BD]?[\u17B7-\u17BA]?)",
    # Modern Khmer Modifiers
    "MS":      """(?:(?:  [\u17C6\u17CB\u17CD-\u17CF\u17D1\u17D3]   # follows anything
                       | (?<!\u17BB) [\u17D0\u17DD])                # not after -u
                     [\u17C6\u17CB\u17CD-\u17D1\u17D3\u17DD]?   # And an optional second
                  )""",
    # Middle Khmer Modifiers
    "MSX":     """(?:(?:  [\u17C6\u17CB\u17CD-\u17CF\u17D1\u17D3]   # follows anything
                        | (?<!\u17BB [\u17B6\u17C4\u17C5]?)    # blocking -u sequence
                     [\u17D0\u17DD])                           # for these modifiers
                  [\u17C6\u17CB\u17CD-\u17D1\u17D3\u17DD]?     # And an optional second
                  )"""
}

# expand 3 times: SHIFTX -> VASX -> VAX -> VA
for i in range(3):
    khres = {k: v.format(**khres) for k, v in khres.items()}

def charcat(c):
    ''' Returns the Khmer character category for a single char string'''
    o = ord(c)
    if 0x1780 <= o <= 0x17DD:
        return categories[o-0x1780]
    elif o == 0x200C:
        return Cats.Z
    elif o == 0x200D:
        return Cats.ZFCoeng
    return Cats.Other

def lunar(m, base):
    ''' Returns the lunar date symbol from the appropriate set base '''
    v = (ord(m.group(1) or "\u17E0") - 0x17E0) * 10 + ord(m.group(2)) - 0x17E0
    if v > 15:      # translate \u17D4\u17D2\u17E0 as well
        return m.group(0)
    return chr(v+base)

def encode_text(txt, lang="km"):
    ''' Returns khmer normalised string, without fixing or marking errors'''
    # Mark final coengs in Middle Khmer
    if lang == "xhm":
        txt = re.sub(r"([\u17B6-\u17C5]\u17D2)", "\u200D\\1", txt)
    # Categorise every character in the string
    charcats = [charcat(c) for c in txt]

    # Recategorise base -> coeng after coeng char (or ZFCoeng)
    for i in range(1, len(charcats)):
        if txt[i-1] in "\u200D\u17D2" and charcats[i] in (Cats.Base, Cats.Coeng):
            charcats[i] = charcats[i-1]

    # Find subranges of base+non other and sort components in the subrange
    i = 0
    res = []
    while i < len(charcats):
        c = charcats[i]
        if c != Cats.Base:
            res.append(txt[i])
            i += 1
            continue
        # Scan for end of syllable
        j = i + 1
        while j < len(charcats) and charcats[j].value > Cats.Base.value:
            j += 1
        # Sort syllable based on character categories
        # Sort the char indices by category then position in string
        newindices = sorted(range(i, j), key=lambda e:(charcats[e].value, e))
        replaces = "".join(txt[n] for n in newindices)

        replaces = re.sub("(\u200D?\u17D2)[\u17D2\u200C\u200D]+",
                          r"\1", replaces)      # remove multiple invisible chars
        replaces = re.sub("\u17BE\u17B6", "\u17C4\u17B8", replaces)  # confusable vowels
        # map compoound vowel sequences to compounds with -u before to be converted
        replaces = re.sub("\u17C1([\u17BB-\u17BD]?)\u17B8", "\u17BE\\1", replaces)
        replaces = re.sub("\u17C1([\u17BB-\u17BD]?)\u17B6", "\u17C4\\1", replaces)
        replaces = re.sub("(\u17BE)(\u17BB)", r"\2\1", replaces)
        # Replace -u + upper vowel with consonant shifter
        replaces = re.sub("({STRONG}[\u17C1-\u17C5]?)\u17BB"
                          "(?={VA}|\u17D0)".format(**khres), "\\1\u17CA", replaces, re.X)
        replaces = re.sub("({NSTRONG}[\u17C1-\u17C5]?)\u17BB"
                          "(?={VA}|\u17D0)".format(**khres), "\\1\u17C9", replaces, re.X)
        replaces = re.sub("(\u17D2\u179A)(\u17D2[\u1780-\u17B3])",
                          r"\2\1", replaces)    # coeng ro second
        replaces = re.sub("(\u17D2)\u178A", "\\1\u178F", replaces)  # coeng da->ta
        # convert lunar dates from old style to use lunar date symbols
        replaces = re.sub("(\u17E1?)([\u17E0-\u17E9])\u17D2\u17D4",
                lambda m:lunar(m, 0x19E0), replaces)
        replaces = re.sub("\u17D4\u17D2(\u17E1?)([\u17E0-\u17E9])",
                lambda m:lunar(m, 0x19F0), replaces)
        replaces = re.sub("\u17D4\u17D2\u17D4", "\u19F0", replaces)
        res.append(replaces)
        i = j
    return "".join(res)

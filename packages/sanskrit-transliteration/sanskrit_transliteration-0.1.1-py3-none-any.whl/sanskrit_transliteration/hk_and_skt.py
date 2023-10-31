from .from_skt import FromSkt


class HkAndSkt:
    __HK_CONSONANTS_DICT = {
        "k": "क",
        "g": "ग",
        "G": "ङ",
        "c": "च",
        "ch": "छ",
        "j": "ज",
        "jh": "झ",
        "J": "ञ",
        "th": "थ",
        "dh": "ध",
        "T": "ट",
        "Th": "ठ",
        "D": "ड",
        "Dh": 'ढ',
        "N": "ण",
        "t": "त",
        "d": "द",
        "n": "न",
        "p": "प",
        "b": "ब",
        "bh": "भ",
        "ph": "फ",
        "m": "म",
        "y": "य",
        "r": "र",
        "l": "ल",
        "v": "व",
        "z": "श",
        "S": "ष",
        "s": "स",
        "h": "ह",
    }

    __HK_VOWEL_MARKER_DICT = {
        'a': '',
        'A': 'ा',
        'i': 'ि',
        'I': 'ी',
        'u': 'ु',
        'U': 'ू',
        'R': 'ृ',
        'e': 'े',
        'o': 'ो',
        "RR": "ॄ",
    }

    __HK_NASAL_DICT = {
        "H": "ः",
        "M": "ं"
    }

    __HK_VOWELS_DICT = {
        "a": "अ",
        "A": "आ",
        "i": "इ",
        "I": "ई",
        "u": "उ",
        "U": "ऊ",
        "R": "ऋ",
        "RR": "ॠ",
        "e": "ए",
        "ai": "ऐ",
        "o": "ओ",
        "au": "औ"
    }

    __HK_NUMBERS_DICT = {
        "0": "०",
        "1": "१",
        "2": "२",
        "3": "३",
        "4": "४",
        "5": "५",
        "6": "६",
        "7": "७",
        "8": "८",
        "9": "९"
    }

    __REM_CHAR_DICT = {
        **__HK_NUMBERS_DICT,
        **__HK_NASAL_DICT,
        **{"|": "।", "\'": "ऽ"}
    }

    @staticmethod
    def hk_to_skt(text: str):
        text_len, res, idx = len(text), [], 0
        while idx < text_len:
            ch = text[idx]
            prev_ch, nxt_ch = None, None
            if idx + 1 < text_len:
                nxt_ch = text[idx + 1]
            if idx > 0:
                prev_ch = text[idx - 1]
            # potential aspirates
            if ch in ["k", "g", "c", "j", "t", "d", "T", "D", "p", "b"]:
                # if character is an aspirate
                if prev_ch in HkAndSkt.__HK_CONSONANTS_DICT:
                    res.append('्')
                if nxt_ch == "h":
                    res.append(
                        HkAndSkt.__HK_CONSONANTS_DICT[ch + nxt_ch]
                    )
                    idx += 1
                # if not an aspirate
                else:
                    res.append(
                        HkAndSkt.__HK_CONSONANTS_DICT[ch]
                    )
            # remaining consonants
            elif ch in HkAndSkt.__HK_CONSONANTS_DICT:
                if prev_ch and prev_ch in HkAndSkt.__HK_CONSONANTS_DICT:
                    res.append('्')
                res.append(HkAndSkt.__HK_CONSONANTS_DICT[ch])
            # check vowels
            elif ch in HkAndSkt.__HK_VOWELS_DICT:
                # if prev character is a consonant
                if prev_ch in HkAndSkt.__HK_CONSONANTS_DICT:
                    if (ch == "a" and nxt_ch in ["i", "u"]) or (ch == "R" == nxt_ch):
                        res.append(HkAndSkt.__HK_VOWEL_MARKER_DICT[ch + nxt_ch])
                        idx += 1
                    else:
                        res.append(HkAndSkt.__HK_VOWEL_MARKER_DICT[ch])
                # if prev character not a consonant
                elif prev_ch not in HkAndSkt.__HK_CONSONANTS_DICT:
                    # for diphthongs
                    if (ch == "a" and nxt_ch in ["i", "u"]) or (ch == "R" == nxt_ch):
                        res.append(HkAndSkt.__HK_VOWELS_DICT[ch + nxt_ch])
                        idx += 1
                    # if not diphthong
                    # then print normally
                    else:
                        res.append(HkAndSkt.__HK_VOWELS_DICT[ch])
            # rest of the characters if they appear convert them
            elif ch in HkAndSkt.__REM_CHAR_DICT:
                if prev_ch and prev_ch in HkAndSkt.__HK_CONSONANTS_DICT:
                    res.append('्')
                res.append(
                    HkAndSkt.__REM_CHAR_DICT[ch]
                )
            # rest of the characters if they don't appear
            # print as it is
            else:
                if prev_ch and prev_ch in HkAndSkt.__HK_CONSONANTS_DICT:
                    res.append('्')
                res.append(ch)
            idx += 1
        # if final char is a consonant then take the halanta
        if text[-1] in HkAndSkt.__HK_CONSONANTS_DICT:
            res.append('्')
        return ''.join(res)

    @staticmethod
    def skt_to_hk(text: str):
        return FromSkt.transliterate_from_skt(scheme="HK", text=text)

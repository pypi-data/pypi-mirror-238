from .from_skt import FromSkt


class WxSlp1Skt:
    __CONSONANTS_DICT = {
        "k": "क",
        "K": "ख",
        "g": "ग",
        "G": "घ",
        "c": "च",
        "C": "छ",
        "j": "ज",
        "J": "झ",
        "n": "न",
        "p": "प",
        "P": "फ",
        "b": "ब",
        "B": "भ",
        "m": "म",
        "y": "य",
        "r": "र",
        "l": "ल",
        "v": "व",
        "S": "श",
        "s": "स",
        "h": "ह",
    }

    __NASAL_DICT = {
        "H": "ः",
        "M": "ं"
    }

    __VOWEL_MARKER_DICT = {
        'A': 'ा',
        'i': 'ि',
        'I': 'ी',
        'u': 'ु',
        'U': 'ू',
        'e': 'े',
        'E': 'ै',
        'o': 'ो',
        'O': 'ौ',
    }

    __VOWELS_DICT = {
        "a": "अ",
        "A": "ा",
        "i": "इ",
        'I': 'ई',
        "u": "उ",
        'U': "ऊ",
        "e": "ए",
        'E': "ऐ",
        "o": "ओ",
        'O': 'औ',
        'q': 'ऋ',
        'Q': 'ॠ'
    }

    __NUMBERS_DICT = {
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
        **__NASAL_DICT,
        **__NUMBERS_DICT,
        **{".": "।"}
    }

    @staticmethod
    def wx_slp1_to_skt(text: str, from_scheme):
        __consonants, __vowels, __vowel_markers, __rem_chars = {}, {}, {}, {}
        if from_scheme == "WX":
            __consonants = {
                **WxSlp1Skt.__CONSONANTS_DICT,
                **{
                    "f": "ङ",
                    "F": "ञ",
                    "x": "द",
                    "X": "ध",
                    "t": "ट",
                    "w": "त",
                    "W": "थ",
                    "T": "ठ",
                    "N": "ण",
                    "d": "ड",
                    "D": "ढ",
                    "R": "ष",
                },
            }
            __vowels = {
                **WxSlp1Skt.__VOWELS_DICT,
                **{
                    'q': 'ऋ',
                    'Q': 'ॠ'
                }

            }
            __vowel_markers = {
                **WxSlp1Skt.__VOWEL_MARKER_DICT,
                **{
                    'q': 'ृ',
                    'Q': 'ॄ'
                }

            }
            __rem_chars = {
                **WxSlp1Skt.__REM_CHAR_DICT,
                **{"Z": "ऽ"}
            }
        elif from_scheme == "SLP1":
            __consonants = {
                **WxSlp1Skt.__CONSONANTS_DICT,
                **{
                    "N": "ङ",
                    "Y": "ञ",
                    "d": "द",
                    "D": "ध",
                    "t": "त",
                    "T": "थ",
                    "w": "ट",
                    "W": "ठ",
                    "R": "ण",
                    "q": "ड",
                    "Q": "ढ",
                    "z": "ष",
                },

            }
            __vowels = {
                **WxSlp1Skt.__VOWELS_DICT,
                **{
                    'f': 'ऋ',
                    'F': 'ॠ'
                }

            }
            __vowel_markers = {
                **WxSlp1Skt.__VOWEL_MARKER_DICT,
                **{
                    'f': 'ृ',
                    'F': 'ॄ'
                }

            }
            __rem_chars = {
                **WxSlp1Skt.__REM_CHAR_DICT,
                **{"'": "ऽ"}
            }

        text_len, res, idx = len(text), [], 0
        while idx < text_len:
            ch = text[idx]
            prev_ch = None
            if idx > 0:
                prev_ch = text[idx - 1]
            # consonants
            if ch in __consonants:
                if prev_ch and prev_ch in __consonants:
                    res.append('्')
                res.append(__consonants[ch])
            # check vowels
            elif ch in __vowels:
                # if prev character is a consonant
                if prev_ch in __consonants:
                    if ch == "a":
                        pass
                    else:
                        res.append(__vowel_markers[ch])
                # if prev character not a consonant
                elif prev_ch not in __consonants:
                    res.append(__vowels[ch])
            # rest of the characters if they appear convert them
            elif ch in __rem_chars:
                if prev_ch and prev_ch in __consonants:
                    res.append('्')
                res.append(
                    __rem_chars[ch]
                )
            # rest of the characters if they don't appear
            # print as it is
            else:
                if prev_ch and prev_ch in __consonants:
                    res.append('्')
                res.append(ch)
            idx += 1
        # if final char is a consonant then take the halanta
        if text[-1] in __consonants:
            res.append('्')
        return ''.join(res)

    @staticmethod
    def skt_to_wx(text: str):
        return FromSkt.transliterate_from_skt(scheme="WX", text=text)

    @staticmethod
    def skt_to_slp1(text: str):
        return FromSkt.transliterate_from_skt(scheme="SLP1", text=text)


if __name__ == '__main__':
    print(
        WxSlp1Skt.wx_slp1_to_skt(
            text="pArWAya prawiboXiwAM BagavawA nArAyaNena svayam vyAsena graWiwAM purANamuninA maXye mahABArawe",
            from_scheme="WX")
    )

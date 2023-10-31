from .from_skt import FromSkt


class VelSkt:
    __VEL_CONSONANTS_DICT = {
        ".t": "ट",
        ".th": "ठ",
        ".d": "ड",
        ".dh": "ढ",
        ".n": "ण",
        ".s": "ष",
        "k": "क",
        "g": "ग",
        "c": "च",
        "j": "ज",
        "t": "त",
        "th": "थ",
        "d": "द",
        "dh": "ध",
        "n": "न",
        "p": "प",
        "ph": "फ",
        "b": "ब",
        "bh": "भ",
        "m": "म",
        "y": "य",
        "r": "र",
        "l": "ल",
        "v": "व",
        "s": "स",
        "h": "ह",
    }

    __VEL_VOWEL_MARKER_DICT = {
        "a": "",
        'aa': 'ा',
        'i': 'ि',
        'ii': 'ी',
        'uu': 'ू',
        'u': 'ु',
        'e': 'े',
        'o': 'ो',
        'au': 'ौ'
    }

    __VEL_VOWELS_DICT = {
        "a": "अ",
        "ii": "ई",
        "aa": "आ",
        "i": "इ",
        "u": "उ",
        "uu": "ऊ",
        "e": "ए",
        "o": "ओ",
        'au': 'औ'
    }

    __VEL_NUMBERS_DICT = {
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

    @staticmethod
    def __dot_handler(
            nxt_ch: str,
            nxt_nxt_ch: str,
            i: int,
            prev_ch: str,
            prev_prev_ch: str,
            prev_prev_prev_ch: str
    ):
        res_ch = ""
        if nxt_ch is None:
            return "।", i
        dot_ch = "." + nxt_ch
        if nxt_ch == "r":
            if nxt_nxt_ch == "r":
                i += 2
                res_ch = 'ॄ' if prev_ch in VelSkt.__VEL_CONSONANTS_DICT else "ॠ"
            else:
                i += 1
                res_ch = 'ृ' if prev_ch in VelSkt.__VEL_CONSONANTS_DICT else "ऋ"
        elif nxt_ch == "h":
            res_ch = "ः"
            i += 1
        elif nxt_ch == "m":
            res_ch = "ं"
            i += 1
        elif nxt_ch == "a":
            res_ch = "ऽ"
            i += 1
        elif nxt_ch in ["t", "d"]:
            if VelSkt.__halant_applies_here(prev_ch, prev_prev_ch, prev_prev_prev_ch):
                res_ch += '्'
            if nxt_nxt_ch == "h":
                i += 2
                res_ch += VelSkt.__VEL_CONSONANTS_DICT[dot_ch + nxt_nxt_ch]
            else:
                i += 1
                res_ch += VelSkt.__VEL_CONSONANTS_DICT.get(dot_ch, nxt_ch)
        elif nxt_ch in ["n", "s"]:
            if VelSkt.__halant_applies_here(prev_ch, prev_prev_ch, prev_prev_prev_ch):
                res_ch = '्'
            i += 1
            res_ch += VelSkt.__VEL_CONSONANTS_DICT[dot_ch]
        else:
            res_ch = '।'
        return res_ch, i

    @staticmethod
    def __halant_applies_here(prev_ch, prev_prev_ch, prev_prev_prev_ch):
        if prev_ch == "r" and prev_prev_ch == "r" and prev_prev_prev_ch == ".":
            return False
        elif (prev_ch == "r" and prev_prev_ch == ".") or \
                (prev_ch == "h" and prev_prev_ch == ".") or \
                (prev_ch == "m" and prev_prev_ch == "."):
            return False
        elif prev_ch in VelSkt.__VEL_CONSONANTS_DICT:
            return True
        else:
            return False

    @staticmethod
    def __get_vowel(ch, nxt_ch, idx, vowel_chars):
        if ch == "a" and nxt_ch in ["a", "i", "u"]:
            res_ch = vowel_chars[ch + nxt_ch]
            idx += 1
        elif (ch == "i" == nxt_ch) or (ch == "u" == nxt_ch) or (ch == "a" == nxt_ch):
            res_ch = vowel_chars[ch + nxt_ch]
            idx += 1
        else:
            res_ch = vowel_chars[ch]
        return res_ch, idx

    @staticmethod
    def vel_to_skt(text: str):
        text_len, cres, idx = len(text), [], 0
        while idx < text_len:
            ch = text[idx]
            prev_ch, nxt_ch, nxt_nxt_ch = None, None, None
            prev_prev_ch, prev_prev_prev_ch = None, None
            if idx + 1 < text_len:
                nxt_ch = text[idx + 1]
            if idx + 2 < text_len:
                nxt_nxt_ch = text[idx + 2]
            if idx > 0:
                prev_ch = text[idx - 1]
            if idx > 1:
                prev_prev_ch = text[idx - 2]
            if idx > 2:
                prev_prev_prev_ch = text[idx - 3]
            # dot alphabets
            if ch == ".":
                res_ch, idx = VelSkt.__dot_handler(
                    nxt_ch,
                    nxt_nxt_ch,
                    idx,
                    prev_ch,
                    prev_prev_ch,
                    prev_prev_prev_ch
                )
                cres.append(res_ch)
            # if ch is a quote
            elif ch == '"':
                # halanta
                if prev_ch in VelSkt.__VEL_CONSONANTS_DICT:
                    cres.append('्')
                # palatal fricative
                if nxt_ch == "s":
                    cres.append("श")
                    idx += 1
                elif nxt_ch == "n":
                    cres.append("ङ")
                    idx += 1
                else:
                    cres.append('"')
            elif ch == '~':
                # halanta
                if prev_ch in VelSkt.__VEL_CONSONANTS_DICT:
                    cres.append('्')
                if nxt_ch == "n":
                    cres.append("ञ")
                    idx += 1
                else:
                    cres.append('"')
            # non retroflex consonants
            elif ch in ["k", "g", "c", "j", "t", "d", "p", "b"]:
                # halanta
                if VelSkt.__halant_applies_here(prev_ch, prev_prev_ch, prev_prev_prev_ch):
                    cres.append('्')
                # aspirates
                if nxt_ch == "h":
                    cres.append(VelSkt.__VEL_CONSONANTS_DICT[ch + nxt_ch])
                    idx += 1
                # if not an aspirate
                else:
                    cres.append(VelSkt.__VEL_CONSONANTS_DICT[ch])
            # remaining consonants
            elif ch in VelSkt.__VEL_CONSONANTS_DICT:
                if VelSkt.__halant_applies_here(prev_ch, prev_prev_ch, prev_prev_prev_ch):
                    cres.append('्')
                cres.append(VelSkt.__VEL_CONSONANTS_DICT[ch])
            # check vowels
            elif ch in VelSkt.__VEL_VOWELS_DICT:
                # if prev character is a consonant
                if prev_ch in VelSkt.__VEL_CONSONANTS_DICT:
                    res_ch, idx = VelSkt.__get_vowel(ch, nxt_ch, idx, VelSkt.__VEL_VOWEL_MARKER_DICT)
                    cres.append(res_ch)
                # if prev character not a consonant
                elif prev_ch not in VelSkt.__VEL_CONSONANTS_DICT:
                    res_ch, idx = VelSkt.__get_vowel(ch, nxt_ch, idx, VelSkt.__VEL_VOWELS_DICT)
                    cres.append(res_ch)
            # rest of the characters if they appear convert them
            elif ch in VelSkt.__VEL_NUMBERS_DICT:
                if VelSkt.__halant_applies_here(prev_ch, prev_prev_ch, prev_prev_prev_ch):
                    cres.append('्')
                cres.append(
                    VelSkt.__VEL_NUMBERS_DICT[ch]
                )
            # rest of the characters if they don't appear
            # print as it is
            else:
                if VelSkt.__halant_applies_here(prev_ch, prev_prev_ch, prev_prev_prev_ch):
                    cres.append('्')
                cres.append(ch)
            idx += 1
        # if final char is a consonant then take the halanta
        prev_ch, prev_prev_ch, prev_prev_prev_ch = None, None, None
        if idx > 0:
            prev_ch = text[idx - 1]
        if idx > 1:
            prev_prev_ch = text[idx - 2]
        if idx > 2:
            prev_prev_prev_ch = text[idx - 3]
        if VelSkt.__halant_applies_here(prev_ch, prev_prev_ch, prev_prev_prev_ch):
            # if text[-1] in VelSkt.__VEL_CONSONANTS_DICT:
            cres.append('्')
        return ''.join(cres)

    @staticmethod
    def skt_to_vel(text: str):
        return FromSkt.transliterate_from_skt(scheme="VELTHIUS", text=text)


if __name__ == '__main__':
    res = VelSkt.vel_to_skt('.dhu.n.dhikaa.api')
    print(res)
    print(
        res == "रामः इव, १२३।"
    )

from functools import partial
from .utils import get_dict_value


class WxSlp1Hk:
    @staticmethod
    def hk_to_wx_or_slp1(text, to_scheme):
        replacements = {
            "'": {"WX": "Z", "SLP1": "'"},
            "ch": "C",
            "dh": {"WX": "X", "SLP1": "D"},
            "ai": "E",
            "au": "O",
            "Th": {"WX": "T", "SLP1": "W"},
            "T": {"WX": "t", "SLP1": "w"},
            "ph": "P",
            "bh": "B",
            "N": {"WX": "N", "SLP1": "R"},
            "D": {"WX": "d", "SLP1": "q"},
            "Dh": {"WX": "D", "SLP1": "Q"},
            "th": {"WX": "W", "SLP1": "T"},
            "kh": "K",
            "G": {"WX": "f", "SLP1": "N"},
            "gh": "G",
            "d": {"WX": "x", "SLP1": "d"},
            "t": {"WX": "w", "SLP1": "t"},
            "R": {"WX": "q", "SLP1": "f"},
            "J": {"WX": "F", "SLP1": "Y"},
            "jh": "J",
            "S": {"WX": "R", "SLP1": "z"},
            "z": "S",
            "|": "."
        }
        res, i, text_len = [], 0, len(text)
        _rep = partial(
            get_dict_value,
            to_scheme,
            replacements
        )

        while i < text_len:
            ch, nxt_ch = text[i], None
            if i < text_len - 1:
                nxt_ch = text[i + 1]
            if ch in ["c", "d", "T", "p", "b", "D", "t", "k", "g", "j"]:
                if nxt_ch == "h":
                    res.append(_rep(ch + nxt_ch))
                    i += 1
                else:
                    res.append(_rep(ch))
            elif ch == "a" and nxt_ch in ["i", "u"]:
                res.append(_rep(ch + nxt_ch))
                i += 1
            elif ch == "R" and nxt_ch == "R":
                if to_scheme == "WX":
                    res.append("Q")
                elif to_scheme == "SLP1":
                    res.append("F")
                i += 1
            else:
                res.append(_rep(ch))
            i += 1
        return ''.join(res)

    @staticmethod
    def wx_to_hk(text):
        replacements = {
            "Z": "'",
            "J": "jh",
            "C": "ch",
            'X': 'dh',
            'E': 'ai',
            'O': 'au',
            'T': 'Th',
            't': 'T',
            'P': 'ph',
            'B': 'bh',
            'D': 'Dh',
            'W': 'th',
            'K': 'kh',
            'G': 'gh',
            'f': 'G',
            'x': 'd',
            'w': 't',
            'q': 'R',
            'Q': 'RR',
            'F': 'J',
            'S': 'z',
            'R': 'S',
            '.': '|'
        }
        res = [replacements.get(ch, ch) for ch in text]
        return ''.join(res)

    @staticmethod
    def slp1_to_hk(text):
        replacements = {
            "J": "jh",
            "C": "ch",
            'N': 'G',
            'D': 'dh',
            'E': 'ai',
            'O': 'au',
            'T': 'th',
            't': 't',
            'P': 'ph',
            'B': 'bh',
            'W': 'Th',
            'K': 'kh',
            'G': 'gh',
            'f': 'R',
            'w': 'T',
            'q': 'D',
            'Q': 'Dh',
            'F': 'RR',
            'S': 'z',
            'R': 'N',
            '.': '|',
            'z': 'S',
            'Y': 'J'
        }
        res = [replacements.get(ch, ch) for ch in text]
        return ''.join(res)

from functools import partial
from .utils import get_dict_value


class WxSlp1Vel:
    @staticmethod
    def vel_to_wx_or_slp1(text, to_scheme):
        replacements = {
            ".a": {"WX": "Z", "SLP1": "'"},
            "ch": "C",
            "dh": {"WX": "X", "SLP1": "D"},
            "aa": "A",
            "ai": "E",
            "au": "O",
            ".th": {"WX": "T", "SLP1": "W"},
            ".t": {"WX": "t", "SLP1": "w"},
            "ph": "P",
            "bh": "B",
            ".n": {"WX": "N", "SLP1": "R"},
            ".d": {"WX": "d", "SLP1": "q"},
            ".dh": {"WX": "D", "SLP1": "Q"},
            "th": {"WX": "W", "SLP1": "T"},
            "kh": "K",
            '"n': {"WX": "f", "SLP1": "N"},
            "gh": "G",
            "d": {"WX": "x", "SLP1": "d"},
            "t": {"WX": "w", "SLP1": "t"},
            ".r": {"WX": "q", "SLP1": "f"},
            ".rr": {"WX": "Q", "SLP1": "F"},
            "~n": {"WX": "F", "SLP1": "Y"},
            "jh": "J",
            ".s": {"WX": "R", "SLP1": "z"},
            '"s': "S",
        }
        res, i, text_len = [], 0, len(text)
        _rep = partial(
            get_dict_value,
            to_scheme,
            replacements
        )

        while i < text_len:
            ch, nxt_ch, nxt_nxt_ch = text[i], None, None
            if i < text_len - 1:
                nxt_ch = text[i + 1]
            if i < text_len - 2:
                nxt_nxt_ch = text[i + 2]
            if ch == ".":
                if nxt_ch in ["d", "t"]:
                    if nxt_nxt_ch == "h":
                        res.append(_rep(ch + nxt_ch + nxt_nxt_ch))
                        i += 2
                    else:
                        res.append(_rep(ch + nxt_ch))
                        i += 1
                elif nxt_ch == 'r':
                    if nxt_nxt_ch == "r":
                        res.append(_rep(ch + nxt_ch + nxt_nxt_ch))
                        i += 2
                    else:
                        res.append(_rep(ch + nxt_ch))
                        i += 1
                elif nxt_ch == "n":
                    res.append(_rep(ch + nxt_ch))
                    i += 1
                elif nxt_ch == "s":
                    res.append(_rep(ch + nxt_ch))
                    i += 1
                elif nxt_ch == "a":
                    res.append(_rep(ch + nxt_ch))
                    i += 1
                elif nxt_ch == "h":
                    res.append('H')
                    i += 1
                elif nxt_ch == "m":
                    res.append('M')
                    i += 1
                else:
                    res.append(".")
            elif ch == '"' and nxt_ch in ['s', 'n']:
                res.append(_rep(ch + nxt_ch))
                i += 1
            elif ch == '~' and nxt_ch == "n":
                res.append(_rep(ch + nxt_ch))
                i += 1
            elif ch in ["c", "p", "b", "k", "g", "j", "t", "d"]:
                if nxt_ch == "h":
                    res.append(_rep(ch + nxt_ch))
                    i += 1
                else:
                    res.append(_rep(ch))

            elif ch == "a" and nxt_ch in ["a", "i", "u"]:
                res.append(_rep(ch + nxt_ch))
                i += 1
            else:
                res.append(_rep(ch))
            i += 1
        return ''.join(res)

    @staticmethod
    def wx_to_vel(text):
        replacements = {
            'Z': ".a",
            'N': '.n',
            'M': '.m',
            'A': 'aa',
            'H': '.h',
            "J": "jh",
            "C": "ch",
            'X': 'dh',
            'E': 'ai',
            'O': 'au',
            'T': '.th',
            't': '.t',
            'P': 'ph',
            'B': 'bh',
            'D': '.dh',
            'W': 'th',
            'K': 'kh',
            'G': 'gh',
            'f': '"n',
            'x': 'd',
            'w': 't',
            'q': '.r',
            'Q': '.rr',
            'F': '~n',
            'S': '"s',
            'R': '.s'
        }
        res = [replacements.get(ch, ch) for ch in text]
        return ''.join(res)

    @staticmethod
    def slp1_to_vel(text):
        replacements = {
            "'": ".a",
            'M': '.m',
            'A': 'aa',
            'H': '.h',
            "J": "jh",
            "C": "ch",
            'N': '"n',
            'D': 'dh',
            'E': 'ai',
            'O': 'au',
            'T': 'th',
            't': 't',
            'P': 'ph',
            'B': 'bh',
            'W': '.th',
            'K': 'kh',
            'G': 'gh',
            'f': '.r',
            'w': '.t',
            'q': '.d',
            'Q': '.dh',
            'F': '.rr',
            'S': '"s',
            'R': '.n',
            '.': '.',
            'z': '.s',
            'Y': '~n'
        }
        res = [replacements.get(ch, ch) for ch in text]
        return ''.join(res)


if __name__ == '__main__':
    print(WxSlp1Vel.wx_to_vel("f"))

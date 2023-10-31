from functools import partial

from .utils import get_dict_value


class WxSlp1Hk:
    """
        Class WxSlp1Hk
        class to convert WX or SLP1 to HK and vice versa
    """

    @staticmethod
    def hk_to_wx_or_slp1(text: str, to_scheme: str) -> str:
        """
        To convert Harvard Kyoto text to either WX or SLP1
        :param text: text in harvard kyoto format
        :param to_scheme: intended output scheme WX or SLP1
        :return: resultant string in WX or SLP1 scheme
        """
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
        # create partial function to get char replacements
        _rep = partial(
            get_dict_value,
            to_scheme,
            replacements
        )

        while i < text_len:
            ch, nxt_ch = text[i], None
            if i < text_len - 1:
                nxt_ch = text[i + 1]
            # dealing with potential aspirates
            if ch in ["c", "d", "T", "p", "b", "D", "t", "k", "g", "j"]:
                if nxt_ch == "h":
                    res.append(_rep(ch + nxt_ch))
                    i += 1
                else:
                    res.append(_rep(ch))
            # potential diphthongs
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
    def wx_to_hk(text: str) -> str:
        """
        Convert WX to HK
        :param text: any text in WX scheme
        :return: string in HK scheme
        """
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
    def slp1_to_hk(text: str) -> str:
        """
        Convert text from SLP1 to HK
        :param text: any string in SLP1 scheme
        :return: result in HK scheme
        """
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

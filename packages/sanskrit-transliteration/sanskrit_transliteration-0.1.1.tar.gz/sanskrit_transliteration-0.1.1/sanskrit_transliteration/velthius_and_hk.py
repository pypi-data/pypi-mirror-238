class VelthiusHk:

    @staticmethod
    def hk_to_velthius(text: str):
        replacements = {
            "A": "aa",
            "I": "ii",
            "U": "uu",
            "R": ".r",
            "G": "\"n",
            "J": "~n",
            "T": ".t",
            "D": ".d",
            "N": ".n",
            "S": ".s",
            "z": "\"s",
            "H": ".h",
            "M": ".m",
            "'": ".a"
        }
        res, i, text_len = [], 0, len(text)
        while i < text_len:
            ch, nxt_ch = text[i], None
            if i < text_len - 1:
                nxt_ch = text[i + 1]
            if text[i] == "R":
                if nxt_ch == "R":
                    res.append(".rr")
                    i += 1
                else:
                    res.append(".r")
            elif ch == "|":
                res.append(".")
            else:
                res.append(
                    replacements.get(ch, ch)
                )
            i += 1
        return "".join(res)

    @staticmethod
    def velthius_to_hk(text: str):
        replacements = {
            "aa": "A",
            "ii": "I",
            "uu": "U",
            ".r": "R",
            "\"n": "G",
            "~n": "J",
            ".t": "T",
            ".d": "D",
            ".n": "N",
            ".s": "S",
            "\"s": "z",
            ".h": "H",
            ".m": "M",
        }
        res, i, text_len = [], 0, len(text)
        while i < text_len:
            ch, nxt_ch, nxt_nxt_ch = text[i], None, None
            if i < text_len - 1:
                nxt_ch = text[i + 1]
            if i < text_len - 2:
                nxt_nxt_ch = text[i + 2]
            if ch == ".":
                if nxt_ch == "r":
                    i += 1
                    if nxt_nxt_ch == "r":
                        res.append("RR")
                        i += 1
                    else:
                        res.append("R")
                elif nxt_ch in ["d", "t", "n", "m", "h", "s"]:
                    i += 1
                    res.append(nxt_ch.upper())
                elif nxt_ch == "a":
                    i += 1
                    res.append("'")
                else:
                    res.append("|")
            elif ch == "~":
                if nxt_ch == "n":
                    i += 1
                    res.append("J")
            elif ch == "a":
                if nxt_ch == "a":
                    i += 1
                    res.append("A")
                else:
                    res.append(ch)
            elif ch == "i":
                if nxt_ch == "i":
                    i += 1
                    res.append("I")
                else:
                    res.append(ch)
            elif ch == "u":
                if nxt_ch == "u":
                    i += 1
                    res.append("U")
                else:
                    res.append(ch)

            elif ch == "\"":
                if nxt_ch in ["n", "s"]:
                    i += 1
                    res.append(replacements[ch + nxt_ch])
                else:
                    res.append(ch)
            else:
                res.append(
                    replacements.get(ch, ch)
                )
            i += 1
        return "".join(res)

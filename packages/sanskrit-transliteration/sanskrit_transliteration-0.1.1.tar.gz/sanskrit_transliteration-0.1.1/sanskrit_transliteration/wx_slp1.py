class WxSlp1:
    @staticmethod
    def wx_to_slp1(text):
        replacements = {
            "Z": "'",
            'f': 'N',
            'F': 'Y',
            't': 'w',
            'T': 'W',
            'w': 't',
            'W': 'T',
            'd': 'q',
            'D': 'Q',
            'N': 'R',
            'q': 'f',
            'Q': 'F',
            'R': 'z',
            'x': 'd',
            'X': 'D'
        }
        return ''.join([replacements.get(ch, ch) for ch in text])

    @staticmethod
    def slp1_to_wx(text):
        replacements = {
            "'": 'Z',
            'N': 'f',
            'Y': 'F',
            'w': 't',
            'W': 'T',
            't': 'w',
            'T': 'W',
            'q': 'd',
            'Q': 'D',
            'R': 'N',
            'f': 'q',
            'F': 'Q',
            'z': 'R',
            'd': 'x',
            'D': 'X',
        }
        return ''.join([replacements.get(ch, ch) for ch in text])

class WxSlp1:
    """
        Class WxSlp1
        class for converting from WX to SLP1 and vice versa
    """

    @staticmethod
    def wx_to_slp1(text: str) -> str:
        """
        :param text: input string in slp1 scheme
        :return: result string in the WX scheme
        """
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
    def slp1_to_wx(text: str) -> str:
        """
        :param text: input string in slp1 scheme
        :return: result string in the WX scheme
        """
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

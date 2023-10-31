class FromSkt:
    __vowels = {
        "अ": {"HK": "a", "VELTHIUS": "a", "SLP1": "a", "WX": "a"},
        "आ": {"HK": "A", "VELTHIUS": "aa", "SLP1": "A", "WX": "A"},
        "इ": {"HK": "i", "VELTHIUS": "i", "SLP1": "i", "WX": "i"},
        "ई": {"HK": "I", "VELTHIUS": "ii", "SLP1": "I", "WX": "I"},
        "उ": {"HK": "u", "VELTHIUS": "u", "SLP1": "u", "WX": "u"},
        "ऊ": {"HK": "U", "VELTHIUS": "uu", "SLP1": "U", "WX": "U"},
        "ए": {"HK": "e", "VELTHIUS": "e", "SLP1": "e", "WX": "e"},
        "ऐ": {"HK": "ai", "VELTHIUS": "ai", "SLP1": "E", "WX": "E"},
        "ओ": {"HK": "o", "VELTHIUS": "o", "SLP1": "o", "WX": "o"},
        "औ": {"HK": "au", "VELTHIUS": "au", "SLP1": "O", "WX": "O"},
        "ऋ": {"HK": "R", "VELTHIUS": ".r", "SLP1": "f", "WX": "q"},
        "ॠ": {"HK": "RR", "VELTHIUS": ".rr", "SLP1": "F", "WX": "Q"},
        "ऌ": {"HK": "lR", "VELTHIUS": ".l", "SLP1": "x", "WX": "L"},
        "ॡ": {"HK": "lRR", "VELTHIUS": ".ll", "SLP1": "X", "WX": "LL"},
    }

    __vowel_markers = {
        "ा": {"HK": "A", "VELTHIUS": "aa", "SLP1": "A", "WX": "A"},
        "ि": {"HK": "i", "VELTHIUS": "i", "SLP1": "i", "WX": "i"},
        "ी": {"HK": "I", "VELTHIUS": "ii", "SLP1": "I", "WX": "I"},
        "ु": {"HK": "u", "VELTHIUS": "u", "SLP1": "u", "WX": "u"},
        "ू": {"HK": "U", "VELTHIUS": "uu", "SLP1": "U", "WX": "U"},
        "े": {"HK": "e", "VELTHIUS": "e", "SLP1": "e", "WX": "e"},
        "ै": {"HK": "ai", "VELTHIUS": "ai", "SLP1": "E", "WX": "E"},
        "ो": {"HK": "o", "VELTHIUS": "o", "SLP1": "o", "WX": "o"},
        "ौ": {"HK": "au", "VELTHIUS": "au", "SLP1": "au", "WX": "au"},
        "ृ": {"HK": "R", "VELTHIUS": ".r", "SLP1": "f", "WX": "q"},
        "ॄ": {"HK": "RR", "VELTHIUS": ".rr", "SLP1": "F", "WX": "Q"},
        "ॢ": {"HK": "lR", "VELTHIUS": ".l", "SLP1": "x", "WX": "L"},
        "ॣ": {"HK": "lRR", "VELTHIUS": ".ll", "SLP1": "X", "WX": "LL"},
    }

    __anusvara = {
        "ः": {"HK": "H", "VELTHIUS": ".h", "SLP1": "H", "WX": "H"},
        "ं": {"HK": "M", "VELTHIUS": ".m", "SLP1": "M", "WX": "M"},
    }

    __misc = {
        "।": {"HK": "|", "VELTHIUS": ".", "SLP1": ".", "WX": "."},
        "ऽ": {"HK": "'", "VELTHIUS": ".a", "SLP1": "'", "WX": "Z"},
    }

    __consonants = {
        'क': {'HK': 'ka', 'VELTHIUS': 'ka', 'SLP1': 'ka', 'WX': 'ka'},
        'ख': {'HK': 'kha', 'VELTHIUS': 'kha', 'SLP1': 'Ka', 'WX': 'Ka'},
        'ग': {'HK': 'ga', 'VELTHIUS': 'ga', 'SLP1': 'ga', 'WX': 'ga'},
        'घ': {'HK': 'gha', 'VELTHIUS': 'gha', 'SLP1': 'Ga', 'WX': 'Ga'},
        'ङ': {'HK': 'Ga', 'VELTHIUS': '"na', 'SLP1': 'Na', 'WX': 'fa'},
        'च': {'HK': 'ca', 'VELTHIUS': 'ca', 'SLP1': 'ca', 'WX': 'ca'},
        'छ': {'HK': 'cha', 'VELTHIUS': 'cha', 'SLP1': 'Ca', 'WX': 'Ca'},
        'ज': {'HK': 'ja', 'VELTHIUS': 'ja', 'SLP1': 'ja', 'WX': 'ja'},
        'झ': {'HK': 'jha', 'VELTHIUS': 'jha', 'SLP1': 'Ja', 'WX': 'Ja'},
        'ञ': {'HK': 'Ja', 'VELTHIUS': '~na', 'SLP1': 'Ya', 'WX': 'Fa'},
        'ट': {'HK': 'Ta', 'VELTHIUS': '.ta', 'SLP1': 'wa', 'WX': 'ta'},
        'ठ': {'HK': 'Tha', 'VELTHIUS': '.tha', 'SLP1': 'Wa', 'WX': 'Ta'},
        'ड': {'HK': 'Da', 'VELTHIUS': '.da', 'SLP1': 'qa', 'WX': 'da'},
        'ढ': {'HK': 'Dha', 'VELTHIUS': '.dha', 'SLP1': 'Qa', 'WX': 'Da'},
        'ण': {'HK': 'Na', 'VELTHIUS': '.na', 'SLP1': 'Ra', 'WX': 'Na'},
        'त': {'HK': 'ta', 'VELTHIUS': 'ta', 'SLP1': 'ta', 'WX': 'wa'},
        'थ': {'HK': 'tha', 'VELTHIUS': 'tha', 'SLP1': 'Ta', 'WX': 'Wa'},
        'द': {'HK': 'da', 'VELTHIUS': 'da', 'SLP1': 'da', 'WX': 'xa'},
        'ध': {'HK': 'dha', 'VELTHIUS': 'dha', 'SLP1': 'Da', 'WX': 'Xa'},
        'न': {'HK': 'na', 'VELTHIUS': 'na', 'SLP1': 'na', 'WX': 'na'},
        'प': {'HK': 'pa', 'VELTHIUS': 'pa', 'SLP1': 'pa', 'WX': 'pa'},
        'फ': {'HK': 'pha', 'VELTHIUS': 'pha', 'SLP1': 'Pa', 'WX': 'Pa'},
        'ब': {'HK': 'ba', 'VELTHIUS': 'ba', 'SLP1': 'ba', 'WX': 'ba'},
        'भ': {'HK': 'bha', 'VELTHIUS': 'bha', 'SLP1': 'Ba', 'WX': 'Ba'},
        'म': {'HK': 'ma', 'VELTHIUS': 'ma', 'SLP1': 'ma', 'WX': 'ma'},
        'य': {'HK': 'ya', 'VELTHIUS': 'ya', 'SLP1': 'ya', 'WX': 'ya'},
        'र': {'HK': 'ra', 'VELTHIUS': 'ra', 'SLP1': 'ra', 'WX': 'ra'},
        'ल': {'HK': 'la', 'VELTHIUS': 'la', 'SLP1': 'la', 'WX': 'la'},
        'व': {'HK': 'va', 'VELTHIUS': 'va', 'SLP1': 'va', 'WX': 'va'},
        'श': {'HK': 'za', 'VELTHIUS': '"sa', 'SLP1': 'Sa', 'WX': 'Sa'},
        'ष': {'HK': 'Sa', 'VELTHIUS': '.sa', 'SLP1': 'za', 'WX': 'Ra'},
        'स': {'HK': 'sa', 'VELTHIUS': 'sa', 'SLP1': 'sa', 'WX': 'sa'},
        'ह': {'HK': 'ha', 'VELTHIUS': 'ha', 'SLP1': 'ha', 'WX': 'ha'}
    }

    __numbers = {
        '१': {'HK': '1', 'VELTHIUS': '1', 'SLP1': '1', 'WX': '1'},
        '२': {'HK': '2', 'VELTHIUS': '2', 'SLP1': '2', 'WX': '2'},
        '३': {'HK': '3', 'VELTHIUS': '3', 'SLP1': '3', 'WX': '3'},
        '४': {'HK': '4', 'VELTHIUS': '4', 'SLP1': '4', 'WX': '4'},
        '५': {'HK': '5', 'VELTHIUS': '5', 'SLP1': '5', 'WX': '5'},
        '६': {'HK': '6', 'VELTHIUS': '6', 'SLP1': '6', 'WX': '6'},
        '७': {'HK': '7', 'VELTHIUS': '7', 'SLP1': '7', 'WX': '7'},
        '८': {'HK': '8', 'VELTHIUS': '8', 'SLP1': '8', 'WX': '8'},
        '९': {'HK': '9', 'VELTHIUS': '9', 'SLP1': '9', 'WX': '9'},
        '०': {'HK': '0', 'VELTHIUS': '0', 'SLP1': '0', 'WX': '0'}
    }

    @staticmethod
    def transliterate_from_skt(scheme: str, text: str) -> str:
        res = []
        for ch in text:
            if ch in FromSkt.__consonants:
                res.append(FromSkt.__consonants[ch][scheme])
            elif ch in FromSkt.__vowel_markers:
                res[-1] = res[-1][:-1] + FromSkt.__vowel_markers[ch][scheme]
            elif ch in FromSkt.__vowels:
                res.append(FromSkt.__vowels[ch][scheme])
            elif ch in FromSkt.__misc:
                res.append(FromSkt.__misc[ch][scheme])
            elif ch in FromSkt.__anusvara:
                res[-1] = res[-1] + FromSkt.__anusvara[ch][scheme]
            elif ch == "्":
                res[-1] = res[-1][:-1]
            elif ch in FromSkt.__numbers:
                res.append(FromSkt.__numbers[ch][scheme])
            else:
                res.append(ch)
        return ''.join(res)

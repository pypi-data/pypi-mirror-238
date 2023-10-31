# Execute with
# $ python -m sanskrit_transliteration   (3.7+)

from sanskrit_transliteration import transliterate
import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Transliterate Sanskrit Text. Currently supported schemes are VELTHIUS, WX, SLP1, HK, SKT'
    )
    parser.add_argument('-i', '--inputtext', type=str, required=True)
    parser.add_argument('-f', '--fromscheme', type=str, required=True)
    parser.add_argument('-t', '--toscheme', type=str, required=True)

    args = parser.parse_args()
    print(
        transliterate(
            text=args.inputtext,
            from_scheme=args.fromscheme,
            to_scheme=args.toscheme,
        )
    )


if __name__ == '__main__':
    main()

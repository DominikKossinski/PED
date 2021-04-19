from argparse import ArgumentParser

from helpers.json_helper import load_tokenized_text, save_grouped_tokenized


def setup_args_parser() -> ArgumentParser:
    args_parser = ArgumentParser()
    args_parser.add_argument("--min", help="Minimum token length", type=int, default=4)
    return args_parser


def main(args) -> None:
    countries = ["GB", "US"]
    for c in countries:
        ocr_texts = load_tokenized_text(f"{c}_grouped_ocr_text")
        filtered_tokens = []
        print(len(ocr_texts))
        for i in ocr_texts:
            new_tokens = []
            for token in i:
                if len(token) >= args.min:
                    new_tokens.append(token)
            filtered_tokens.append(new_tokens)
        save_grouped_tokenized(f"{c}_grouped_filtered_ocr_text", filtered_tokens)


if __name__ == '__main__':
    parser = setup_args_parser()
    main(parser.parse_args())

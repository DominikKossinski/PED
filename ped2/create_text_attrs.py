from argparse import ArgumentParser

from imgprocessing.image_size import ImageSize


def setup_args_parser() -> ArgumentParser:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--size", help="Image size", type=ImageSize, choices=list(ImageSize),
                            default=ImageSize.maxresdefault.value)
    arg_parser.add_argument("--path", help="Data path", type=str)
    arg_parser.add_argument("--save-path", help="Save path", type=str)
    return arg_parser


def main(args):
    attrs = ["vevo", "trailer", "offici", "music", "interview", "remix", "show"]


if __name__ == '__main__':
    parser = setup_args_parser()
    main(parser.parse_args())

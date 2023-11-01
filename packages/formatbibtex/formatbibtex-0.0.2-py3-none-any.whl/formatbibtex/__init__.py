import argparse
import shutil
import re

from textwrap import TextWrapper, indent
from pathlib import Path
from importlib import metadata

from bibtexparser import parse_file, write_string, BibtexFormat


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("files", nargs="*", help="src files to be formatted.")

    # parser.add_argument(
    #     "-l",
    #     "--line-length",
    #     type=int,
    #     default=87,
    #     help="How many characters per line to allow. [default: 87]",
    # )

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbose mode",
    )

    parser.add_argument(
        "-i",
        "--inplace",
        action="store_true",
        help="Inplace mode (warning!)",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Show program's version number and exit",
    )

    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    if args.verbose:
        print(args)

    for path_input in args.files:
        path_input = Path(path_input).absolute()
        if path_input.name.startswith("tmp_"):
            continue
        library = parse_file(path_input)

        if args.inplace:
            path_save_input = path_input.with_stem(f"tmp_saved_input_{path_input.stem}")
            shutil.copyfile(path_input, path_save_input)
            if args.verbose:
                print(f"Processing {path_input} (input saved in {path_save_input})")
            path_output = path_input
        else:
            path_output = path_input.with_stem(f"tmp_{path_input.stem}_formatted")

        cfg = BibtexFormat()
        cfg.indent = "  "

        wrapper = TextWrapper(break_long_words=False, width=87, break_on_hyphens=False)
        pattern = re.compile(r"\n\ *")

        for entry in library.entries:
            for field in entry.fields:
                value = pattern.subn(" ", field.value)[0]
                tmp = "a" * (1 + len(field.key)) + " " + value
                wrapped = wrapper.fill(tmp)
                field.value = indent(wrapped, "    ")[6 + len(field.key) :]

        bib_str = write_string(library, bibtex_format=cfg)

        with open(path_output, "w") as file:
            file.write(bib_str)

        if args.verbose >= 3:
            print(bib_str)


__version__ = metadata.version("formatbibtex")

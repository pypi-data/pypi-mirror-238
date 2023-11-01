from pathlib import Path
import sys

from formatbibtex import main

here = Path(__file__).absolute().parent


def test_simple(monkeypatch):

    with monkeypatch.context() as m:
        m.setattr(
            sys, "argv", [sys.argv[0], str(here / "references.bib"), "-vvv"]
        )
        main()

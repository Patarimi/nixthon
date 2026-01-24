from cyclopts import App

from nixthon.core import nix_check
import logging

logging.basicConfig(level=logging.WARNING)

app = App("nixthon")

@app.command()
def check():
    """
    Check if nix is installed and available.
    """
    return nix_check()

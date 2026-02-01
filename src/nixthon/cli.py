from cyclopts import App
from nixthon import core
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s - %(message)s')

app = App("nixthon")

app.command(core.nix_check, name="check")
app.command(core.nix_run, name="run")
app.command(core.init_nixthon_project, name="init")

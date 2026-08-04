import functools
import logging
import os
import shutil
from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess, run

logger = logging.getLogger(__name__)

THIS_DIR = Path(__file__).parent
WORKING_DIR = Path.cwd()


@functools.lru_cache(maxsize=1)
def nix_check():
    """
    Check if nix is installed and available.
    """
    if os.name == "nt":
        proc = run(["wsl", "-l"], capture_output=True, text=True, check=False)
        list_of_wsl = proc.stdout.replace("\0", "")
        if "NixOS" not in list_of_wsl:
            logger.error(list_of_wsl)
            return False
        logger.info("NixOS WSL distribution found.")
    try:
        proc = nix_run(["nix --version"])
        logger.info(f"nix command found: {proc.stdout}")
        logger.info("Checks passed: nix is installed and available.")
        return True
    except CalledProcessError as e:
        logger.error(e)
        return False


def to_wsl(path: (Path | str)) -> str:
    """
    Convert a windows path to a linux path for WSL usage.
    """
    if os.name != "nt":
        return str(path)
    if type(path) is not Path:
        path = Path(path).absolute()
    if ":" in str(path):
        drive, tail = path.as_posix().split(":")
        return "/mnt/" + drive.lower() + tail
    if str(path)[0] == "\\":
        path = "." + path.as_posix()
    else:
        path = path.as_posix()
    return str(path)


def nix_run(cmd: list[str]) -> CompletedProcess:
    """
    Run a command inside nix-shell.
    """
    over_head = [
        "nix-shell",
        "--command",
    ]
    if os.name == "nt":
        over_head = ["wsl", "-d", "NixOS", "--shell-type", "login"] + over_head
    over_head.append(" ".join(cmd))
    shell_path = THIS_DIR / "shell.nix"
    over_head.append(to_wsl(shell_path))
    logger.debug('"' + '" "'.join(over_head) + '"')
    proc = run(
        over_head,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    logger.debug(f"{proc.stdout=}")
    logger.debug(f"{proc.stderr=}")
    return proc


def init_nixthon_project(project_path: (Path | str) = WORKING_DIR) -> None:
    """
    Initialize a nixthon project by creating a shell.nix file in the specified directory.
    """
    if type(project_path) is not Path:
        project_path = Path(project_path)
    shutil.copyfile(THIS_DIR.parent / "template/shell.nix", project_path / "shell.nix")

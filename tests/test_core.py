import logging
import os
from nixthon import core as m


def test_main():
    assert m.nix_check()


def test_to_wsl():
    if os.name == "nt":
        assert m.to_wsl("C:\\Users\\User") == "/mnt/c/Users/User"
    else:
        assert m.to_wsl("/home/user") == "/home/user"


def test_nix_run():
    proc = m.nix_run(["echo Hello, Nix!"])
    assert proc.returncode == 0
    assert "Hello, Nix!" in proc.stdout


def test_init_nixthon_project(tmp_path):
    project_dir = tmp_path / "my_nixthon_project"
    project_dir.mkdir()
    m.init_nixthon_project(project_dir)
    shell_nix_path = project_dir / "shell.nix"
    logging.info(f"Created shell.nix at: {shell_nix_path}")
    assert shell_nix_path.exists()

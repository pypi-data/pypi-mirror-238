from __future__ import annotations

import os


def test_cli():
    exit_status = os.system("usatt ratings -i 1165420 220283 31126")
    assert exit_status == 0
    exit_status = os.system("usatt summary --outfile usatt.csv")
    assert exit_status == 0
    assert os.path.exists("usatt.csv")
    os.remove("usatt.csv")

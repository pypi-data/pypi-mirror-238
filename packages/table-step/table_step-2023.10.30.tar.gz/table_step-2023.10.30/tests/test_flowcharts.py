#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `table_step` running full flowcharts."""
from pathlib import Path
import pytest
from seamm import run_flowchart

test_dir = Path(__file__).resolve().parent

flowcharts = [
    str(test_dir / path) for path in sorted(test_dir.glob("flowcharts/*.flow"))
]


@pytest.mark.integration
@pytest.mark.parametrize("flowchart", flowcharts)
def test_flowchart(monkeypatch, tmp_path, flowchart):
    monkeypatch.setattr(
        "sys.argv",
        [
            "testing",
            flowchart,
            "--standalone",
        ],
    )

    run_flowchart(wdir=str(tmp_path))

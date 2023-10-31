#!/usr/bin/env python3
# coding: utf-8
# SPDX-License-Identifier: MIT
"""Testing making a LetterBomb"""
import io
import pathlib
import tempfile
import typing

import letterbomb

TEST_MAC = "ECC40DFB90B9"


def test_hackmii():
    letterbomb.write(TEST_MAC, "U", False)
    letterbomb.write(TEST_MAC, "u", False)
    assert len(typing.cast(io.BytesIO, letterbomb.write(TEST_MAC, "U", False)).getvalue()) < 90000


def test_output_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        file = pathlib.Path(tmpdir).joinpath("test.zip")

        # Without HackMii
        assert letterbomb.write(TEST_MAC, "U", False, file).stat().st_size < 90000
        # With HackMii
        assert letterbomb.write(TEST_MAC, "U", output_file=file).stat().st_size < 4450000

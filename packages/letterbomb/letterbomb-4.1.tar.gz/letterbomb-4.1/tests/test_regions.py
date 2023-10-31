#!/usr/bin/env python3
# coding: utf-8
# SPDX-License-Identifier: MIT
"""Testing regions."""
import pytest

import letterbomb

TEST_MAC = "ECC40DFB90B9"


def test_region_u():
    letterbomb.write(TEST_MAC, "U", False)
    letterbomb.write(TEST_MAC, "u", False)


def test_region_e():
    letterbomb.write(TEST_MAC, "E", False)
    letterbomb.write(TEST_MAC, "e", False)


def test_region_j():
    letterbomb.write(TEST_MAC, "J", False)
    letterbomb.write(TEST_MAC, "j", False)


def test_region_k():
    letterbomb.write(TEST_MAC, "K", False)
    letterbomb.write(TEST_MAC, "k", False)


def test_region_invalid():
    with pytest.raises(letterbomb.RegionError):
        letterbomb.write(TEST_MAC, "bad region", False)
        letterbomb.write(TEST_MAC, "USA", False)
        letterbomb.write(TEST_MAC, 0, False)
        letterbomb.write(TEST_MAC, "korea", False)
        letterbomb.write(TEST_MAC, "JJ", False)

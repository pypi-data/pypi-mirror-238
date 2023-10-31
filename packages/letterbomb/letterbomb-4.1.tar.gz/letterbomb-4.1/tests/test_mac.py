#!/usr/bin/env python3
# coding: utf-8
# SPDX-License-Identifier: MIT
"""Testing MAC addresses."""
import pytest
import letterbomb


def test_bad_length():
    with pytest.raises(letterbomb.MACLengthError):
        letterbomb.write("ECC40DFB90B9FF", "U", False)


def test_dolphin_mac():
    with pytest.raises(letterbomb.MACEmulatedError):
        letterbomb.write("0017AB999999", "U", False)


def test_invalid_mac():
    with pytest.raises(letterbomb.MACError):
        letterbomb.write("000000000000", "U", False)


def test_ok_mac():
    assert letterbomb.write("ECC40DFB90B9", "U", False)

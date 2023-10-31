#!/usr/bin/env python3
# coding: utf-8
# SPDX-License-Identifier: MIT
"""
✉️💣 **LetterBomb**: A fork of the `classic Wii hacking tool
<https://wiibrew.org/wiki/LetterBomb>`_ from `fail0verflow
<https://github.com/fail0verflow/letterbomb>`_.

::

    ██╗     ███████╗████████╗████████╗███████╗██████╗ ██████╗  ██████╗ ███╗   ███╗██████╗
    ██║     ██╔════╝╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗
    ██║     █████╗     ██║      ██║   █████╗  ██████╔╝██████╔╝██║   ██║██╔████╔██║██████╔╝
    ██║     ██╔══╝     ██║      ██║   ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗
    ███████╗███████╗   ██║      ██║   ███████╗██║  ██║██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝
    ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝

----

For most usage, you should be using :func:`write`.

For additional usage, either:

* view documentation on `ReadTheDocs <https://letterbomb.rtfd.io>`_.
* build and view the documentation located in the `docs` folder.

If you downloaded this package from `PyPI <https://pypi.org/project/letterbomb>`_, the `docs` folder is not included.

Obtain the latest copy of LetterBomb here: https://gitlab.com/whoatemybutter/letterbomb

.. note:: This exploit only works for System Menu 4.3. 4.2 and below will not work.

LetterBomb is licensed under the MIT license. You can obtain a copy at https://mit-license.org/.
"""
import hashlib
import hmac
import io
import logging
import pathlib
import struct
import zipfile

import datetime

__author__ = "WhoAteMyButter"
__version__ = (4, 1)
__license__ = "MIT"

__HERE = pathlib.Path(__file__).parent

TEMPLATES_DATA: dict[str, bytes] = {}
BUNDLED_DATA: dict[str, bytes] = {}

REGIONS = {"U", "E", "K", "J"}

TEMPLATES = {
    "U": "./included/templates/U.bin",
    "E": "./included/templates/E.bin",
    "J": "./included/templates/J.bin",
    "K": "./included/templates/K.bin",
}

for __region in REGIONS:
    with open(pathlib.Path(__HERE / TEMPLATES[__region]), "rb") as bin_template:
        TEMPLATES_DATA[__region] = bin_template.read()

for __bundlefile in __HERE.joinpath("included/bundled/").iterdir():
    with open(__bundlefile, "rb") as bundle_open:
        BUNDLED_DATA[__bundlefile.name] = bundle_open.read()

with open(pathlib.Path(__HERE / "included/oui_list.txt"), encoding="utf-8") as oui_file:
    OUI_DATA = oui_file.read().splitlines()

LOGGING_DICT = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

LOGGING_LEVEL = logging.INFO
LOGGING_FILE = ""


class MACError(ValueError):
    """Raised when a MAC does not belong to a Wii."""

    def __init__(self, message: str = "Bad MAC, does not belong to a Wii."):
        super().__init__(message)
        self.message = message


class MACLengthError(MACError):
    """Raised when a MAC is not 12 characters in length."""

    def __init__(self, message: str = "Bad MAC, length should be 12 characters only."):
        super().__init__(message)
        self.message = message


class MACEmulatedError(MACError):
    """Raised when a MAC is of an emulator."""

    def __init__(self, message: str = "Bad MAC, you cannot use a MAC address from an emulator."):
        super().__init__(message)
        self.message = message


class RegionError(ValueError):
    """Raised when region is not a valid region character."""

    def __init__(self, message: str = "Region must be one of U, E, J, K."):
        super().__init__(message)
        self.message = message


def mac_digest(mac: str) -> bytes:
    r"""
    Process `mac` through a SHA1 encoding with ``'\x75\x79\x79'`` added.

    :param str mac: MAC address to digest.
    :returns: SHA-1 hash of MAC, plus \x75\x79\x79, then digested.
    """
    return hashlib.sha1(mac.encode("latin-1") + b"\x75\x79\x79").digest()


def serialize_mac(mac: str) -> str:
    """
    Return `mac` as a string, each field split by a ":".

    Padded with zeros to two-lengths.

    :param str mac: MAC address.
    :returns: A ":" split string.
    """
    return ":".join(mac[i : i + 2].zfill(2) for i in range(0, len(mac), 2))


def validate_mac(mac: str, oui_list: list[str]) -> bool:
    """
    Ensure `mac` is a valid Wii MAC address.

    If MAC is valid, returns True.

    :param mac: MAC address to validate.
    :param oui_list: OUI list, not a path to an OUI file.
    :raises BadLengthMACError: if MAC is not the proper length.
    :raises EmulatedMACError: if MAC is from an emulator.
    :raises InvalidMACError: if MAC does not belong to a Wii.
    :returns: True is MAC is valid.
    """
    if len(mac) != 12:
        raise MACLengthError(mac)
    if mac.upper() == "0017AB999999":
        raise MACEmulatedError(mac)
    if not any(mac.upper().startswith(i.upper()) for i in oui_list):
        raise MACError(mac)
    return True


def pack_blob(digest: bytes, time_stamp: int, blob: bytearray) -> bytearray:
    """
    Pack `blob` with corresponding timestamps and the MAC `digest`.

    :param digest: MAC digest.
    :param time_stamp: Unix epoch time.
    :param blob: Blob content.
    :returns: Resulting blob content.
    """
    blob[0x08:0x10] = digest[:8]
    blob[0xB0:0xC4] = b"\x00" * 20
    blob[0x7C:0x80] = struct.pack(">I", time_stamp)
    blob[0x80:0x8A] = b"%010d" % time_stamp
    blob[0xB0:0xC4] = hmac.new(digest[8:], blob, hashlib.sha1).digest()
    return blob


def sd_path(digest: bytes, deltatime: datetime.datetime, time_stamp: int) -> str:
    """
    Return the path of the LetterBomb, relative to the root of the SD card.

    :param digest: MAC digest, see :func:`mac_digest`
    :param deltatime: Time of letter receival.
    :param time_stamp: Unix epoch time.
    :returns: String of resulting path, relative.
    """
    return (
        "private/wii/title/HAEA/"
        f"{digest[:4].hex().upper()}/"
        f"{digest[4:8].hex().upper()}/"
        "%04d/%02d/%02d/%02d/%02d/HABA_#1/txt/%08X.000"
        % (
            deltatime.year,
            deltatime.month - 1,
            deltatime.day,
            deltatime.hour,
            deltatime.minute,
            time_stamp,
        )
    )


def timestamp() -> tuple[datetime.datetime, datetime.timedelta, int]:
    """
    Return a tuple of timestamps.

    :returns: Tuple of ``(date, delta from 2000/1/1, timestamp)``.
    """
    deltatime = datetime.datetime.utcnow() - datetime.timedelta(1)
    delta = deltatime - datetime.datetime(2000, 1, 1)
    return deltatime, delta, delta.days * 86400 + delta.seconds


def write(
    mac: str,
    region: str,
    pack_bundle: bool = True,
    output_file: str | pathlib.Path | None = None,
) -> io.BytesIO | pathlib.Path:
    """
    Write LetterBomb archive.
    Depending on `output_file`, archive bytes may be returned.

    Depending upon the `region`, different LetterBomb templates will be used.

    * If `pack_bundle` is True, the HackMii installer will be included with the archive.
    * If `output_file` is falsy, it will be ignored and the raw bytes are returned.

    :param mac: Full string of the Wii's MAC address.
    :param region: Region of Wii, must be single letter of ``U,J,K,E``.
    :param pack_bundle: Pack the HackMii installer with archive.
    :param output_file: File to write archive to, bytes are returned if empty.
    :raises MACLengthError: if MAC is not the proper length.
    :raises MACEmulatedError: if MAC is from an emulator.
    :raises MACError: if MAC does not belong to a Wii.
    :returns: BytesIO of ZIP archive, or file path of archive.
    """
    if not LOGGING_FILE:
        logging.basicConfig(filename=LOGGING_FILE, level=LOGGING_LEVEL)

    region = region.upper()
    if region not in REGIONS:
        raise RegionError(region)

    dig = mac_digest(mac)
    time = timestamp()

    validate_mac(mac, OUI_DATA)

    zip_stream: pathlib.Path | io.BytesIO
    if output_file:
        zip_stream = pathlib.Path(output_file).expanduser().absolute()
    else:
        zip_stream = io.BytesIO()
    with zipfile.ZipFile(zip_stream, "w", compression=zipfile.ZIP_BZIP2, compresslevel=9) as zip_out:
        zip_out.writestr(
            sd_path(dig, time[0], time[2]),
            pack_blob(dig, time[2], pack_blob(dig, time[2], bytearray(TEMPLATES_DATA[region]))),
        )
        if pack_bundle:
            for name, dpath in BUNDLED_DATA.items():
                zip_out.writestr(name, dpath)
    return zip_stream

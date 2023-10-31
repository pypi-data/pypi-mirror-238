#!/usr/bin/env python3
"""
Updates the bundled OUI list with new Nintendo IDs.

Python port of update_oui.sh.
"""
# SPDX-License-Identifier: MIT
import pathlib
import urllib.request


def update_oui() -> None:
    """
    Update the stored ``oui_list.txt`` and backup the old file to ``oui_list.txt.old``.
    Data is from https://standards-oui.ieee.org/.

    .. note:: Run this in the directory that **contains** the letterbomb module, not inside the module itself.
    """
    print(__file__)
    if not (included := pathlib.Path("./letterbomb/included")).exists():
        print("This script must be ran inside of the LetterBomb module directory.")
        return
    print("Getting latest OUI list...")
    with urllib.request.urlopen("https://standards-oui.ieee.org/") as response:
        print("Parsing OUI received list...")
        oui_list = [
            line.split(maxsplit=1)[0]
            for line in [
                line
                for line in response.read().decode("utf-8").split("\n")
                if ("nintendo" in line.lower() and "base 16" in line.lower())
            ]
        ]
        print("Sorting OUI list...")
        oui_list.sort()

        print("Backing up old OUI list...")
        (included_oui := included.joinpath("./oui_list.txt")).rename(
            pathlib.Path("./letterbomb/included/oui_list.txt.old")
        )
        print("Writing new OUI list...")
        with included_oui.open("w", encoding="utf-8") as oui:
            oui.write("\n".join(oui_list))
        print("Updated succesfully.")


if __name__ == "__main__":
    update_oui()

#!/usr/bin/env python3
# coding: utf-8
# SPDX-License-Identifier: MIT
"""CLI component."""
import argparse

import letterbomb_web
import letterbomb

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f'letterbomb_web v{".".join(str(x) for x in letterbomb_web.__version__)}, under letterbomb v'
                f'{".".join(str(x) for x in letterbomb.__version__)}'
    )
    parser.parse_args()

    letterbomb_web.start()

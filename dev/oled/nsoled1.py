#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

import sys
import time

from demo_opts import get_device
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, SINCLAIR_FONT

def main(num_iterations=4):
    device = get_device()

    while num_iterations > 0:
        num_iterations -= 1

        msg = "a"
        show_message(device, msg, fill="white", font=proportional(SINCLAIR_FONT))
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass


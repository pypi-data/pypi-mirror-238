# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) Ansel Neunzert (2023)
#
# This file is part of fscan

# simple snippet to handle various ways of specifying True
def str_to_bool(choice):
    return bool(str(choice).lower() in ('yes', 'y', 'true', 't', '1'))

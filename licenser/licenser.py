#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

"""
# I need to work in a community.
Use the license preferred by the community you’re contributing to or depending on. Your project will fit right in.

If you have a dependency that doesn’t have a license, ask its maintainers to add a license.

# I want it simple and permissive.
The MIT License is short and to the point. It lets people do almost anything they want with your project, like making and distributing closed source versions.

Babel, .NET, and Rails use the MIT License.

# I care about sharing improvements.
The GNU GPLv3 also lets people do almost anything they want with your project, except distributing closed source versions.

Ansible, Bash, and GIMP use the GNU GPLv3.

{ What if none of these work for me? }

# My project isn’t software.
[https://choosealicense.com/non-software/](There are licenses for that).

# I want more choices.
[https://choosealicense.com/licenses/](More licenses are available.)

# I don’t want to choose a license.
[https://choosealicense.com/no-permission/](Here’s what happens if you don’t.)
"""

import argparse
import sys

#---------------Software----------------
agplv3_gnu = """

"""
gnu_gplv3 = """

"""
lgplv3_gnu = """

"""
mplv2 = """

"""
apachev2 = """

"""
mit = """

"""
bslv1 = """

"""
unlicense = """
"""
#---------------Hardware----------------
cern_ohl_p2 = """

"""
cern_ohl_w2 = """

"""
cern_ohl_s2 = """

"""
#---------------Fonts----------------
sil_ofl_1 = """

"""
#---------------Data and media----------------
cc0_1 = """

"""
cc_by_4 = """

"""
cc_by_sa_4 = """

"""
def main(path):
    license_type = """
1. software
2. media, data, etc.
3. documentation
4. fonts
5. hardware
6. mix project
"""
    license_type_option = int(input(license_type))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to the file')
    args = parser.parse_args()
    path = args.path
    main(path)
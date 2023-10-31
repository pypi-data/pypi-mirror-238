# -*- coding: utf-8 -*-
import pyard

#
#    my_project_template My Project Template.
#    Copyright (c) 2021 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#

message = """
    Legacy pyard. This is not the pyard you're looking for.
    Use py-ard (https://pypi.org/project/py-ard/)
    Steps:
     1. Remove pyard project: `pip uninstall pyard`
     2. Install py-ard: `pip install py-ard`
     3. redux() away.
"""


class ARD(object):
    """
    This is legacy. Use py-ard https://pypi.org/project/py-ard/
    """
    print(message)

    def __init__(self, version="1234"):
        print(message)

    def redux(self, allele, redux_type):
        print(message)
        return "This is not the pyard you're looking for."

    def redux_gl(self, gl, redux_type):
        return self.redux(gl, redux_type)

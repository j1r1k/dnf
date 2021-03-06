# Copyright (C) 2017 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import tempfile
import unittest

import libdnf.conf
import dnf

DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class ModuleConfTest(unittest.TestCase):

    def setUp(self):
        self.dnf_conf = dnf.conf.MainConf()
        self.dnf_conf.modulesdir = os.path.join(DIR, "modules/etc/dnf/modules.d")
        parser = libdnf.conf.ConfigParser()
        self.conf = dnf.conf.ModuleConf(section="base-runtime", parser=parser)

        # name - equal to section name
        self.conf.stream._set("f26")
        self.conf.version._set(1)
        # profiles - empty list by default
        self.conf.enabled._set(1)
        self.conf.locked._set(0)

    def test_options(self):
        self.assertEqual(self.conf.name._get(), "base-runtime")
        self.assertEqual(self.conf.stream._get(), "f26")
        self.assertEqual(self.conf.version._get(), 1)
        self.assertEqual(list(self.conf.profiles._get()), [])
        self.assertEqual(self.conf.enabled._get(), True)
        self.assertEqual(self.conf.locked._get(), False)

    def test_write(self):
        tmp_dir = tempfile.mkdtemp()
        tmp_file = os.path.join(tmp_dir, "%s.module" % self.conf._section)
        with open(tmp_file, "w") as config_file:
            self.conf._write(config_file)
        # TODO: compare
        os.unlink(tmp_file)
        os.rmdir(tmp_dir)

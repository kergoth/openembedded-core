# SPDX-License-Identifier: MIT
import os
import sys
import re
import logging
from oeqa.core.decorator import OETestTag
from oeqa.core.case import OEPTestResultTestCase
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, get_bb_var, get_bb_vars
from oeqa.utils.multilib import load_tests_multilib_variants


def parse_values(content):
    for i in content:
        for v in ["PASS", "FAIL", "XPASS", "XFAIL", "UNRESOLVED", "UNSUPPORTED", "UNTESTED", "ERROR", "WARNING"]:
            if i.startswith(v + ": "):
                yield i[len(v) + 2:].strip(), v
                break


@OETestTag("toolchain-user", "toolchain-system")
class BinutilsCrossSelfTest(OESelftestTestCase, OEPTestResultTestCase):
    def test_binutils(self):
        self.run_binutils("binutils")

    def test_gas(self):
        self.run_binutils("gas")

    def test_ld(self):
        self.run_binutils("ld")

    def run_binutils(self, suite):
        features = []
        features.append('CHECK_TARGETS = "{0}"'.format(suite))
        self.write_config("\n".join(features))

        recipe = self.mlprefix + "binutils-cross-testsuite"

        bitbake("{0} -c check".format(recipe))

        builddir = get_bb_var("B", recipe)
        sumspath = os.path.join(builddir, suite, "{0}.sum".format(suite))
        if not os.path.exists(sumspath):
            sumspath = os.path.join(builddir, suite, "testsuite", "{0}.sum".format(suite))
        logpath = os.path.splitext(sumspath)[0] + ".log"

        ptestsuite = "{}binutils{}".format(self.mlprefix, '-' + suite if suite != 'binutils' else '')
        self.ptest_section(ptestsuite, logfile = logpath)
        with open(sumspath, "r") as f:
            for test, result in parse_values(f):
                self.ptest_result(ptestsuite, test, result)


def load_tests(loader, tests, pattern):
    return load_tests_multilib_variants(loader, tests, pattern, [BinutilsCrossSelfTest])

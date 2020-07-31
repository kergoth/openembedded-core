#
# Copyright (C) 2020 Mentor Graphics, a Siemens Company
#
# SPDX-License-Identifier: MIT

import sys
import unittest
from oeqa.utils.commands import get_bb_var


def generate_variant_classes(baseclasses, name, modulename, variants):
    """Generate new variant test case classes for each baseclass.

    For each variant, we create a new class which inherits the baseclass, with
    the variant as a underscore suffix, and we set the 'variant' member variable
    to match.
    """
    module = sys.modules[modulename]
    for variant in variants:
        if variant:
            newname = name + '_' + variant
        else:
            newname = name

        newcls = type(
            newname,
            baseclasses,
            {'__module__': modulename,
             '__qualname__': newname,
             'variant': variant,
             'mlprefix': variant + '-' if variant else ''},
        )
        setattr(module, newname, newcls)
        yield newcls


def load_tests_multilib_variants(loader, tests, pattern, baseclasses):
    """Load the baseclasses and new classes for each variant in MULTILIB_VARIANTS."""
    variants = (get_bb_var('MULTILIB_VARIANTS') or '').split()

    classes = []
    for baseclass in baseclasses:
        baseclass.variant, baseclass.mlprefix = '', ''
        if variants:
            classes.extend(generate_variant_classes(
                (baseclass,), baseclass.__name__, baseclass.__module__, variants))

    suite = unittest.TestSuite()
    for test_class in classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite


def classes_inheriting(baseclass, module=None):
    if module is None:
        module = sys.modules[baseclass.__module__]

    for name in dir(module):
        obj = getattr(module, name)
        if type(obj) == type and issubclass(obj, baseclass):
            yield obj

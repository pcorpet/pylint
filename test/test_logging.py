# Copyright 2014 Google Inc. All Rights Reserved.
"""
Unittest for the logging checker.
"""
from logilab.common.testlib import unittest_main
from astroid import test_utils

from pylint.checkers import logging

from pylint.testutils import CheckerTestCase, Message, set_config


class LoggingModuleDetectionTest(CheckerTestCase):
    CHECKER_CLASS = logging.LoggingChecker
    
    def test_detects_standard_logging_module(self):
        stmts = test_utils.extract_node("""
        import logging #@
        logging.warn('%s' % '%s')  #@
        """)
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertAddsMessages(Message('W1201', node=stmts[1])):
            self.checker.visit_callfunc(stmts[1])

    def test_detects_renamed_standard_logging_module(self):
        stmts = test_utils.extract_node("""
        import logging as blogging #@
        blogging.warn('%s' % '%s')  #@
        """)
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertAddsMessages(Message('W1201', node=stmts[1])):
            self.checker.visit_callfunc(stmts[1])

    @set_config(logging_modules=['logging', 'my.logging'])
    def test_nonstandard_logging_module(self):
        stmts = test_utils.extract_node("""
        from my import logging as blogging #@
        blogging.warn('%s' % '%s')  #@
        """)
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertAddsMessages(Message('W1201', node=stmts[1])):
            self.checker.visit_callfunc(stmts[1])


if __name__ == '__main__':
    unittest_main()
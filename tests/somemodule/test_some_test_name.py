# Copyright (c) 2019-2023, Cloudless Consulting Pty Ltd.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# - To skip a test, use this decoractor (doc: https://docs.pytest.org/en/latest/how-to/skipping.html):
#
#       @pytest.mark.skip()
#
# - To only run a single test function, in the `makefile`, replace this command:
#
#       pytest --capture=no --verbose tests
#
#   with this:
#
#       pytest --capture=no --verbose tests/somemodule/test_some_test_name.py::test_self_describing_test_name

import pytest  # uncomment this line to use the 'pytest' decorators
import sys

sys.path.append(".")  # noqa

from src.yourmodule import do_something, do_something_else


def test_self_describing_test_name():
    val = do_something()

    assert val


@pytest.mark.skip()
def test_self_describing_another_test_name():
    val = do_something_else()

    assert val

# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest

from datadog_checks.system_core import SystemCore

from . import common


@pytest.fixture(scope='session')
def dd_environment():
    yield common.INSTANCE


@pytest.fixture
def check():
    return SystemCore(common.CHECK_NAME, {}, {})

# Copyright Red Hat
#
# This file is part of fedfind.
#
# fedfind is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Adam Williamson <awilliam@redhat.com>

# these are all kinda inappropriate for pytest patterns
# pylint: disable=old-style-class, no-init, protected-access, no-self-use, unused-argument

"""Test configuration and fixtures."""

from __future__ import unicode_literals
from __future__ import print_function

import json
import os
import re
import shutil
import subprocess
import time

try:
    # Python >= 3.3
    from unittest import mock
except ImportError:
    # Python < 3.3
    import mock

import pytest

# pylint:disable=import-error
from six.moves.urllib.error import URLError, HTTPError
from six.moves.urllib.request import urlopen

import fedfind.const
import fedfind.helpers

# Fake data for the releases fixtures. This is what real data would
# have looked like as of 2020-02-21.
RELEASES_BRANCHED_JSON = {"fedora": {"stable": [30, 31], "branched": [32]}}

# This removes Branched, to check behaviour when there isn't one.
RELEASES_NOBRANCHED_JSON = {"fedora": {"stable": [30, 31], "branched": []}}


@pytest.yield_fixture(scope="session")
def http(request):
    """Run a SimpleHTTPServer that we can use as a fake dl.fp.o. Serve
    the contents of tests/data/http, for the entire test session. We
    just do this with subprocess as we need it to run parallel to the
    tests and this is really the easiest way.
    """
    root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "http")
    args = ("python3", "-m", "http.server", "5001")
    proc = subprocess.Popen(args, cwd=root)
    # block until the server is actually running
    resp = None
    while not resp:
        try:
            resp = urlopen("http://localhost:5001/pub")
        except (ValueError, URLError, HTTPError):
            time.sleep(0.1)
    # Redefine the HTTPS_DL and HTTPS constants to point to the fake
    fedfind.const.HTTPS_DL = "http://localhost:5001/pub"
    fedfind.const.HTTPS = "http://localhost:5001/pub"
    yield

    # teardown
    proc.kill()


@pytest.yield_fixture(scope="function")
def clean_home(request):
    """Provides a fake user home directory, at data/home/ under the
    tests directory. Before the test, re-create it, change the cache
    dir global to use it, and patch os.path.expanduser to return it.
    After the test, delete it and clean up the other bits. Yields
    the full path.
    """
    home = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "home")
    if os.path.exists(home):
        shutil.rmtree(home)
    cachedir = os.path.join(home, ".cache", "fedfind")
    os.makedirs(cachedir)
    with mock.patch("os.path.expanduser", return_value=home, autospec=True):
        origcache = fedfind.helpers.CACHEDIR
        fedfind.helpers.CACHEDIR = cachedir
        yield home

    # teardown stuff
    fedfind.helpers.CACHEDIR = origcache
    if os.path.exists(home):
        shutil.rmtree(home)


def fake_pdc_query(path, params=None):
    """A fake pdc_query that doesn't really hit PDC, it just returns
    canned information (some inline, some loaded from tests/data) for
    queries the tests are known to make.
    """
    # match how pdc_query sanitizes the path
    path = path.strip("/") + "/"
    # composes query. This is hit for cid_from_label.
    if path == "composes/":
        # Knowns in (release, label, composeid) form:
        composes = (
            ("fedora-24", "RC-1.2", "Fedora-24-20160614.0"),
            ("fedora-25", "RC-1.3", "Fedora-25-20161115.0"),
            ("fedora-26", "RC-1.5", "Fedora-26-20170705.0"),
            ("fedora-27", "RC-1.6", "Fedora-27-20171105.0"),
            ("fedora-28", "RC-1.1", "Fedora-28-20180425.0"),
            ("fedora-29", "RC-1.2", "Fedora-29-20181024.1"),
            # these two were apparently never actually imported to the
            # real PDC, so our fake PDC shouldn't 'find' them either
            # ('fedora-30', 'RC-1.2', 'Fedora-30-20190425.0'),
            # ('fedora-31', 'RC-1.9', 'Fedora-31-20191023.0'),
            ("fedora-32", "RC-1.6", "Fedora-32-20200422.0"),
            ("fedora-33", "RC-1.2", "Fedora-33-20201019.0"),
            ("fedora-34", "RC-1.2", "Fedora-34-20210423.0"),
            ("fedora-35", "RC-1.2", "Fedora-35-20211026.0"),
            ("fedora-36", "RC-1.5", "Fedora-36-20220504.1"),
            ("fedora-37", "RC-1.7", "Fedora-37-20221105.0"),
            ("fedora-38", "RC-1.6", "Fedora-38-20230413.1"),
        )
        for rel, label, cid in composes:
            # We can make this matching smarter if needed, for now
            # it's specific to cid_from_label:
            if params.get("release") == rel and params.get("compose_label") == label:
                return [{"compose_id": cid, "release": rel, "compose_label": label}]
            # ...or label_from_cid:
            if params.get("compose_id") == cid:
                return [{"compose_id": cid, "release": rel, "compose_label": label}]
        # fallthrough
        return []

    # compose-images query. Just grab the compose ID and look for a
    # backing file to return.
    compimgs = re.compile(r"compose-images/(.*)/")
    match = compimgs.match(path)
    if match:
        fname = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data",
            "pdc-compimages-{}.json".format(match.group(1)),
        )
        with open(fname, "r") as datafh:
            return json.loads(datafh.read())


@pytest.yield_fixture(scope="function")
def pdc(request):
    """Mock fedfind.helpers.pdc_query with fake_pdc_query."""
    with mock.patch("fedfind.helpers.pdc_query", fake_pdc_query):
        yield


@pytest.yield_fixture(scope="function")
def releases_branched(request):
    """Mock fedfind.helpers._get_releases to return test data (with a
    Branched release)."""
    with mock.patch(
        "fedfind.helpers._get_releases", return_value=RELEASES_BRANCHED_JSON, autospec=True
    ):
        yield


@pytest.yield_fixture(scope="function")
def releases_nobranched(request):
    """Mock fedfind.helpers._get_releases to return test data."""
    with mock.patch(
        "fedfind.helpers._get_releases", return_value=RELEASES_NOBRANCHED_JSON, autospec=True
    ):
        yield


@pytest.yield_fixture(scope="function")
def json_releases(request):
    """Mock fedfind.helpers.download_json to return releases test
    data (wrapped appropriately). Returns the mock so tests can check
    its call count, and the test data so they can verify it.
    """
    with mock.patch(
        "fedfind.helpers.download_json", return_value=RELEASES_BRANCHED_JSON, autospec=True
    ) as mocked:
        yield (mocked, RELEASES_BRANCHED_JSON)


# vim: set textwidth=100 ts=8 et sw=4:

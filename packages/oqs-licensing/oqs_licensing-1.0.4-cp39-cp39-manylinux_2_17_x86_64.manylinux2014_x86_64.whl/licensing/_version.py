# -*- coding: utf-8 -*-
# This file is part of 'miniver': https://github.com/jbweston/miniver
#
import contextlib
import json
import os
import subprocess
from collections import namedtuple
from distutils.util import strtobool

import requests
from setuptools.command.build_py import build_py as build_py_orig
from setuptools.command.sdist import sdist as sdist_orig

Version = namedtuple("Version", ("release", "dev", "labels"))

# No public API
__all__ = []

package_root = os.path.dirname(os.path.realpath(__file__))
package_name = os.path.basename(package_root)

STATIC_VERSION_FILE = "_static_version.py"


def get_version(version_file=STATIC_VERSION_FILE):
    version_info = get_static_version_info(version_file)
    version = version_info["version"]
    if version == "__use_git__":
        if strtobool(os.environ.get("MINIVER_RELEASE_ALPHA", "False")):
            # Alpha release
            version = get_new_alpha_version()
        else:
            version = get_version_from_git()
        if not version:
            version = get_version_from_git_archive(version_info)
        if not version:
            version = Version("unknown", None, None)
        return pep440_format(version)
    else:
        return version


def get_static_version_info(version_file=STATIC_VERSION_FILE):
    version_info = {}
    with open(os.path.join(package_root, version_file), "rb") as f:
        exec(f.read(), {}, version_info)
    return version_info


def version_is_from_git(version_file=STATIC_VERSION_FILE):
    return get_static_version_info(version_file)["version"] == "__use_git__"


def pep440_format(version_info):
    release, dev, labels = version_info

    version_parts = [release]
    if dev:
        if (
            release.endswith("-dev")
            or release.endswith(".dev")
            or dev.startswith("a")
            or dev.startswith("rc")
        ):
            version_parts.append(dev)
        else:  # prefer PEP440 over strict adhesion to semver
            version_parts.append(".dev{}".format(dev))

    if labels:
        version_parts.append("+")
        version_parts.append(".".join(labels))

    return "".join(version_parts)


def get_version_from_git():
    # git describe --first-parent does not take into account tags from branches
    # that were merged-in. The '--long' flag gets us the 'dev' version and
    # git hash, '--always' returns the git hash even if there are no tags.
    for opts in [["--first-parent"], []]:
        try:
            p = subprocess.Popen(
                ["git", "describe", "--long", "--always"] + opts,
                cwd=package_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except OSError:
            return
        if p.wait() == 0:
            break
    else:
        return

    description = (
        p.communicate()[0]
        .decode()
        .strip("v")  # Tags can have a leading 'v', but the version should not
        .rstrip("\n")
        .rsplit("-", 2)  # Split the latest tag, commits since tag, and hash
    )

    try:
        release, dev, git = description
    except ValueError:  # No tags, only the git hash
        # prepend 'g' to match with format returned by 'git describe'
        git = "g{}".format(*description)
        release = "unknown"
        dev = None

    labels = []
    if dev == "0":
        dev = None
    else:
        labels.append(git)

    try:
        p = subprocess.Popen(["git", "diff", "--quiet"], cwd=package_root)
    except OSError:
        labels.append("confused")  # This should never happen.
    else:
        if p.wait() == 1:
            labels.append("dirty")

    return Version(release, dev, labels)


def get_latest_version_in_registry():
    token = os.environ.get("ACCESS_TOKEN", "")
    if token == "":
        raise ValueError(
            "Cannot latest version from registry because no token is specified."
        )
    # Set the header to authenticate the CI token if triggered by CI.
    if os.environ.get("USER_NAME") == "gitlab-ci-token":
        headers = {"JOB-TOKEN": token}
    else:
        headers = {"PRIVATE-TOKEN": token}

    response = requests.get(
        "https://code.orangeqs.com/api/v4/projects/56/packages?package_name="
        + "licensing&order_by=version&sort=desc",
        headers=headers,
        stream=True,
    )
    if int(response.status_code) != 200:
        raise Exception(
            "Failed to get latest version from registry. Server responded with "
            + str(json.loads(response.content))
        )
    list_of_releases = json.loads(response.content)
    latest_release = max(list_of_releases, key=lambda x: x["id"])
    latest_version = (
        latest_release["version"]
        .strip("v")  # Tags can have a leading 'v', but the version should not
        .rstrip("\n")
    )
    return latest_version


def get_new_alpha_version():
    latest_version = get_latest_version_in_registry()

    if ".dev" in latest_version:
        coming_release = latest_version.split(".dev")[0]  # Backwards compatible
        alpha = "a0"
    elif "a" in latest_version:
        coming_release = latest_version.split("a")[0]
        alpha = "a" + str(int(latest_version.split("a")[-1]) + 1)
    elif "rc" in latest_version:
        # Exception for when pushing to main right after a release candidate was
        # released. In this case, we bump the RC number by 1.
        coming_release, rc = latest_version.split("rc")
        alpha = "rc" + str(int(rc) + 1)
    else:
        latest_release = latest_version
        yyyy, ww, minor = latest_release.split(".")
        # Bump minor by one
        bumped_minor = str(int(minor) + 1)
        coming_release = ".".join([yyyy, ww, bumped_minor])
        alpha = "a0"

    return Version(coming_release, alpha, None)


# TODO: change this logic when there is a git pretty-format
#       that gives the same output as 'git describe'.
#       Currently we can only tell the tag the current commit is
#       pointing to, or its hash (with no version info)
#       if it is not tagged.
def get_version_from_git_archive(version_info):
    try:
        refnames = version_info["refnames"]
        git_hash = version_info["git_hash"]
    except KeyError:
        # These fields are not present if we are running from an sdist.
        # Execution should never reach here, though
        return None

    if git_hash.startswith("$Format") or refnames.startswith("$Format"):
        # variables not expanded during 'git archive'
        return None

    VTAG = "tag: v"
    refs = set(r.strip() for r in refnames.split(","))
    version_tags = set(r[len(VTAG) :] for r in refs if r.startswith(VTAG))
    if version_tags:
        release, *_ = sorted(version_tags)  # prefer e.g. "2.0" over "2.0rc1"
        return Version(release, dev=None, labels=None)
    else:
        return Version("unknown", dev=None, labels=["g{}".format(git_hash)])


__version__ = get_version()


# The following section defines a 'get_cmdclass' function
# that can be used from setup.py. The '__version__' module
# global is used (but not modified).


def _write_version(fname):
    # This could be a hard link, so try to delete it first.  Is there any way
    # to do this atomically together with opening?
    with contextlib.suppress(OSError):
        os.remove(fname)

    with open(fname, "w") as f:
        f.write(
            "# This file has been created by setup.py.\n"
            + f"version = '{__version__}'\n"
        )


def get_cmdclass(pkg_source_path):
    class _build_py(build_py_orig):
        def run(self):
            super().run()

            src_marker = "".join(["src", os.path.sep])

            if pkg_source_path.startswith(src_marker):
                path = pkg_source_path[len(src_marker) :]
            else:
                path = pkg_source_path
            _write_version(os.path.join(self.build_lib, path, STATIC_VERSION_FILE))

    class _sdist(sdist_orig):
        def make_release_tree(self, base_dir, files):
            super().make_release_tree(base_dir, files)
            _write_version(os.path.join(base_dir, pkg_source_path, STATIC_VERSION_FILE))

    return dict(sdist=_sdist, build_py=_build_py)

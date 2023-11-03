"""A Vulnerability Scanner for Gitlab's Gemnasiumm Database."""
# This file is part of hoppr-cop
#
# Licensed under the MIT License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Copyright (c) 2022 Lockheed Martin Corporation
from __future__ import annotations

import os
import pkgutil
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import zipfile

from pathlib import Path
from typing import ClassVar
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import hoppr_cyclonedx_models.cyclonedx_1_4 as cdx
import requests
import typer
import yaml

from cvss import CVSS2, CVSS3
from hoppr_security_commons.utils import (
    get_advisories_from_urls,
    get_references_from_ids,
    get_vulnerability_source,
)
from hoppr_security_commons.vulnerability_scanner import VulnerabilitySuper

from hopprcop.gemnasium.models import GemnasiumVulnerability


if TYPE_CHECKING:
    from packageurl import PackageURL


class GemnasiumScanner(VulnerabilitySuper):
    """A Vulnerability Scanner for Gitlab's Gemnasiumm Database."""

    supported_formats: ClassVar[list[str]] = ["npm", "maven", "pypi", "gem", "golang", "conan", "nuget"]
    # TODO: supported_formats is not used; should get_vulnerabilities_by_purl be filtering purls by it?

    database_path = None
    # url = "https://gitlab.com/gitlab-org/security-products/gemnasium-db/-/archive/master/gemnasium-db-master.zip"
    url = os.getenv(
        "GEMNASIUM_DATABASE_ZIP",
        "https://gitlab.com/gitlab-org/advisories-community/-/archive/main/advisories-community-main.zip",
    )

    semver_path = "/usr/local/bin/semver"
    required_tools_on_path = ["ruby"]

    def __init__(self):
        self.database_path = Path(self.__get_cache_dir()) / "gemnasium"

        if self.should_activate():
            if not Path(self.semver_path).exists():
                self.__extract_semver_to_local()
            self.__download_and_extract_database()

    def __extract_semver_to_local(self):
        """If the ruby semver command isn't installed then extract from this package."""
        data = pkgutil.get_data(__name__, "semver").decode("utf-8")
        self.semver_path = Path(tempfile.gettempdir()) / "semver"
        self.semver_path.write_text(data, encoding="utf-8")
        self.semver_path.chmod(mode=stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    def __download_and_extract_database(self):
        """Downloads the gymnasium database."""
        url = urlparse(self.url)

        path_to_zip_file = Path(self.__get_cache_dir()) / os.path.basename(url.path)

        def do_download_and_unpack():
            typer.echo(f"Updating Gemnasium database to {self.database_path}")
            request = requests.get(self.url, allow_redirects=True)
            with open(path_to_zip_file, "wb") as file:
                file.write(request.content)
                file.close()

            with zipfile.ZipFile(path_to_zip_file, "r") as zip_ref:
                zip_ref.extractall(self.database_path)

        if not path_to_zip_file.exists():
            do_download_and_unpack()
        else:
            file_time = os.path.getmtime(path_to_zip_file)
            # Check against 24 hours
            older_than_one_day = (time.time() - file_time) / 3600 > 24 * 1
            if older_than_one_day:
                shutil.rmtree(self.database_path / path_to_zip_file.stem)
                do_download_and_unpack()
        self.database_path = self.database_path / path_to_zip_file.stem

    def __is_affected_range(self, repository_format, version, affected_range) -> bool:
        """Checks if the version matches the affected range based on package manager specific semantic versioning.
        :param repository_format:
        :param version:
        :param affected_range:
        :return:
        """
        try:
            # Gemnasium docs list nuget as supported, however no results are returned
            # nuget package-versioning is based on maven dependency version
            # specification. Below repository_format override allows nuget vuln discovery
            # https://learn.microsoft.com/en-us/nuget/concepts/package-versioning
            # https://maven.apache.org/pom.html#dependency-version-requirement-specification
            repository_format = repository_format.replace("nuget", "maven")

            _win32 = sys.platform == "win32"
            output = subprocess.run(
                [
                    *(["ruby"] if _win32 else []),
                    self.semver_path,
                    "check_version",
                    repository_format,
                    version,
                    affected_range,
                ],
                capture_output=True,
                text=True,
                check=False,
                # TODO this command suddenly started throwing errors, not sure what changed but it needs investigated.
                # It looks like  a spell checker package changed
            )
            return "matches" in str(output)
        except Exception as err:
            print(f"Failed to check version for: {repository_format} {version} {err}")
            return False

    def get_vulnerabilities_by_purl(self, purls: list[PackageURL]) -> dict[str, list[cdx.Vulnerability] | None]:
        """Get the vulnerabilities for a list of package URLS (purls)
        This function will return a dictionary of package URL to vulnerabilities or none if no vulnerabilities are found.
        """
        vulnerabilities_by_purl = {}
        for purl in purls:
            purl_str = purl.to_string()
            vulnerabilities_by_purl[purl_str] = []

            if not (path := self.__get_path(purl)).exists():
                continue

            vuln_files = [file for file in path.glob("*") if file.is_file()]

            for vuln_file in vuln_files:
                try:
                    data = yaml.full_load(vuln_file.read_text(encoding="utf-8"))
                    vuln = GemnasiumVulnerability(**data)

                    if self.__is_affected_range(purl.type, purl.version, vuln.affected_range):
                        vulnerability = self.__convert_to_cyclone_dx(vuln)
                        if len(vulnerability.ratings) > 0:
                            vulnerabilities_by_purl[purl_str].append(vulnerability)
                except Exception:
                    print(f"failed to parse gemnasium file for {purl}")

        return vulnerabilities_by_purl

    @staticmethod
    def __convert_to_cyclone_dx(vuln: GemnasiumVulnerability) -> cdx.Vulnerability:
        """Converts a gemnasium vulnerabity to a vulnerability."""
        res = list(filter(lambda x: "cve-" in x.lower(), vuln.identifiers))
        vuln_id = res[0] if len(res) > 1 else vuln.identifiers[0]
        cwes = []
        if vuln.cwe_ids is not None:
            cwes = [int(x.replace("CWE-", "")) for x in vuln.cwe_ids]
        cyclone_vuln = cdx.Vulnerability(
            id=vuln_id,
            recommendation=vuln.solution,
            cwes=cwes,
            description=vuln.description,
            ratings=[],
            source=get_vulnerability_source(vuln_id),
        )
        cyclone_vuln.advisories = get_advisories_from_urls(vuln.urls)
        cyclone_vuln.references = get_references_from_ids(vuln.identifiers, cyclone_vuln.id)
        if vuln.cvss_v3 is not None:
            cvss = CVSS3(vuln.cvss_v3)
            cyclone_vuln.ratings.append(
                cdx.Rating(
                    score=cvss.base_score,
                    severity=cdx.Severity[cvss.severities()[0].lower()],
                    method=cdx.ScoreMethod.CVSSv3,
                    vector=str(cvss.clean_vector()),
                )
            )
        elif vuln.cvss_v2 is not None:
            cvss = CVSS2(vuln.cvss_v2)
            cyclone_vuln.ratings.append(
                cdx.Rating(
                    score=cvss.base_score,
                    severity=cdx.Severity[cvss.severities()[0].lower()],
                    method=cdx.ScoreMethod.CVSSv2,
                    vector=cvss.clean_vector(),
                )
            )
        cyclone_vuln.tools = [cdx.Tool(vendor="Gitlab", name="Gemnasium")]
        return cyclone_vuln

    @staticmethod
    def __get_cache_dir() -> Path:
        cache = os.getenv("CACHE_DIR")
        return Path(cache) if cache is not None else Path(tempfile.gettempdir())

    def __get_path(self, purl: PackageURL) -> Path:
        """Build a path to the gemnasium path."""
        repo_format = purl.type
        if repo_format == "npm":
            path_slug = Path("npm") / (purl.namespace or "") / purl.name
        elif repo_format == "maven":
            path_slug = Path("maven") / purl.namespace / purl.name
        elif repo_format == "golang":
            path_slug = Path("go") / purl.namespace / purl.name
        else:
            path_slug = Path(repo_format) / purl.name

        return self.database_path / path_slug

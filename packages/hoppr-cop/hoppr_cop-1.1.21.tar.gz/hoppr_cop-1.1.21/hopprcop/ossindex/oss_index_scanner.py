"""A vulnerability scanner that locates vulnerabilities in Sonotypes' OSS Index."""
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

from typing import TYPE_CHECKING

import hoppr_cyclonedx_models.cyclonedx_1_4 as cdx

from cvss import CVSS2, CVSS3
from cvss.exceptions import CVSS3MalformedError
from hoppr_security_commons.utils import (
    get_advisories_from_urls,
    get_vulnerability_source,
)
from hoppr_security_commons.vulnerability_scanner import VulnerabilitySuper
from packageurl import PackageURL
from requests.auth import HTTPBasicAuth

from hopprcop.ossindex.api.ossindex import OssIndex


if TYPE_CHECKING:
    from hopprcop.ossindex.api.model import OssIndexComponent, Vulnerability as OssVulnerability


class OSSIndexScanner(VulnerabilitySuper):
    """A vulnerability scanner that locates vulnerabilities in Sonotypes' OSS Index."""

    required_environment_variables = ["OSS_INDEX_TOKEN", "OSS_INDEX_USER"]
    api = OssIndex()
    api.osthentication = HTTPBasicAuth(os.getenv("OSS_INDEX_TOKEN"), os.getenv("OSS_INDEX_USER"))

    supported_types = [
        "npm",
        "maven",
        "pypi",
        "gem",
        "golang",
        "nuget",
        "rpm",
        "conan",
    ]

    def get_vulnerabilities_by_purl(self, purls: list[PackageURL]) -> dict[str, list[cdx.Vulnerability] | None]:
        """Get the vulnerabilities for a list of package URLS (purls)
        This function will return a dictionary of package URL to vulnerabilities or none if no vulnerabilities are found.
        """
        purls = list(filter(lambda x: x.type in self.supported_types, purls))
        cleaned_purl_map = {}

        def remove_qualifiers(pkg_url: PackageURL) -> PackageURL:
            before_cleaning = pkg_url.to_string()
            pkg_url.qualifiers.clear()
            if pkg_url.type == "rpm":
                pkg_url = PackageURL(name=pkg_url.name, type=pkg_url.type, version=pkg_url.version)
            cleaned_purl_map[pkg_url.to_string()] = before_cleaning
            return pkg_url

        purls = list(map(remove_qualifiers, purls))

        results: list[OssIndexComponent] = self.api.get_component_report(packages=purls)
        enhanced_results = {}

        for result in results:
            purl = result.coordinates
            enhanced_results[cleaned_purl_map[purl]] = []
            for vulnerability in result.vulnerabilities:
                enhanced_results[cleaned_purl_map[purl]].append(self.__convert_to_cyclone_dx(vulnerability))
        return enhanced_results

    @staticmethod
    def __convert_to_cyclone_dx(vulnerability: OssVulnerability) -> cdx.Vulnerability:
        """Convert an OSS Index vulnerability to cyclone dx."""
        vuln_id = vulnerability.cve if vulnerability.cve is not None else vulnerability.display_name

        try:
            cwes = [int((vulnerability.cwe or "").removeprefix("CWE-"))]
        except ValueError:
            cwes = []

        cyclone_vuln = cdx.Vulnerability(
            id=vuln_id,
            description=vulnerability.description,
            cwes=cwes,
            source=get_vulnerability_source(vuln_id),
        )
        cyclone_vuln.ratings = []
        if vulnerability.cvss_vector is not None:
            try:
                cvss = CVSS3(vulnerability.cvss_vector)
                cyclone_vuln.ratings.append(
                    cdx.Rating(
                        score=cvss.base_score,
                        severity=cdx.Severity[cvss.severities()[0].lower()],
                        method=cdx.ScoreMethod.CVSSv3,
                        vector=cvss.vector,
                    )
                )
            except CVSS3MalformedError:
                cvss = CVSS2(vulnerability.cvss_vector)
                cyclone_vuln.ratings.append(
                    cdx.Rating(
                        score=cvss.base_score,
                        severity=cdx.Severity[cvss.severities()[0].lower()],
                        method=cdx.ScoreMethod.CVSSv2,
                        vector=cvss.vector,
                    )
                )
        cyclone_vuln.advisories = get_advisories_from_urls(list(vulnerability.external_references))
        cyclone_vuln.tools = [cdx.Tool(vendor="Sonatype", name="OSS-Index")]

        return cyclone_vuln

"""This file contains auto generated pydantic models for the grype json output."""
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

from typing import Any

from pydantic import BaseModel, Field


class Fix(BaseModel):
    versions: list
    state: str


class Metrics(BaseModel):
    base_score: float = Field(..., alias="baseScore")
    exploitability_score: float = Field(..., alias="exploitabilityScore")
    impact_score: float = Field(..., alias="impactScore")


class Cvs(BaseModel):
    version: str
    vector: str
    metrics: Metrics
    vendor_metadata: dict[str, Any] = Field(..., alias="vendorMetadata")


class Vulnerability(BaseModel):
    id: str
    data_source: str = Field(..., alias="dataSource")
    namespace: str
    severity: str
    urls: list[str]
    description: str | None
    cvss: list[Cvs]
    fix: Fix
    advisories: list


class RelatedVulnerability(BaseModel):
    id: str
    data_source: str = Field(..., alias="dataSource")
    namespace: str
    severity: str | None
    urls: list[str]
    description: str
    cvss: list[Cvs]


class SearchedBy(BaseModel):
    language: str | None
    namespace: str | None


class Found(BaseModel):
    version_constraint: str = Field(..., alias="versionConstraint")


class MatchDetail(BaseModel):
    type: str
    matcher: str
    searched_by: SearchedBy = Field(..., alias="searchedBy")
    found: Found


class Artifact(BaseModel):
    name: str
    version: str
    type: str
    locations: list
    language: str
    licenses: list
    cpes: list
    purl: str
    upstreams: list


class Match(BaseModel):
    vulnerability: Vulnerability
    related_vulnerabilities: list[RelatedVulnerability] = Field(..., alias="relatedVulnerabilities")
    match_details: list[MatchDetail] = Field(..., alias="matchDetails")
    artifact: Artifact


class Source(BaseModel):
    type: str
    # target: [Optional[str]]


class Distro(BaseModel):
    name: str
    version: str
    id_like: Any = Field(..., alias="idLike")


class Search(BaseModel):
    scope: str
    unindexed_archives: bool = Field(..., alias="unindexed-archives")
    indexed_archives: bool = Field(..., alias="indexed-archives")


class Db(BaseModel):
    cache_dir: str = Field(..., alias="cache-dir")
    update_url: str = Field(..., alias="update-url")
    ca_cert: str = Field(..., alias="ca-cert")
    auto_update: bool = Field(..., alias="auto-update")
    validate_by_hash_on_start: bool = Field(..., alias="validate-by-hash-on-start")
    validate_age: bool = Field(..., alias="validate-age")
    max_allowed_built_age: int = Field(..., alias="max-allowed-built-age")


class Maven(BaseModel):
    search_upstream_by_sha1: bool = Field(..., alias="searchUpstreamBySha1")
    base_url: str = Field(..., alias="baseUrl")


class ExternalSources(BaseModel):
    enable: bool
    maven: Maven


class Dev(BaseModel):
    profile_cpu: bool = Field(..., alias="profile-cpu")
    profile_mem: bool = Field(..., alias="profile-mem")


class Registry(BaseModel):
    insecure_skip_tls_verify: bool = Field(..., alias="insecure-skip-tls-verify")
    insecure_use_http: bool = Field(..., alias="insecure-use-http")
    auth: list


class Log(BaseModel):
    structured: bool
    level: str
    file: str


class Attestation(BaseModel):
    public_key: str = Field(..., alias="public-key")
    skip_verification: bool = Field(..., alias="skip-verification")


class Configuration(BaseModel):
    config_path: str = Field(..., alias="configPath")
    output: str | list[str]
    file: str
    distro: str
    add_cpes_if_none: bool = Field(..., alias="add-cpes-if-none")
    output_template_file: str = Field(..., alias="output-template-file")
    quiet: bool
    check_for_app_update: bool = Field(..., alias="check-for-app-update")
    only_fixed: bool = Field(..., alias="only-fixed")
    only_notfixed: bool = Field(..., alias="only-notfixed")
    platform: str
    search: Search
    ignore: Any
    exclude: list
    db: Db
    external_sources: ExternalSources = Field(..., alias="externalSources")
    dev: Dev
    fail_on_severity: str = Field(..., alias="fail-on-severity")
    registry: Registry
    log: Log
    attestation: Attestation | None


class Db1(BaseModel):
    built: str
    schema_version: int = Field(..., alias="schemaVersion")
    location: str
    checksum: str
    error: Any


class Descriptor(BaseModel):
    name: str
    version: str
    configuration: Configuration
    db: Db1


class GrypeResult(BaseModel):
    matches: list[Match] = []
    source: Source | None = None
    distro: Distro | None = None
    descriptor: Descriptor | None = None

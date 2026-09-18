from __future__ import annotations

import ipaddress
import json
import socket
import ssl
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin, urlparse

import httpx
from sqlalchemy.orm import Session

from delicious_scanner.models import Finding, Scan, Target, utcnow
from delicious_scanner.security import redact

MAX_REQUESTS = 500
MAX_ENDPOINTS = 250
MAX_CAPTURE = 16_384


@dataclass(frozen=True)
class ScanSummary:
    endpoints: int
    requests: int
    findings: int


def _allowed_address(host: str, environment_class: str) -> tuple[bool, str]:
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        return False, f"DNS resolution failed: {exc}"
    addresses = sorted({str(item[4][0]) for item in infos})
    if not addresses:
        return False, "Target did not resolve to an address"
    for text in addresses:
        ip = ipaddress.ip_address(text)
        if ip.is_multicast or ip.is_unspecified or ip.is_link_local:
            return False, f"Target resolved to blocked address class: {text}"
        if ip.is_loopback and environment_class != "controlled-cloud":
            return False, "Loopback targets are allowed only for the controlled lab"
        if str(ip) == "169.254.169.254":
            return False, "Cloud metadata destinations are blocked"
    return True, ", ".join(addresses)


def _base_url(target: Target) -> str:
    default = (target.scheme == "https" and target.port == 443) or (
        target.scheme == "http" and target.port == 80
    )
    port = "" if default else f":{target.port}"
    path = target.base_path if target.base_path.startswith("/") else f"/{target.base_path}"
    if not path.endswith("/"):
        path += "/"
    return f"{target.scheme}://{target.host}{port}{path}"


def _same_authority(url: str, target: Target) -> bool:
    parsed = urlparse(url)
    expected_port = target.port
    actual_port = parsed.port or (443 if parsed.scheme == "https" else 80)
    return (
        parsed.scheme == target.scheme
        and (parsed.hostname or "").lower() == target.host.lower()
        and actual_port == expected_port
    )


def _finding(
    db: Session,
    scan: Scan,
    *,
    rule_id: str,
    severity: str,
    confidence: str,
    endpoint: str,
    title: str,
    description: str,
    remediation: str,
    evidence: dict[str, Any],
    method: str = "GET",
    owasp: str | None = None,
    cwe: str | None = None,
) -> None:
    db.add(
        Finding(
            scan=scan,
            rule_id=rule_id,
            severity=severity,
            confidence=confidence,
            state="CONFIRMED",
            method=method,
            endpoint=endpoint[:1024],
            title=title,
            description=description,
            evidence_json=json.dumps(redact(evidence), ensure_ascii=False)[:MAX_CAPTURE],
            remediation=remediation,
            owasp=owasp,
            cwe=cwe,
        )
    )


def _discover_openapi(
    client: httpx.Client, base: str, target: Target
) -> tuple[dict[str, Any] | None, int]:
    candidates = [urljoin(base, "openapi.json"), urljoin(base, "api/openapi.json")]
    requests = 0
    for candidate in candidates:
        if not _same_authority(candidate, target):
            continue
        try:
            response = client.get(candidate)
            requests += 1
        except httpx.HTTPError:
            continue
        if response.status_code != 200:
            continue
        ctype = response.headers.get("content-type", "")
        if "json" not in ctype.lower():
            continue
        try:
            document = response.json()
        except ValueError:
            continue
        if isinstance(document, dict) and isinstance(document.get("paths"), dict):
            return document, requests
    return None, requests


def _inventory(openapi: dict[str, Any] | None, base: str) -> list[tuple[str, str]]:
    operations: list[tuple[str, str]] = []
    if openapi:
        for path, item in openapi.get("paths", {}).items():
            if not isinstance(path, str) or not isinstance(item, dict):
                continue
            if "{" in path or "}" in path:
                continue
            for method in ("get", "head", "options"):
                if method in item:
                    operations.append((method.upper(), urljoin(base, path.lstrip("/"))))
                    break
    if not operations:
        operations = [("GET", base)]
    dedup: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for op in operations:
        if op not in seen:
            dedup.append(op)
            seen.add(op)
    return dedup[:MAX_ENDPOINTS]


def _check_response(db: Session, scan: Scan, response: httpx.Response, method: str) -> None:
    url = str(response.request.url)
    headers = {k.lower(): v for k, v in response.headers.items()}
    expected = {
        "x-content-type-options": (
            "nosniff",
            "Missing X-Content-Type-Options",
            "Add X-Content-Type-Options: nosniff.",
        ),
        "x-frame-options": (
            None,
            "Missing clickjacking protection",
            "Set X-Frame-Options or a CSP frame-ancestors directive.",
        ),
        "content-security-policy": (
            None,
            "Missing Content-Security-Policy",
            "Define a restrictive Content-Security-Policy where browser content is served.",
        ),
    }
    for key, (_, title, remediation) in expected.items():
        if key not in headers:
            _finding(
                db,
                scan,
                rule_id="CONFIG-HEADERS-001",
                severity="low",
                confidence="high",
                endpoint=url,
                title=title,
                description=f"The response did not include the security header {key}.",
                remediation=remediation,
                evidence={"status": response.status_code, "missing_header": key},
                method=method,
                owasp="API8:2023 Security Misconfiguration",
                cwe="CWE-693",
            )

    acao = headers.get("access-control-allow-origin")
    if acao == "*":
        _finding(
            db,
            scan,
            rule_id="CONFIG-CORS-001",
            severity="medium",
            confidence="high",
            endpoint=url,
            title="Permissive CORS policy",
            description="The endpoint allows any origin through Access-Control-Allow-Origin: *.",
            remediation="Restrict allowed origins to the explicitly trusted application origins.",
            evidence={"status": response.status_code, "access_control_allow_origin": "*"},
            method=method,
            owasp="API8:2023 Security Misconfiguration",
            cwe="CWE-942",
        )

    server = headers.get("server", "")
    if server:
        _finding(
            db,
            scan,
            rule_id="CONFIG-HEADERS-002",
            severity="info",
            confidence="high",
            endpoint=url,
            title="Server technology disclosed",
            description="The response exposes a Server header that may reveal implementation details.",
            remediation="Minimise unnecessary product/version disclosure in response headers.",
            evidence={"server": server[:200]},
            method=method,
            owasp="API8:2023 Security Misconfiguration",
        )

    if response.status_code >= 500:
        excerpt = response.text[:2000]
        keywords = ("traceback", "exception", "stack trace", "sqlalchemy", "syntaxerror")
        if any(word in excerpt.lower() for word in keywords):
            _finding(
                db,
                scan,
                rule_id="CONFIG-ERROR-001",
                severity="medium",
                confidence="medium",
                endpoint=url,
                title="Verbose server error disclosure",
                description="A server error response appears to disclose implementation or stack details.",
                remediation="Return generic production errors and retain detailed diagnostics only in protected logs.",
                evidence={"status": response.status_code, "excerpt": excerpt[:500]},
                method=method,
                owasp="API8:2023 Security Misconfiguration",
                cwe="CWE-209",
            )


def run_full_scan(db: Session, scan: Scan, target: Target) -> ScanSummary:
    scan.state = "RUNNING"
    scan.started_at = utcnow()
    scan.error_message = None
    db.commit()

    allowed, detail = _allowed_address(target.host, target.environment_class)
    if not allowed:
        scan.state = "BLOCKED"
        scan.error_message = detail
        scan.completed_at = utcnow()
        db.commit()
        return ScanSummary(0, 0, 0)

    base = _base_url(target)
    request_count = 0
    endpoint_count = 0
    try:
        with httpx.Client(
            timeout=httpx.Timeout(10.0, connect=5.0),
            follow_redirects=False,
            trust_env=False,
            headers={"User-Agent": "Delicious-Scanner/0.2 (+authorised-read-only)"},
            verify=True,
        ) as client:
            openapi, used = _discover_openapi(client, base, target)
            request_count += used
            operations = _inventory(openapi, base)
            endpoint_count = len(operations)

            if openapi is None:
                _finding(
                    db,
                    scan,
                    rule_id="INVENTORY-DIFF-001",
                    severity="info",
                    confidence="medium",
                    endpoint=base,
                    title="OpenAPI specification not discovered",
                    description="The scanner could not discover an OpenAPI document at the standard same-host locations.",
                    remediation="Publish or import an approved OpenAPI specification for complete API inventory coverage.",
                    evidence={"checked": ["openapi.json", "api/openapi.json"]},
                    owasp="API9:2023 Improper Inventory Management",
                )
            else:
                docs_url = urljoin(base, "docs")
                try:
                    docs = client.get(docs_url)
                    request_count += 1
                    if docs.status_code == 200:
                        _finding(
                            db,
                            scan,
                            rule_id="CONFIG-DOCS-001",
                            severity="low",
                            confidence="high",
                            endpoint=docs_url,
                            title="Interactive API documentation exposed",
                            description="Interactive API documentation is reachable from the scanned target.",
                            remediation="Restrict documentation in production environments unless it is intentionally public.",
                            evidence={"status": docs.status_code},
                            owasp="API9:2023 Improper Inventory Management",
                        )
                except httpx.HTTPError:
                    pass

            if target.scheme == "http":
                _finding(
                    db,
                    scan,
                    rule_id="CONFIG-TLS-001",
                    severity="high",
                    confidence="high",
                    endpoint=base,
                    title="API is served without TLS",
                    description="The registered API target uses clear-text HTTP.",
                    remediation="Serve production APIs exclusively over HTTPS with a valid, maintained TLS configuration.",
                    evidence={"scheme": "http"},
                    owasp="API8:2023 Security Misconfiguration",
                    cwe="CWE-319",
                )

            for method, url in operations:
                if request_count >= MAX_REQUESTS:
                    break
                if not _same_authority(url, target):
                    continue
                try:
                    response = client.request(method, url)
                except (httpx.HTTPError, ssl.SSLError) as exc:
                    _finding(
                        db,
                        scan,
                        rule_id="TRANSPORT-ERROR-001",
                        severity="info",
                        confidence="high",
                        endpoint=url,
                        title="Endpoint could not be evaluated",
                        description="The endpoint could not be reached within the bounded scan.",
                        remediation="Confirm target availability, TLS trust and authorised network reachability.",
                        evidence={"error": type(exc).__name__},
                        method=method,
                    )
                    request_count += 1
                    continue
                request_count += 1
                _check_response(db, scan, response, method)
    except Exception as exc:
        scan.state = "ERROR"
        scan.error_message = f"{type(exc).__name__}: {str(exc)[:300]}"
    else:
        scan.state = "COMPLETED"
    finally:
        scan.request_count = request_count
        scan.endpoint_count = endpoint_count
        scan.finding_count = len(scan.findings)
        scan.completed_at = utcnow()
        db.commit()

    return ScanSummary(endpoint_count, request_count, scan.finding_count)

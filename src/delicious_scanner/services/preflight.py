from __future__ import annotations

from dataclasses import dataclass

from delicious_scanner.models import Target


@dataclass(frozen=True)
class PreflightResult:
    ok: bool
    checks: tuple[tuple[str, str, bool], ...]


def run_preflight(target: Target, profile: str) -> PreflightResult:
    checks: list[tuple[str, str, bool]] = [
        ("Explicit target", target.host, bool(target.host.strip())),
        ("Scheme", target.scheme, target.scheme in {"http", "https"}),
        ("Port", str(target.port), 1 <= target.port <= 65535),
        (
            "Profile",
            profile,
            profile in {"safe-read-only", "controlled-lab-full", "authorised-zchpc"},
        ),
    ]
    controlled = target.environment_class == "controlled-cloud"
    if not controlled:
        checks.append(
            (
                "Authorisation reference",
                target.authorisation_reference or "Missing",
                bool(target.authorisation_reference),
            )
        )
    checks.extend(
        [
            ("Mutation tests", "disabled in Full Scan", True),
            ("Resource-control tests", "disabled in Full Scan", True),
            ("Exact-host scope", "same registered host and port only", True),
            ("Request budget", "maximum 500 requests", True),
        ]
    )
    return PreflightResult(ok=all(item[2] for item in checks), checks=tuple(checks))

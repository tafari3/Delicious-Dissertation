from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from delicious_scanner.db import Base
from delicious_scanner.models import Finding, Project, Scan, Target
from delicious_scanner.services.reports import report_bytes
from delicious_scanner.services.scanner import _allowed_address


def test_scope_blocks_loopback_for_operational_target() -> None:
    allowed, _ = _allowed_address("127.0.0.1", "authorised-government")
    assert allowed is False


def test_scope_allows_loopback_for_controlled_lab() -> None:
    allowed, _ = _allowed_address("127.0.0.1", "controlled-cloud")
    assert allowed is True


def test_all_report_formats_render() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        project = Project(name="Agency", description="Test")
        db.add(project)
        db.flush()
        target = Target(
            project_id=project.id,
            name="Citizen API",
            scheme="https",
            host="api.example.test",
            port=443,
            base_path="/",
            environment_class="authorised-government",
            authorisation_reference="TEST-001",
        )
        db.add(target)
        db.flush()
        scan = Scan(
            project_id=project.id,
            target_id=target.id,
            profile="safe-read-only",
            state="COMPLETED",
            endpoint_count=1,
            request_count=1,
            finding_count=1,
        )
        db.add(scan)
        db.flush()
        db.add(
            Finding(
                scan_id=scan.id,
                rule_id="CONFIG-HEADERS-001",
                severity="low",
                confidence="high",
                state="CONFIRMED",
                method="GET",
                endpoint="https://api.example.test/",
                title="Missing security header",
                description="Header not observed.",
                evidence_json="{}",
                remediation="Add the security header.",
                owasp="API8:2023 Security Misconfiguration",
            )
        )
        db.commit()
        db.refresh(scan)
        for fmt in ("html", "pdf", "json", "csv"):
            content, media_type = report_bytes(scan, fmt)
            assert len(content) > 100
            assert media_type

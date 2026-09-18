from delicious_scanner.models import Target
from delicious_scanner.services.preflight import run_preflight


def make_target(environment: str = "controlled-cloud", auth: str | None = None) -> Target:
    return Target(
        project_id=1,
        name="Target",
        scheme="https",
        host="example.test",
        port=443,
        base_path="/",
        environment_class=environment,
        authorisation_reference=auth,
    )


def test_controlled_lab_is_ready_for_safe_read_only_scan() -> None:
    result = run_preflight(make_target(), "safe-read-only")
    assert result.ok is True
    assert any(name == "Exact-host scope" and ok for name, _, ok in result.checks)


def test_operational_target_requires_authorisation_reference() -> None:
    result = run_preflight(make_target("authorised-government"), "safe-read-only")
    assert result.ok is False
    assert any(name == "Authorisation reference" and not ok for name, _, ok in result.checks)


def test_operational_target_with_reference_is_ready() -> None:
    result = run_preflight(make_target("authorised-government", "APPROVAL-001"), "safe-read-only")
    assert result.ok is True

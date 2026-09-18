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


def test_preflight_keeps_network_locked_until_p4() -> None:
    result = run_preflight(make_target(), "safe-read-only")
    assert result.ok is False
    assert any(name == "Network execution" and not ok for name, _, ok in result.checks)


def test_operational_profile_requires_authorisation_reference() -> None:
    result = run_preflight(make_target("authorised-zchpc"), "authorised-zchpc")
    assert any(name == "Authorisation reference" and not ok for name, _, ok in result.checks)

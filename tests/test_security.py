from delicious_scanner.security import redact, sanitise_terminal


def test_redaction_removes_structured_secrets() -> None:
    result = redact({"Authorization": "Bearer secret", "nested": {"token": "abc", "safe": "ok"}})
    assert result["Authorization"] == "[REDACTED]"
    assert result["nested"]["token"] == "[REDACTED]"
    assert result["nested"]["safe"] == "ok"


def test_terminal_controls_are_removed() -> None:
    assert sanitise_terminal("safe\x1b[31mtext") == "safe[31mtext"

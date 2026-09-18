from delicious_scanner.auth import hash_password, verify_password


def test_password_hash_round_trip() -> None:
    encoded = hash_password("correct horse battery staple", salt=b"fixed-test-salt!!")
    assert verify_password("correct horse battery staple", encoded)
    assert not verify_password("incorrect", encoded)


def test_password_hash_is_not_plaintext() -> None:
    password = "research-console-password"
    encoded = hash_password(password, salt=b"another-test-salt")
    assert password not in encoded
    assert encoded.startswith("pbkdf2_sha256$")

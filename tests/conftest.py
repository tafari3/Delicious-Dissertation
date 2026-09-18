from __future__ import annotations

import os
from pathlib import Path

os.environ["DELICIOUS_DATABASE_URL"] = "sqlite:///./.data/test-scanner.db"
Path(".data").mkdir(exist_ok=True)

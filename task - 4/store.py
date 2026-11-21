import json
import os
import tempfile
import threading
from copy import deepcopy
from pathlib import Path


DATA_FILE = Path(os.getenv("DATA_FILE", Path(__file__).parent / "data" / "data.json"))
_lock = threading.RLock()


def load_users() -> list[dict]:
    with _lock:
        if not DATA_FILE.exists():
            DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
            DATA_FILE.write_text("[]\n", encoding="utf-8")
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise RuntimeError("DATA_FILE must contain a JSON array")
        return deepcopy(data)


def save_users(users: list[dict]) -> None:
    with _lock:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(
            dir=str(DATA_FILE.parent), prefix=".users-", suffix=".json"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as file:
                json.dump(users, file, indent=2, ensure_ascii=False)
                file.write("\n")
            os.replace(temp_name, DATA_FILE)
        except Exception:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
            raise

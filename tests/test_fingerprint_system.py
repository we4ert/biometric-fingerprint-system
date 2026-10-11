import json
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Tuple


def build_fingerprint_template(sample: str) -> List[int]:
    if not sample or not sample.strip():
        raise ValueError("La donnée de l'empreinte ne peut pas être vide.")

    normalized = sample.strip().lower()
    digest = sha256(normalized.encode("utf-8")).digest()
    return [int(byte) for byte in digest]


def compare_fingerprints(template_a: List[int], template_b: List[int]) -> float:
    if len(template_a) != len(template_b):
        return 0.0

    matches = sum(1 for a, b in zip(template_a, template_b) if a == b)
    return matches / len(template_a)


@dataclass
class FingerprintRecord:
    user_id: str
    template: List[int]
    created_at: str


class FingerprintDatabase:
    def __init__(self, storage_path: str = "data/fingerprints.json") -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._records: Dict[str, Dict[str, Any]] = self._load()

    def _load(self) -> Dict[str, Dict[str, Any]]:
        if not self.storage_path.exists():
            return {}

        try:
            with self.storage_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            return {}

        return {}

    def _save(self) -> None:
        with self.storage_path.open("w", encoding="utf-8") as file:
            json.dump(self._records, file, ensure_ascii=False, indent=2)

    def register_user(self, user_id: str, sample: str) -> FingerprintRecord:
        if not user_id or not user_id.strip():
            raise ValueError("L'identifiant utilisateur est obligatoire.")

        if user_id in self._records:
            raise ValueError(f"L'utilisateur '{user_id}' existe déjà.")

        template = build_fingerprint_template(sample)
        record = {
            "template": template,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._records[user_id] = record
        self._save()
        return FingerprintRecord(user_id=user_id, template=template, created_at=record["created_at"])

    def verify(self, user_id: str, sample: str, threshold: float = 0.90) -> Tuple[bool, float]:
        if user_id not in self._records:
            return False, 0.0

        candidate = build_fingerprint_template(sample)
        stored = self._records[user_id]["template"]
        score = compare_fingerprints(candidate, stored)
        accepted = score >= threshold
        return accepted, score

    def list_users(self) -> List[str]:
        return sorted(self._records.keys())

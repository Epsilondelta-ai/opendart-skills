from __future__ import annotations

import json
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path

DEFAULT_CACHE_DIRNAME = "opendart-skills"
DEFAULT_CORP_CODE_TTL_DAYS = 7


def cache_root(base_dir: str | Path | None = None) -> Path:
    if base_dir is not None:
        path = Path(base_dir).expanduser()
    else:
        env = os.environ.get("OPENDART_CACHE_DIR")
        if env:
            path = Path(env).expanduser()
        else:
            xdg = os.environ.get("XDG_CACHE_HOME")
            parent = Path(xdg).expanduser() if xdg else Path.home() / ".cache"
            path = parent / DEFAULT_CACHE_DIRNAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def corp_code_archive_path(base_dir: str | Path | None = None) -> Path:
    return cache_root(base_dir) / "corpCode.zip"


def corp_code_xml_path(base_dir: str | Path | None = None) -> Path:
    return cache_root(base_dir) / "corpCode.xml"


def corp_code_meta_path(base_dir: str | Path | None = None) -> Path:
    return cache_root(base_dir) / "corpCode.meta.json"


def corp_code_ttl_days() -> int:
    raw = os.environ.get("OPENDART_CORP_CODE_TTL_DAYS")
    if raw is None:
        return DEFAULT_CORP_CODE_TTL_DAYS
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_CORP_CODE_TTL_DAYS
    return max(1, value)


def _normalize_datetime(value: datetime | str | None) -> datetime:
    if value is None:
        return datetime.now(UTC)
    if isinstance(value, datetime):
        dt = value
    else:
        dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt


def write_corp_code_metadata(
    base_dir: str | Path | None = None,
    *,
    fetched_at: datetime | str | None = None,
    ttl_seconds: int | None = None,
) -> dict[str, object]:
    fetched = _normalize_datetime(fetched_at)
    payload: dict[str, object] = {
        "fetched_at": fetched.isoformat(),
        "ttl_days": corp_code_ttl_days(),
    }
    if ttl_seconds is not None:
        payload["ttl_seconds"] = max(1, int(ttl_seconds))
    corp_code_meta_path(base_dir).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def read_corp_code_metadata(base_dir: str | Path | None = None) -> dict[str, object] | None:
    path = corp_code_meta_path(base_dir)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _hint_for_reason(reason: str) -> str:
    hints = {
        "missing_xml_cache": "Refresh corp-code cache before searching or company lookup.",
        "missing_metadata": "Refresh corp-code cache to restore freshness metadata.",
        "missing_fetched_at": "Refresh corp-code cache to recreate fetched_at metadata.",
        "invalid_fetched_at": "Refresh corp-code cache because metadata is corrupted.",
        "ttl_expired": "Refresh corp-code cache because TTL expired.",
        "fresh": "Cache is fresh enough to reuse.",
    }
    return hints.get(reason, "Inspect corp-code cache status and refresh if unsure.")


def corp_code_cache_status(base_dir: str | Path | None = None, *, now: datetime | None = None) -> dict[str, object]:
    xml_path = corp_code_xml_path(base_dir)
    archive_path = corp_code_archive_path(base_dir)
    meta = read_corp_code_metadata(base_dir)
    reference = now or datetime.now(UTC)
    result = {
        "exists": xml_path.exists(),
        "xml_path": str(xml_path),
        "archive_path": str(archive_path),
        "meta_path": str(corp_code_meta_path(base_dir)),
        "ttl_days": corp_code_ttl_days(),
        "stale": False,
        "reason": "fresh",
        "hint": _hint_for_reason("fresh"),
        "fetched_at": None,
    }
    if not xml_path.exists():
        result["stale"] = True
        result["reason"] = "missing_xml_cache"
        result["hint"] = _hint_for_reason("missing_xml_cache")
        return result
    if meta is None:
        result["stale"] = True
        result["reason"] = "missing_metadata"
        result["hint"] = _hint_for_reason("missing_metadata")
        return result
    fetched_at = meta.get("fetched_at")
    if not fetched_at:
        result["stale"] = True
        result["reason"] = "missing_fetched_at"
        result["hint"] = _hint_for_reason("missing_fetched_at")
        return result
    try:
        fetched_dt = _normalize_datetime(str(fetched_at))
    except ValueError:
        result["stale"] = True
        result["reason"] = "invalid_fetched_at"
        result["hint"] = _hint_for_reason("invalid_fetched_at")
        return result
    if "ttl_seconds" in meta:
        ttl = timedelta(seconds=int(meta["ttl_seconds"]))
    else:
        ttl = timedelta(days=int(meta.get("ttl_days") or corp_code_ttl_days()))
    result["fetched_at"] = fetched_dt.isoformat()
    if fetched_dt + ttl < reference:
        result["stale"] = True
        result["reason"] = "ttl_expired"
        result["hint"] = _hint_for_reason("ttl_expired")
        return result
    return result

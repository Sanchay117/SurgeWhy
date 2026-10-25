"""Configuration loader for SurgeWhy (Zetaris + Meterless Engines + Nightshift Nemotron)."""

from __future__ import annotations

import os
import pathlib
from dataclasses import dataclass

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent


def _load_dotenv_if_present(env_path: pathlib.Path) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


@dataclass(frozen=True)
class SurgeWhyConfig:
    sample_mode: bool
    zetaris_base_url: str
    zetaris_rest_url: str
    zetaris_org_id: str
    zetaris_api_key: str
    meterless_base_url: str
    meterless_runtime_token: str
    meterless_app_name: str
    meterless_scope: str
    fast_model: str
    deep_model: str
    server_port: int
    sample_dir: pathlib.Path
    runtime_hmem_path: pathlib.Path


def load_config(force_live: bool = False) -> SurgeWhyConfig:
    _load_dotenv_if_present(ROOT_DIR / ".env")
    _load_dotenv_if_present(ROOT_DIR / ".env.local")

    raw_sample = os.environ.get("SAMPLE_MODE", "true").strip().lower()
    sample_mode = False if force_live else raw_sample not in ("false", "0", "no")

    meterless_base = (
        os.environ.get("METERLESS_BASE_URL")
        or os.environ.get("MODEL_BASE_URL")
        or "http://127.0.0.1:8088/v1"
    ).rstrip("/")

    meterless_token = (
        os.environ.get("METERLESS_RUNTIME_TOKEN")
        or os.environ.get("MODEL_API_KEY")
        or "sample-nightshift-token"
    )

    fast_model = (
        os.environ.get("METERLESS_FAST_MODEL")
        or os.environ.get("METERLESS_MODEL")
        or os.environ.get("NEMOTRON_MODEL")
        or "nvidia/nemotron-3.5-lightning-30b-a3b"
    )
    deep_model = (
        os.environ.get("METERLESS_DEEP_MODEL")
        or "nvidia/nemotron-3.5-super-vl-120b-a12b"
    )

    return SurgeWhyConfig(
        sample_mode=sample_mode,
        zetaris_base_url=os.environ.get("ZETARIS_BASE_URL", "http://localhost:3000").rstrip("/"),
        zetaris_rest_url=os.environ.get("ZETARIS_REST_URL", "http://localhost:8888/api/v1.0").rstrip("/"),
        zetaris_org_id=os.environ.get("ZETARIS_ORG_ID", "1"),
        zetaris_api_key=os.environ.get("ZETARIS_API_KEY", "sample-zetaris-key"),
        meterless_base_url=meterless_base,
        meterless_runtime_token=meterless_token,
        meterless_app_name=os.environ.get("METERLESS_APP_NAME", "surgewhy-agent"),
        meterless_scope=os.environ.get("METERLESS_SCOPE", "user"),
        fast_model=fast_model,
        deep_model=deep_model,
        server_port=int(os.environ.get("SURGEWHY_PORT", "8060")),
        sample_dir=ROOT_DIR / "data" / "sample",
        runtime_hmem_path=ROOT_DIR / "data" / "runtime_hmem.json",
    )

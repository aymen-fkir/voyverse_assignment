import logging
import sys
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Optional


class VoyverseLogger:
    """
    Centralized logger for the ETL pipeline.
    Supports console + rotating file output, with per-stage context.
    """

    _instances: dict[str, "VoyverseLogger"] = {}

    def __init__(
        self,
        name: str,
        log_dir: str = "logs",
        level: int = logging.DEBUG,
        max_bytes: int = 5 * 1024 * 1024,  # 5 MB
        backup_count: int = 3,
        console: bool = True,
    ):
        self.name = name
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        self._logger.handlers.clear()  # avoid duplicate handlers on re-init

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # — Console handler
        if console:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            self._logger.addHandler(stream_handler)

        # — Rotating file handler
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            filename=log_path / f"{name}.log",
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    @classmethod
    def get(cls, name: str, **kwargs) -> "VoyverseLogger":
        """Return a cached instance — one logger per name."""
        if name not in cls._instances:
            cls._instances[name] = cls(name, **kwargs)
        return cls._instances[name]

    # ── Core log methods ────────────────────────────────────────────────────

    def debug(self, msg: str, **ctx) -> None:
        self._logger.debug(self._fmt(msg, ctx))

    def info(self, msg: str, **ctx) -> None:
        self._logger.info(self._fmt(msg, ctx))

    def warning(self, msg: str, **ctx) -> None:
        self._logger.warning(self._fmt(msg, ctx))

    def error(self, msg: str, exc: Optional[BaseException] = None, **ctx) -> None:
        self._logger.error(self._fmt(msg, ctx), exc_info=exc)

    def critical(self, msg: str, exc: Optional[BaseException] = None, **ctx) -> None:
        self._logger.critical(self._fmt(msg, ctx), exc_info=exc)

    # ── ETL-specific helpers ────────────────────────────────────────────────

    def stage_start(self, stage: str) -> None:
        self.info(f"▶ Starting stage", stage=stage)

    def stage_end(self, stage: str, count: Optional[int] = None) -> None:
        extra = {"stage": stage}
        if count is not None:
            extra["records"] = count #type: ignore
        self.info(f"✔ Completed stage", **extra)

    def skipped(self, obj_type: str, obj_id: str) -> None:
        self.warning("Skipping unknown type", type=obj_type, id=obj_id)

    def batch_progress(self, current: int, total: int, label: str = "records") -> None:
        pct = round((current / total) * 100, 1) if total else 0
        self.debug(f"Batch progress", processed=f"{current}/{total}", pct=f"{pct}%", label=label)

    # ── Internal ────────────────────────────────────────────────────────────

    @staticmethod
    def _fmt(msg: str, ctx: dict) -> str:
        """Append structured key=value context to the message."""
        if not ctx:
            return msg
        pairs = " | ".join(f"{k}={v}" for k, v in ctx.items())
        return f"{msg} | {pairs}"
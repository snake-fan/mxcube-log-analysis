from datetime import datetime, timedelta
from typing import Protocol


class LogReader(Protocol):
    def read(self, device_id: str, occurred_at: datetime, window_minutes: int) -> list[str]:
        """Read device logs for the requested time window."""


class FixtureLogReader:
    def read(self, device_id: str, occurred_at: datetime, window_minutes: int) -> list[str]:
        start = occurred_at - timedelta(minutes=window_minutes)
        return [
            f"{start.isoformat()} {device_id} INFO device heartbeat ok",
            f"{occurred_at.isoformat()} {device_id} WARNING motor response latency increased",
            (
                f"{occurred_at.isoformat()} {device_id} ERROR controller timeout while waiting "
                "for axis ready"
            ),
            f"{occurred_at.isoformat()} {device_id} INFO recovery command queued by operator panel",
        ]


class SSHLogReader:
    def read(self, device_id: str, occurred_at: datetime, window_minutes: int) -> list[str]:
        raise NotImplementedError(
            "Configure an SSHLogReader implementation before setting MXCUBE_LOG_READER_MODE=ssh."
        )

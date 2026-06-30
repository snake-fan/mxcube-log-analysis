from datetime import datetime

from app.log_collection.readers import LogReader


class LogCollectionService:
    def __init__(self, reader: LogReader) -> None:
        self._reader = reader

    def collect(self, device_id: str, occurred_at: datetime, window_minutes: int) -> list[str]:
        return self._reader.read(device_id, occurred_at, window_minutes)


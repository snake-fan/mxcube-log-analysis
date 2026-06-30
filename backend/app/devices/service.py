from app.diagnoses.schemas import Device


class DeviceService:
    def get_device(self, device_id: str) -> Device:
        return Device(device_id=device_id, display_name=f"MXCuBE {device_id}")


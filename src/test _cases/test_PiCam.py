import types
import pytest

import photo as photo_module  # <-- adjust if your file has a different name


class DummyCamera:
    def __init__(self):
        self.called = []

    def create_still_configuration(self, **kwargs):
        self.called.append(("create_still_configuration", kwargs))
        return {"dummy": "config"}

    def configure(self, config):
        self.called.append(("configure", config))

    def start(self):
        self.called.append(("start", None))

    def capture_file(self, path):
        self.called.append(("capture_file", path))

    def stop(self):
        self.called.append(("stop", None))


@pytest.fixture
def fake_picamera(monkeypatch):
    dummy = DummyCamera()
    # Replace Picamera2 with our dummy
    monkeypatch.setattr(photo_module, "Picamera2", lambda: dummy)
    # Also stub out time.sleep so tests run instantly
    monkeypatch.setattr(photo_module, "time", types.SimpleNamespace(sleep=lambda x: None))
    return dummy


def test_photo_runs_all_camera_steps(fake_picamera):
    # Run the function under test
    photo_module.photo()

    # Collect the sequence of calls made
    calls = [c[0] for c in fake_picamera.called]

    # Ensure all expected steps are called in order
    assert calls == [
        "create_still_configuration",
        "configure",
        "start",
        "capture_file",
        "stop",
    ]

    # Verify correct capture path
    capture_call = [c for c in fake_picamera.called if c[0] == "capture_file"][0]
    assert capture_call[1] == "/home/pi/ET0735/Smart_FireAlert_System_AIoT/src/static/test.jpg"

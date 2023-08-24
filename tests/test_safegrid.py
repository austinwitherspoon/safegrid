import safegrid
from shotgun_api3.lib import mockgun


class Version(safegrid.Entity):
    type = "Version"
    sg_path_to_frames: dict
    code: str
    description: str


def test_find(sg: mockgun.Shotgun):
    shots = sg.find("Shot", [], ["code", "created_at"])
    assert len(shots) > 0

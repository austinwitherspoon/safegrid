import pickle

import pytest
from shotgun_api3.lib import mockgun


@pytest.fixture(scope="function")
def sg():
    """Preps a mockgun instance with the schema and data from the demo site."""
    mockgun.Shotgun.set_schema_paths("./mockgun/schema", "./mockgun/entity_schema")
    sg = mockgun.Shotgun(
        "https://mysite.shotgunstudio.com", script_name="xyz", api_key="abc"
    )
    data_dump = pickle.load(open("./mockgun/entity_dump.pickle", "rb"))
    for entity_name, entities in data_dump.items():
        for entity in entities:
            entity.pop("type")
            row = sg._get_new_row(entity_name)
            sg._update_row(entity_name, row, entity)
            sg._db[entity_name][entity["id"]] = row
    return sg

"""Script intended to run against a demo shotgun site,
which will copy the schema and data to the repo for testing purposes.
"""
import contextlib
import os
import pickle

from shotgun_api3 import Fault, Shotgun
from shotgun_api3.lib import mockgun

sg = Shotgun(
    os.environ["SG_SITE"],
    script_name=os.environ["SG_SCRIPT"],
    api_key=os.environ["SG_KEY"],
)
print("Generating schema files..")
mockgun.generate_schema(sg, "./mockgun/schema", "./mockgun/entity_schema")

print("Downloading entity data..")
schema: dict = sg.schema_read()  # type:ignore
dump = {}
for i, (entity_name, entity_data) in enumerate(schema.items()):
    with contextlib.suppress(Fault):  # API read error on MimEntity?!
        print(f"Downloading {entity_name} [{i}/{len(schema)}]...")
        fields = list(entity_data.keys())
        entities = sg.find(entity_name, [], fields)
        dump[entity_name] = entities

pickle.dump(dump, open("./mockgun/entity_dump.pickle", "wb"))

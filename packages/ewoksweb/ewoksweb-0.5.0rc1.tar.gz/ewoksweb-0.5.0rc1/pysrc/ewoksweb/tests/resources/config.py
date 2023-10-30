from pathlib import Path
import os


RESOURCE_DIRECTORY = str(Path(__file__).resolve().parent)

DB_FILEPATH = os.path.join(RESOURCE_DIRECTORY, "ewoks_events.db")

if os.path.exists(DB_FILEPATH):
    os.remove(DB_FILEPATH)

EWOKS = {
    "handlers": [
        {
            "class": "ewokscore.events.handlers.Sqlite3EwoksEventHandler",
            "arguments": [{"name": "uri", "value": f"file:{DB_FILEPATH}"}],
        }
    ]
}

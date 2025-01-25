import logging
from homeassistant.helpers.entity import Entity
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    db_path = hass.data[DOMAIN][config_entry.entry_id]["db_path"]
    async_add_entities([WhiskyCollectionSensor(db_path)], True)

class WhiskyCollectionSensor(Entity):
    def __init__(self, db_path):
        self._db_path = db_path
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return "Whisky Collection"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_update(self):
        import aiosqlite
        
        async with aiosqlite.connect(self._db_path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM whiskies")
            row = await cursor.fetchone()
            self._state = row[0] if row else 0
            
            cursor = await db.execute("SELECT type, COUNT(*) FROM whiskies GROUP BY type")
            rows = await cursor.fetchall()
            self._attributes = {row[0]: row[1] for row in rows}

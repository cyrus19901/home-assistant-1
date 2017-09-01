"""
The "devices list" component.

"""

import asyncio
import logging
import os
import json
from datetime import timedelta
from homeassistant.config import load_yaml_config_file
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.core import State


_LOGGER = logging.getLogger(__name__)

DOMAIN = "connected_devices"
FROM = "from"
SCAN_INTERVAL = timedelta(3600)

DEPENDENCIES = []

def setup(hass, config):
    """Setup our skeleton component."""

    _LOGGER.info("Connected Devices loading.")
    
    component = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)

    component.setup(config)

    descriptions = load_yaml_config_file(
        os.path.join(os.path.dirname(__file__), 'services.yaml'))

    def update_connected_device(service):
        """Update a transactive home device."""

        update_obj = service.data.get('value')

        connected_devices = hass.states.get('connected_devices.connected_devices').as_dict()
        
        attributes = connected_devices["attributes"]

        for obj in update_obj:
            attributes["devices"][obj["device"]][obj["target"]] = obj["value"]

        connected_devices["attributes"] = attributes

        hass.states.set('connected_devices.connected_devices', 'On', attributes, True)

    hass.services.register(
        DOMAIN,
        'update_connected_device',
        update_connected_device,
        descriptions['update_connected_device'])

    return True


class ConnectedDevicesComponent(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""

        _LOGGER.info("ConnectedDevicesPlatform loading.")

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Connected Devices'

    @property
    def state(self):
        """Camera state."""
        return 'happy'

    @property
    def overall_reduction(self):
        """Return the name of the sensor."""
        return 84

    @property
    def state_attributes(self):
        """Return the optional state attributes."""

        data = {
            "devices": {
                "AC1":  {
                    "participate": True,
                    "reset": False,
                    "zone_min": 0,
                    "zone_max": 1,
                    "power": 0,
                    "energy": 0,
                    "flexibility": "high"
                },
                "AC2": {
                    "participate": True,
                    "reset": False,
                    "zone_min": 0,
                    "zone_max": 1,
                    "power": 0,
                    "energy": 0,
                    "flexibility": "low"
                },
                "WH1": {
                    "participate": True,
                    "reset": False,
                    "zone_min": 0,
                    "zone_max": 1,
                    "power": 0,
                    "energy": 0,
                    "flexibility": "low"
                }
            }
        }

        return data

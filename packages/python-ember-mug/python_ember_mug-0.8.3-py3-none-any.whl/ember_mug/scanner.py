"""Scanning tools for finding mugs."""
from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

from bleak import BleakScanner

from .consts import EMBER_BLUETOOTH_NAMES, IS_LINUX, MugCharacteristic

if TYPE_CHECKING:
    from collections.abc import Callable

    from bleak.backends.device import BLEDevice
    from bleak.backends.scanner import AdvertisementData


logger = logging.getLogger(__name__)


def build_scanner_kwargs(adapter: str | None = None) -> dict[str, Any]:
    """Add Adapter to kwargs for scanner if specified and using BlueZ."""
    if adapter and IS_LINUX is not True:
        msg = "The adapter option is only valid for the Linux BlueZ Backend."
        raise ValueError(msg)
    return {"adapter": adapter} if adapter else {}


async def discover_mugs(mac: str | None = None, adapter: str | None = None, wait: int = 5) -> list[BLEDevice]:
    """Discover new mugs in pairing mode."""
    scanner_kwargs = build_scanner_kwargs(adapter)
    service_uuids = [str(uuid) for uuid in (MugCharacteristic.STANDARD_SERVICE, MugCharacteristic.TRAVEL_MUG_SERVICE)]
    async with BleakScanner(service_uuids=service_uuids, **scanner_kwargs) as scanner:
        await asyncio.sleep(wait)
        if mac:
            mac = mac.lower()
            return [d for d in scanner.discovered_devices if d.address.lower() == mac]
        return scanner.discovered_devices


def build_find_filter(mac: str | None = None) -> Callable:
    """Create a filter for finding the mug by name and or mac address."""
    known_names = [n.lower() for n in EMBER_BLUETOOTH_NAMES]

    def mug_filter(device: BLEDevice, advertisement: AdvertisementData) -> bool:
        """Filter by mac if specified else just check the name."""
        if mac is not None and device.address.lower() != mac:
            return False
        return bool(device.name and device.name.lower() in known_names)

    return mug_filter


async def find_mug(mac: str | None = None, adapter: str | None = None) -> BLEDevice | None:
    """Find a mug."""
    if mac is not None:
        mac = mac.lower()
    scanner_kwargs = build_scanner_kwargs(adapter)
    return await BleakScanner.find_device_by_filter(build_find_filter(mac), **scanner_kwargs)

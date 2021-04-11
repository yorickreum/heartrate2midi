import asyncio
from bleak import BleakScanner


async def run():
    devices = await BleakScanner.discover()
    polar_devices = [d for d in devices if ("Polar OH1" in d.name)]
    oh1 = polar_devices[0]
    print(oh1)
    pass


loop = asyncio.get_event_loop()
loop.run_until_complete(run())

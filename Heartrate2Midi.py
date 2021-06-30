# Build with  pyinstaller -F Heartrate2Midi.py

import asyncio
import math

import rtmidi
from bleak import BleakClient, BleakError

# show console
# import pdb
# pdb.set_trace()

from utils import query_yes_no

# address = "A0:9E:1A:71:96:37" --> Where do I find this address?
# address = "31ac55d6-a113-46cf-9274-e09de1885289"  # yorick
# address = "3068ac7d-b56f-4b1f-ab66-f6d38963649d"  # sophie
address = "a471f15e-50e3-41bc-979f-bd8920066a54"  # sophie 2
model_uid = "00002a24-0000-1000-8000-00805f9b34fb"
battery_uid = "00002a19-0000-1000-8000-00805f9b34fb"
heartbeat_uid = "00002a37-0000-1000-8000-00805f9b34fb"

running = True

midiout = rtmidi.MidiOut()
midiout.open_virtual_port("Heartrate2MIDI")
print("\nCreated Midi port \"Heartrate2MIDI\" to output volume.")


def hr2midi(bpm):
    mu = 120
    sigma = 35
    s = .5
    ut = 170
    normalized_midi = \
        ((ut - s * mu) / ut) * math.exp(-((bpm - mu) / sigma) ** 2) + s * bpm / ut
    if bpm > mu:
        normalized_midi = math.exp(-((bpm - mu) / sigma) ** 2)
    return int(normalized_midi * 127)


async def run(midiout):
    try_again = True
    while try_again:
        print("Trying to connect to pulse sensor...")
        try:
            async with BleakClient(address) as client:
                model = await client.read_gatt_char(model_uid)
                model = model.decode("utf-8")

                battery = await client.read_gatt_char(battery_uid)
                battery = battery[0]

                print("Connected to pulse sensor: ", end="")
                print("Model: {:s}, battery state: {:d}% \n".format(model, battery))

                def callback(sender, data):
                    bpm = data[1]
                    print("\r\rCurrent heart rate: {:d} bpm".format(bpm), end="")
                    midi_val = hr2midi(bpm)
                    channel_volume_course = [176, 7, midi_val]
                    midiout.send_message(channel_volume_course)
                    print(", MIDI output value: {:d}".format(midi_val), end="")
                    print(" (approx volume: {:.2f} %).".format((midi_val / 127) * 100), end="")

                await client.start_notify(heartbeat_uid, callback)
                while client.is_connected and running:
                    try:
                        await asyncio.sleep(1)
                    except KeyboardInterrupt:
                        await client.disconnect()
                        del midiout
                        print('Program ended by interrupt, bye bye! :-)')
        except BleakError as e:
            print("Ooops, could not connect to the pulse sensor... This went wrong:")
            print(str(e))
            try_again = query_yes_no("Try again?")


asyncio.run(run(midiout))  # event based
# del midiout

# heartrate2midi

A Python script to output the heart rate determined by a Polar OH1 pulse sensor as a MIDI signal, for example to use in Ableton Live to control speed or volume.
Tested on macOS 10.15.7 with Python 3.8.

Uses https://github.com/hbldh/bleak for Bluetooth LE / GATT and https://pypi.org/project/python-rtmidi for MIDI.

## Inspired by references
https://www.socsci.ru.nl/wilberth/python/polar.html  
https://github.com/erikboto/polar-oh1
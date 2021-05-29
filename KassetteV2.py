import os
import soco
from evdev import InputDevice, categorize, ecodes


def play(nfc_number):
    print('start play "' + nfc_number + '"')
    try:
        sonos = {
            s for s in soco.discover() if s.player_name == os.environ["SPEAKER"]
        }.pop()
        playlist = next(
            p
            for p in sonos.music_library.get_music_library_information(
                "sonos_playlists"
            )
            if p.title.endswith(nfc_number)
        )
        sonos.unjoin()
        sonos.clear_queue()
        sonos.add_to_queue(playlist)
        sonos.play_from_queue(0)
    except StopIteration:
        print('found no Playlist for "' + nfc_number + '"')


scancodes = {
    2: u"1",
    3: u"2",
    4: u"3",
    5: u"4",
    6: u"5",
    7: u"6",
    8: u"7",
    9: u"8",
    10: u"9",
    11: u"0",
}


def main():
    accumluator = ""
    devicePath = "/dev/input/event0"
    dev = InputDevice(devicePath)
    dev.grab()

    print("Start listining on " + devicePath)
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            data = categorize(event)
            if data.keystate == 1:
                if data.scancode == 28:
                    play(accumluator)
                    accumluator = ""
                else:
                    accumluator += scancodes.get(data.scancode)


main()

"""A script to controll a sonos speaker with a NFC Card"""
import os
from datetime import datetime
from applicationinsights import TelemetryClient, exceptions
import soco
exceptions.enable(os.environ['APPLICATIONINSIGHTS'])

def main():
    """runs input loop of kassette V2"""
    telemetry_client = TelemetryClient(os.environ['APPLICATIONINSIGHTS'])
    telemetry_client.track_event("Startup")
    telemetry_client.flush()
    nfc_number = ''
    while nfc_number != 'exit':
        nfc_number = input('Ready for NFC input: ')
        if nfc_number != 'exit':
            try:
                start_time = datetime.utcnow()
                sonos = {s for s in soco.discover() if s.player_name == os.environ['SPEAKER']}.pop()
                playlist = next(p for p in
                                sonos.music_library.get_music_library_information('sonos_playlists')
                                if p.title.endswith(nfc_number))
                sonos.unjoin()
                sonos.clear_queue()
                sonos.add_to_queue(playlist)
                sonos.play()
                duration = (datetime.utcnow() - start_time).total_seconds() * 1000
                telemetry_client.track_request("Play", nfc_number, True, duration=duration,
                                               properties={'playList': playlist.title})
            except StopIteration:
                duration = (datetime.utcnow() - start_time).total_seconds() * 1000
                telemetry_client.track_request("Play", nfc_number, True,
                                               duration=duration, response_code=404)
                print('found no Playlist for "' + nfc_number + '"')
            except:
                duration = (datetime.utcnow() - start_time).total_seconds() * 1000
                telemetry_client.track_request("Play", nfc_number, False,
                                               duration=duration, response_code=500)
                raise
            finally:
                telemetry_client.flush()

main()

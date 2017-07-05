from applicationinsights import TelemetryClient, exceptions
import soco
import os
tc = TelemetryClient(os.environ['APPLICATIONINSIGHTS'])
exceptions.enable(os.environ['APPLICATIONINSIGHTS'])

tc.track_event("Startup")
tc.flush()
nfcNumber = ''
while (nfcNumber != 'exit'):
    nfcNumber = input('Ready for NFC input: ')
    if (nfcNumber != 'exit'):
        try:
            sonos = {s for s in soco.discover() if s.player_name == os.environ['SPEAKER']}.pop()
            playList = next(p for p in sonos.music_library.get_music_library_information('sonos_playlists') if p.title.endswith(nfcNumber))
            sonos.unjoin()
            sonos.clear_queue()
            sonos.add_to_queue(playList)
            sonos.play()
            tc.track_event("Play", {'nfcNumer': nfcNumber, 'playList': playList.title })
        except StopIteration:
            tc.track_event('found no Playlist', {'nfcNumer': nfcNumber})
            print('found no Playlist for "' + nfcNumber + '"')
        tc.flush()

from applicationinsights import TelemetryClient, exceptions
import soco
import os
from datetime import datetime
tc = TelemetryClient(os.environ['APPLICATIONINSIGHTS'])
exceptions.enable(os.environ['APPLICATIONINSIGHTS'])

tc.track_event("Startup")
tc.flush()
nfcNumber = ''
while (nfcNumber != 'exit'):
    nfcNumber = input('Ready for NFC input: ')
    if (nfcNumber != 'exit'):
        try:
            start_time = datetime.utcnow()
            sonos = {s for s in soco.discover() if s.player_name == os.environ['SPEAKER']}.pop()
            playList = next(p for p in sonos.music_library.get_music_library_information('sonos_playlists') if p.title.endswith(nfcNumber))
            sonos.unjoin()
            sonos.clear_queue()
            sonos.add_to_queue(playList)
            sonos.play()
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            tc.track_request("Play", nfcNumber, True, duration = duration, properties = { 'playList': playList.title })
        except StopIteration:
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            tc.track_request("Play", nfcNumber, True, duration = duration, response_code = 404)
            print('found no Playlist for "' + nfcNumber + '"')
        except:
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            tc.track_request("Play", nfcNumber, False, duration = duration, response_code = 500)
            raise
        finally:
            tc.flush()

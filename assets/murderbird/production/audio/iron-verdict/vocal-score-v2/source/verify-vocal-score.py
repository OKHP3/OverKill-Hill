"""Round-trip check of the exported score against MIDI and guide audio."""
from pathlib import Path
import json
import mido
import numpy as np
import soundfile as sf
from music21 import converter, stream, note

p=Path(__file__).resolve().parent.parent
score=converter.parse(p/'iron-verdict-vocal-score.musicxml')
measures=list(score.parts[0].getElementsByClass(stream.Measure))
assert [m.number for m in measures]==list(range(1,57))
assert all(m.duration.quarterLength==4 for m in measures)
notes=list(score.parts[0].stripTies().flatten().getElementsByClass(note.Note))
mf=mido.MidiFile(p/'iron-verdict-vocal-melody.mid')
assert abs(mf.length-224*60/104)<.001
mnotes=[]; active={}; ticks=0; lyric_count=0
for msg in mf.tracks[1]:
    ticks+=msg.time
    if msg.type=='lyrics': lyric_count+=1
    if msg.type=='note_on' and msg.velocity>0: active[msg.note]=ticks
    if msg.type=='note_off':
        start=active.pop(msg.note)
        mnotes.append((start/480,(ticks-start)/480,msg.note))
mnotes.sort()
assert len(notes)==len(mnotes)==lyric_count==279
for n,(on,duration,pitch) in zip(notes,mnotes):
    assert n.pitch.midi==pitch and abs(float(n.offset)-on)<1e-6
    assert abs(float(n.duration.quarterLength)-duration)<1e-6
wave,sr=sf.read(p/'iron-verdict-vocal-pitch-guide.wav')
errors=[]
for n in notes:
    start=int(float(n.offset)*60/104*sr)
    duration=int(float(n.duration.quarterLength)*60/104*sr)
    a=wave[start+min(1000,duration//5):start+duration-min(1500,duration//5)]
    spectrum=np.abs(np.fft.rfft(a*np.hanning(len(a)),n=131072))
    hz=np.argmax(spectrum)*sr/131072
    expected=440*2**((n.pitch.midi-69)/12)
    errors.append(abs(hz-expected))
assert max(errors)<2
report=json.loads((p/'validation.json').read_text())
report['independent_roundtrip_checks']={
    'measure_sequence':'1 through 56 in order',
    'measures_total_four_beats':56,
    'score_midi_matching_notes':len(notes),
    'midi_lyric_events':lyric_count,
    'midi_duration_seconds':mf.length,
    'audio_note_pitch_max_error_hz':max(errors)
}
(p/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report['independent_roundtrip_checks'],indent=2))

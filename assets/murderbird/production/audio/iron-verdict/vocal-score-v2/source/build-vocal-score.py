"""Original vocal setting for the existing 56-bar Iron Verdict instrumental.

Run from this directory with the repository's .local/vocal-score-env Python.
Engraving tools are isolated production tools, not website dependencies.
"""
from pathlib import Path
import base64, copy, io, json, re, subprocess, hashlib
import numpy as np
import soundfile as sf
import mido
import verovio
from music21 import stream, note, meter, key, clef, tempo, metadata, expressions, dynamics, layout, bar, harmony, tie
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as PdfTTFont
from fontTools.ttLib import TTFont as FontTTFont
from lxml import etree
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from svglib.svglib import svg2rlg

OUT = Path(__file__).resolve().parent.parent
BASE = OUT.parent
REPO = BASE.parents[4]
WORK = REPO / '.local/vocal-score-v2'
WORK.mkdir(parents=True, exist_ok=True)
BPM, BEATS, SR = 104, 224, 44100
SPB = 60 / BPM
bars = {}
lines = {}
def add(number, text, pitches, durations):
    tokens = []
    for word in text.split():
        syls = word.split('-')
        for i, syl in enumerate(syls):
            typ = 'single' if len(syls) == 1 else 'begin' if i == 0 else 'end' if i == len(syls)-1 else 'middle'
            tokens.append((syl, typ))
    assert len(tokens) == len(pitches) == len(durations), (number, tokens, pitches)
    assert sum(durations) <= 4, (number, durations)
    rows = [dict(pitch=p, duration=d, syllable=s, syllabic=t) for p,d,(s,t) in zip(pitches,durations,tokens)]
    if sum(durations) < 4: rows.append(dict(pitch=None, duration=4-sum(durations)))
    bars[number] = rows
    lines[number] = text.replace('-', '').replace('woundup', 'wound-up')

for i in range(1,5): bars[i] = [dict(pitch=None, duration=4)]
for b,text,ps in [(5,'No crown.',['D3','A3']), (6,'No cage.',['D3','G3']), (7,'Just weight.',['F3','A3']), (8,'Just truth.',['F3','D3'])]:
    add(b,text,ps,[1,2])

verse1 = [
    'Sev-en win-ters shaped this skin,',
    'Ham-mer marks are writ-ten in.',
    'Wings no king could teach to rise,',
    'Hea-vy feet and watch-ful eyes.',
    'Wa-ter dark-ened ev-ery seam,',
    'Names went qui-et in the green.',
    'They could weigh me, name their price,',
    'Not the will be-hind these eyes.'
]
verse2 = [
    'I-ron braced the bro-ken frame,',
    'Brass and bor-rowed pow-er came.',
    'Ev-ery step a wound-up spring,',
    'No one there to choose a thing.',
    'Now a heart-beat runs with me.',
    'Now the choice be-longs to me.',
    'Leave the old scar where it stays.',
    'I can learn an-oth-er way.'
]
vpatterns = [
    ['D3','D3','F3','F3','G3','F3','A3'],
    ['F3','F3','G3','F3','E3','F3','D3'],
    ['D3','F3','A3','A3','G3','F3','A3'],
    ['G3','G3','F3','E3','F3','E3','D3'],
]
for j,txt in enumerate(verse1): add(9+j,txt,vpatterns[j%4],[.5]*7)
for j,txt in enumerate(verse2):
    p = vpatterns[j%4].copy()
    if j in (0,2,4,6): p[-1] = 'C4' if j in (2,6) else 'A3'
    add(17+j,txt,p,[.5]*7)

chorus = [
    ('Put your prom-ise un-der load.', ['D4','D4','F4','E4','D4','E4','F4'], [.5]*6+[1]),
    ("Don't look a-way.", ['E4','D4','C4','D4'], [.5,.5,1,1.5]),
    ('Let the hid-den frac-ture show', ['B-3','B-3','D4','C4','D4','E4','F4'], [.5]*6+[1]),
    ('Be-fore we fall.', ['D4','F4','D4','B-3'], [.5,.5,1,1.5]),
    ('I will stand be-side the hands', ['C4','C4','E4','D4','E4','D4','G4'], [.5]*6+[1]),
    ('That build it strong.', ['E4','G4','E4','C4'], [.5,.5,1,1.5]),
    ("I will find what does-n't hold.", ['D4','D4','F4','E4','D4','E4','F4'], [.5]*6+[1]),
    ('We car-ry on.', ['E4','D4','C4','D4'], [.5,.5,1,1.5]),
]
# F4 is the ceiling: the chorus opens up without requiring a high rock tenor.
chorus = [(t, ['F4' if p=='G4' else p for p in ps],ds) for t,ps,ds in chorus]
# On C harmony, use its fifth rather than the suspended fourth as a long target.
chorus[4] = (chorus[4][0], ['C4','C4','E4','D4','E4','D4','E4'], chorus[4][2])
chorus[5] = (chorus[5][0], ['E4','E4','D4','C4'], chorus[5][2])
for start in [25,41]:
    for j,(txt,p,d) in enumerate(chorus): add(start+j,txt,p,d)

bridge = [
    ('Some scars stay.', ['D3','F3','A3'], [.5,.5,2.5]),
    ('Some seams give way.', ['D3','F3','G3','A3'], [.5,.5,1,1.5]),
    ('Leave the ham-mer marks.', ['F3','F3','G3','F3','A3'], [.5,.5,.5,.5,1.5]),
    ("They don't make me weak.", ['A3','G3','F3','E3','D3'], [.5,.5,.5,.5,1.5]),
    ('Be-fore the or-der', ['D3','F3','A3','G3','F3'], [.5,1,.5,.5,1]),
    ("Leaves your mouth, I've seen", ['G3','F3','A3','G3','A3'], [.5,.5,1,.5,1]),
    ('Where the brace gives way.', ['A3','A3','C4','A3','F3'], [.5,.5,1,.5,1]),
    ('I shift be-fore I fall.', ['F3','A3','A3','C4','A3','D4'], [.5,.5,.5,.5,.5,1]),
]
for j,(txt,p,d) in enumerate(bridge): add(33+j,txt,p,d)
outro = ["Close the file. I'll bring you back.", 'One more fault be-neath the patch.', 'Leave no weak-ness dressed as done.', 'We stay here till it can run.']
for j,txt in enumerate(outro): add(49+j,txt,vpatterns[j],[.5]*7)
add(53,"Find what does-n't hold.",['D4','C4','A3','C4','D4'],[1,.5,.5,.5,1.5])
bars[53][-1]['tie']='start'
bars[54]=[dict(pitch='D4',duration=3,tie='stop'),dict(pitch=None,duration=1)]
for b in [55,56]: bars[b]=[dict(pitch=None,duration=4)]
assert sorted(bars)==list(range(1,57))
assert all(sum(n['duration'] for n in b)==4 for b in bars.values())

sections = {
    1: ('A  IGNITION', 'Instrumental. Count four full bars.', 'mp'),
    5: ('B  THE BIRD', 'Low, deliberate; sing on pitch.', 'mp'),
    9: ('C  WHAT THE WATER KEPT', 'Tight rhythmic delivery; no rush.', 'mf'),
    17: ('D  THE REBUILD', 'Build intensity, keep words clear.', 'mf'),
    25: ('E  UNDER LOAD', 'Open and firm; sustain final vowels.', 'f'),
    33: ('F  JUDGMENT', 'Pull close; feel the half-time drums.', 'mp'),
    41: ('G  IRON VERDICT', 'Full voice. Same melody, greater conviction.', 'f'),
    49: ('H  THE UNFINISHED FILE', 'Direct, rhythmic; back toward the low register.', 'mf'),
    53: ('I  FINAL WORD', 'Hold vowel; close the d at the notated release.', 'f'),
    55: ('J  FINAL HIT', 'Vocal tacet. Let the band finish.', None),
}
score=stream.Score(id='iron-verdict-vocal')
score.metadata=metadata.Metadata()
score.metadata.title='MURDERBIRD: IRON VERDICT'
score.metadata.composer='Original vocal setting | rehearsal edition v2'
part=stream.Part(id='lead-vocal'); part.partName='Lead voice'; part.partAbbreviation='V.'
events=[]
for b,rows in sorted(bars.items()):
    m=stream.Measure(number=b)
    if b==1:
        m.insert(0,clef.Treble8vbClef()); m.insert(0,key.Key('d','minor')); m.insert(0,meter.TimeSignature('4/4'))
        m.insert(0,tempo.MetronomeMark(number=BPM))
    if b in [17,33,49]: m.insert(0,layout.PageLayout(isNew=True))
    elif b%2==1: m.insert(0,layout.SystemLayout(isNew=True))
    if b in sections:
        label,detail,dyn=sections[b]
        rm=expressions.RehearsalMark(label)
        rm.style.alignHorizontal='left'
        m.insert(0,rm)
        # Detailed delivery instructions live in the performance sheet, keeping staves clear.
        if dyn: m.insert(0,dynamics.Dynamic(dyn))
    if b in [1,5,9,17,25,27,29,31,33,41,43,45,47,49,53]:
        symbol='B-' if b in [27,43] else 'C' if b in [29,45] else 'Dm'
        m.insert(0,harmony.ChordSymbol(symbol))
    off=0
    for row in rows:
        n=note.Rest(quarterLength=row['duration']) if row['pitch'] is None else note.Note(row['pitch'],quarterLength=row['duration'])
        if row.get('syllable'):
            ly=note.Lyric(text=row['syllable'],number=1,syllabic=row['syllabic']); n.lyrics=[ly]
        if row.get('tie'): n.tie=tie.Tie(row['tie'])
        m.append(n)
        if row['pitch']:
            events.append(dict(bar=b,start=(b-1)*4+off,duration=row['duration'],midi=n.pitch.midi,**{k:v for k,v in row.items() if k not in ['duration']}))
        off+=row['duration']
    m.makeBeams(inPlace=True)
    if b==56: m.rightBarline=bar.Barline('final')
    part.append(m)
score.insert(0,part)
xml=OUT/'iron-verdict-vocal-score.musicxml'
score.write('musicxml',fp=xml)
(OUT/'source/vocal-events.json').write_text(json.dumps(dict(bpm=BPM,bars=56,events=events,sections=sections),indent=2)+'\n')

# Engrave the MusicXML, preserving explicit two-bar systems and page breaks.
v=verovio.toolkit()
v.setOptions(dict(pageWidth=2100,pageHeight=2970,pageMarginTop=90,pageMarginBottom=80,pageMarginLeft=75,pageMarginRight=75,
                 scale=40,breaks='encoded',header='none',footer='none',lyricSize=5.2,lyricWordSpace=2.2,spacingSystem=9,adjustPageHeight=False))
assert v.loadFile(str(xml))
c=canvas.Canvas(str(OUT/'iron-verdict-vocal-score.pdf'),pagesize=letter)
c.setTitle('MurderBird: Iron Verdict | Vocal score v2')
pages=v.getPageCount()
for pg in range(1,pages+1):
    svg=v.renderToSVG(pg)
    # SVG-to-PDF text runs do not preserve mixed SMuFL font spacing reliably.
    # The tempo is already explicit in the page header; chord text uses ASCII Bb.
    root=etree.fromstring(svg.encode())
    ns={'s':'http://www.w3.org/2000/svg'}
    for g in root.xpath('.//s:g[@class="tempo"]',namespaces=ns):
        g.getparent().remove(g)
    for g in root.xpath('.//s:g[@class="harm"]',namespaces=ns):
        tx=g.find('s:text',ns)
        if tx is not None:
            raw=''.join(tx.itertext()).strip()
            for child in list(tx): tx.remove(child)
            tx.text='Bb' if 'B' in raw else 'Dm' if 'Dm' in raw else 'C'
            tx.set('font-family','Times')
            tx.set('font-size','405px')
    svg=etree.tostring(root,encoding='unicode')
    (WORK/f'score-{pg}.svg').write_text(svg)
    if pg==1:
        encoded=re.search(r'base64,([^)]*)',svg).group(1)
        font=FontTTFont(io.BytesIO(base64.b64decode(encoded)))
        font.flavor=None
        font.save(str(WORK/'leipzig.ttf'))
        pdfmetrics.registerFont(PdfTTFont('Leipzig',str(WORK/'leipzig.ttf')))
    drawing=svg2rlg(io.BytesIO(svg.encode()))
    x0,y0,x1,y1=drawing.getBounds()
    factor=min(540/(x1-x0),650/(y1-y0))
    c.saveState()
    c.translate(36,727)
    c.scale(factor,factor)
    c.translate(-x0,-y1)
    renderPDF.draw(drawing,c,0,0)
    c.restoreState()
    c.setFont('Helvetica-Bold',13); c.drawString(36,765,'MURDERBIRD: IRON VERDICT')
    c.setFont('Helvetica',9); c.drawRightString(576,765,f'Lead vocal | v2 | {pg}/{pages}')
    c.setFont('Helvetica',9); c.drawString(36,748,'104 BPM | 4/4 | D minor | sounding D3-F4 | treble clef sounds one octave lower')
    if pg==pages:
        y=727-(y1-y0)*factor-32
        c.setFont('Helvetica-Bold',11);c.drawString(36,y,'PERFORMANCE NOTES');y-=20
        style=ParagraphStyle('directions',fontName='Helvetica',fontSize=10,leading=14)
        for txt in [
            '<b>Entry and ending.</b> Audio starts at bar 1, with no extra count-in. Sing "No" at bar 5 (0:09.23). Release the final "hold" at bar 54, beat 4 (2:04.04). Stay silent for the band hit at bar 55 (2:04.62).',
            '<b>Voice.</b> Keep verses grounded and clear, open the chorus, and bring the bridge close. Roughness is optional; the notes and words carry the force. This key is a starting setting, not a requirement to strain for the top notes.',
            '<b>Breathing and holds.</b> Breathe in the written rests. Sustain the vowel on long notes and close its final consonant at release. The tie on "hold" joins both notes into one syllable. Both choruses are written out; no repeats or extensions.',
            '<b>Rehearsal files.</b> The pitch guide plays this melody with a synthesized tone. The rehearsal mix adds the existing backing stems with their lead synth reduced. Neither file is a sung performance. MIDI and MusicXML are included for editing or a separate vocal-synthesis pass.',
            '<b>Timing.</b> 233 performed words; 1:42 of notated vocal sound across a 2:10 arrangement. The remaining time is written rests and instrumental space. This setting has not yet been auditioned by a vocalist.'
        ]:
            para=Paragraph(txt,style);_,h=para.wrap(540,300);para.drawOn(c,36,y-h);y-=h+10
        assert y>50, y
    c.setFont('Helvetica',8); c.drawString(36,29,'Straight through, no repeats. Breathe in written rests. Audio begins at bar 1, with no added count-in.')
    c.drawRightString(576,17,'2026-09-20 | Original melody and lyrics')
    c.showPage()
c.save()

# MIDI: absolute 480-PPQ schedule, syllable meta-events, section markers, full duration.
# Join the only tied syllable across bars 53 and 54 into one sounding note.
joined=[]
for e in events:
    if e.get('tie')=='stop':
        assert joined[-1]['midi']==e['midi'] and joined[-1]['start']+joined[-1]['duration']==e['start']
        joined[-1]['duration']+=e['duration']
    else: joined.append(copy.deepcopy(e))
mid=mido.MidiFile(ticks_per_beat=480)
con=mido.MidiTrack();mid.tracks.append(con)
con.append(mido.MetaMessage('set_tempo',tempo=mido.bpm2tempo(BPM)))
con.append(mido.MetaMessage('time_signature',numerator=4,denominator=4))
con.append(mido.MetaMessage('key_signature',key='Dm'))
last=0
for b,(name,_,__) in sections.items():
    tick=(b-1)*4*480
    con.append(mido.MetaMessage('marker',text=name,time=tick-last));last=tick
con.append(mido.MetaMessage('end_of_track',time=BEATS*480-last))
tr=mido.MidiTrack();mid.tracks.append(tr)
tr.append(mido.MetaMessage('track_name',name='Original vocal melody with lyric syllables'))
tr.append(mido.Message('program_change',program=53))
schedule=[]
for e in joined:
    a=round(e['start']*480);z=round((e['start']+e['duration'])*480)
    # Short articulation between repeated syllables, while preserving the score's note values.
    if e.get('syllable'): schedule.append((a,1,mido.MetaMessage('lyrics',text=e['syllable'])))
    schedule.append((a,2,mido.Message('note_on',note=e['midi'],velocity=95 if 25<=e['bar']<=32 or 41<=e['bar']<=48 else 80)))
    schedule.append((z,0,mido.Message('note_off',note=e['midi'],velocity=0)))
last=0
for t,_,msg in sorted(schedule,key=lambda x:(x[0],x[1])):
    msg.time=t-last;tr.append(msg);last=t
tr.append(mido.MetaMessage('end_of_track',time=BEATS*480-last))
mid.save(OUT/'iron-verdict-vocal-melody.mid')

# Audible pitch/rhythm guide. This is an original synthesized tone, not a sung vocal.
master,rate=sf.read(BASE/'murderbird-iron-verdict.wav',dtype='float32',always_2d=True)
assert rate==SR
length=len(master)
tone=np.zeros(length,dtype=np.float32)
for e in joined:
    start=round(e['start']*SPB*SR)
    count=round(e['duration']*SPB*SR)
    t=np.arange(count)/SR
    hz=440*2**((e['midi']-69)/12)
    # Rounded reed tone with restrained upper partials.
    wave=np.sin(2*np.pi*hz*t)+.25*np.sin(2*np.pi*hz*2*t)+.10*np.sin(2*np.pi*hz*3*t)
    attack=np.minimum(1,t/.012)
    release=np.minimum(1,np.maximum(0,(t[-1]-t)/.045))
    wave=(wave*attack*release*.18).astype(np.float32)
    tone[start:start+count]+=wave[:len(tone[start:start+count])]
sf.write(OUT/'iron-verdict-vocal-pitch-guide.wav',tone,SR,subtype='PCM_24')
backing=np.zeros_like(master)
for f in (BASE/'stems').glob('*.wav'):
    a,r=sf.read(f,dtype='float32',always_2d=True)
    assert r==SR and a.shape==master.shape, (f,a.shape,master.shape)
    backing+=a*(.10 if f.stem=='lead' else 1)
backing*=.40/max(np.max(np.abs(backing)),1e-9)
mix=backing+tone[:,None]
assert np.max(np.abs(mix))<1
sf.write(OUT/'iron-verdict-vocal-rehearsal-mix.wav',mix,SR,subtype='PCM_24')
for stem in ['iron-verdict-vocal-pitch-guide','iron-verdict-vocal-rehearsal-mix']:
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(OUT/(stem+'.wav')),'-codec:a','libmp3lame','-b:a','192k',str(OUT/(stem+'.mp3'))],check=True)

word_count=sum(len(s.split()) for s in lines.values())
syllables=sum(bool(e.get('syllable')) for e in events)
sounding=sum(e['duration'] for e in joined)*SPB
report=dict(bpm=BPM,bars=56,beats=BEATS,score_duration_seconds=BEATS*SPB,audio_duration_seconds=length/SR,
            vocal_first_entry_seconds=16*SPB,vocal_final_release_seconds=215*SPB,
            notated_vocal_duration_excluding_rests_seconds=sounding,performed_word_count=word_count,lyric_syllables=syllables,
            range='D3-F4',midi_min=min(e['midi'] for e in events),midi_max=max(e['midi'] for e in events),
            pdf_pages=pages,guide_peak=float(np.max(np.abs(tone))),mix_peak=float(np.max(np.abs(mix))),
            checks=['All 56 bars total exactly four beats.','Each printed syllable has a note.','Tied final syllable becomes one MIDI/audio event.','All stems have matching sample rate and length.','No sample clipping in either new WAV.'],
            limitations=['Pitch guide is synthesized, not sung.','No human vocalist audition or musical listening assessment has been performed.','Existing instrumental and GarageBand project were not edited.'])
(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')

md=['# MurderBird: Iron Verdict', '', 'Vocal performance edition v2 | 104 BPM | 4/4 | D minor | 56 bars | 2:09.23 plus audio tail', '',
    '## Performance directions', '',
    'Sing the written melody at sounding D3-F4. The small 8 beneath the treble clef means sound one octave below ordinary treble notation. Read straight through; both choruses are written out. No repeats or improvised extensions are required.', '',
    'Use a grounded, intelligible delivery in the verses, open vowels in the chorus, and a close, deliberate bridge. Vocal roughness is optional. Breathe in the written rests. Do not breathe between a hyphenated word or within the tied final hold. Sustain the vowel and place the final consonant at the release.', '',
    'The audio starts at instrumental bar 1 without an added count-in. First vocal: bar 5 at 0:09.23. Final vocal release: bar 54, beat 4, at 2:04.04. Remain silent for the final band hit at bar 55 (2:04.62).', '',
    f'This performance contains {word_count} words and {syllables} lyric syllables. Notated sounding vocal time is {sounding:.2f} seconds; the rest is intentional breathing and instrumental space. The entire song lasts {BEATS*SPB:.2f} seconds before its audio tail.', '',
    '## Complete performed lyric', '']
for b in range(1,57):
    if b in sections:
        name,detail,_=sections[b]
        sec=(b-1)*4*SPB
        md.extend(['',f'### {name} | bar {b} | {int(sec//60)}:{sec%60:05.2f}', '',detail,''])
    if b in lines: md.append(f'{b:02d}. {lines[b]}  ')
    elif b==54: md.append('54. Continue the tied vowel in "hold" for three beats; release and breathe on beat 4.  ')
    elif b in [1,55]: md.append('[Instrumental; no vocal.]  ')
md.extend(['','## Files and production handoff','',
    '- `iron-verdict-vocal-score.pdf`: printable staff notation with syllable underlay, rhythms, rests, chord cues, rehearsal marks and dynamics.',
    '- `iron-verdict-vocal-score.musicxml`: editable score, including lyrics and tempo.',
    '- `iron-verdict-vocal-melody.mid`: sounding pitches, exact rhythm and lyric meta-events. Some DAWs ignore MIDI lyric events; use MusicXML and this sheet as the authoritative underlay.',
    '- `iron-verdict-vocal-rehearsal-mix.mp3`: guide melody over a reduced backing mix; the existing lead synth is quieter to make the new vocal line easier to follow.',
    '- `iron-verdict-vocal-pitch-guide.wav` and `.mp3`: isolated synthesized melody. These are pitch/rhythm guides, not a human or synthesized singing performance.',
    '- `validation.json`: timing, range, note/lyric counts and audio checks.', '',
    'The original instrumental and GarageBand project remain intact. These guides are derived from the existing custom-rendered stems; they are not renders of the GarageBand project. All guides align to bar 1 of the original 104 BPM arrangement. No reference-song recordings were sampled.', '',
    'The story is the basis for the new lyric: https://overkillhill.com/writings/murderbird/ . Ancient history is described as evidence carried by the body, not recovered ancestral memory. The restrained wings, repair history, self-directed judgment and refusal to abandon unfinished work anchor the character.', '',
    'This is a fully specified rehearsal setting. It has not yet been auditioned by a vocalist; breath, key and phrasing may still be refined through an actual performance. The guide tone demonstrates the notes and timing, not final vocal timbre.', '',
    'Engraving: Music21 MusicXML and Verovio (https://book.verovio.org/). Isolated build environment: repository `.local/vocal-score-env`. Rebuild with `source/build-vocal-score.py`. No website package dependencies or public-page registration were changed.',''])
(OUT/'performance-sheet.md').write_text('\n'.join(md))
print(json.dumps(report,indent=2))

"""Compose/render original MurderBird demo. No external samples or source songs."""
from pathlib import Path
import json, math, hashlib
import numpy as np
from scipy.signal import butter, sosfilt
import soundfile as sf
import mido
from composition import generate_events
from instruments import render_note

OUT=Path(__file__).resolve().parent.parent/'rebuild'
OUT.mkdir(parents=True,exist_ok=True)
STEMS=OUT/'stems'; STEMS.mkdir(exist_ok=True)
SR=44100
score=generate_events()
SPB=60/score['bpm']; BAR=4*SPB
END=score['bars']*BAR+.6
N=math.ceil(END*SR)
rng=np.random.default_rng(9172026)

def filt(x,freq,kind='lowpass',order=2):
    return sosfilt(butter(order,freq,btype=kind,fs=SR,output='sos'),x)

def envelope(n,attack=.002,release=.018):
    e=np.ones(n)
    a=min(n,round(attack*SR)); r=min(n-a,round(release*SR))
    if a:e[:a]=np.linspace(0,1,a)**.75
    if r:e[-r:]*=np.linspace(1,0,r)**1.5
    return e

def drum(kind,vel,seed):
    rr=np.random.default_rng(seed)
    dur={'kick':.55,'snare':.38,'hat':.105,'openhat':.48,'crash':2.3,'tom':.5,'metal':1.6}[kind]
    t=np.arange(round(dur*SR))/SR; noise=rr.normal(0,1,len(t))
    if kind=='kick':
        f=49+100*np.exp(-t*48)
        body=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)
        click=filt(noise,1800,'highpass')*np.exp(-t*180)*.13
        x=np.tanh(1.8*(body+click))*.85
    elif kind=='snare':
        body=(np.sin(2*np.pi*185*t)*np.exp(-t*19)+.42*np.sin(2*np.pi*330*t)*np.exp(-t*26))*.5
        snap=filt(filt(noise,1250,'highpass'),8500)*np.exp(-t*20)*.58
        x=np.tanh(1.35*(body+snap))*.78
    elif kind in ('hat','openhat','crash'):
        lo=6500 if kind=='hat' else 4300
        hiss=filt(filt(noise,lo,'highpass'),13500)
        metallic=sum(np.sin(2*np.pi*f*t+rr.uniform(0,6)) for f in [4321,5763,6911,8837,10471])/6
        decay={'hat':55,'openhat':10,'crash':2.3}[kind]
        x=(.66*hiss+.1*metallic)*np.exp(-t*decay)
        if kind=='crash':x+=filt(noise,2900,'highpass')*.17*np.exp(-t*4)
    elif kind=='tom':
        f=110+65*np.exp(-t*30)
        x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*10)*.8+filt(noise,900)*np.exp(-t*80)*.2
    else:
        freqs=[211,497,823,1267,1943]
        x=sum((.44/(i+1))*np.sin(2*np.pi*f*t+rr.uniform(0,.1))*np.exp(-t*(2+i*.8)) for i,f in enumerate(freqs))
        x+=filt(noise,2500,'highpass')*.18*np.exp(-t*140)
    return (x*envelope(len(t),.0006,.015)*vel).astype(np.float32)

def place(buf,x,start,pan=0,gain=1):
    offset=round(start*SR)
    if offset<0:x=x[-offset:];offset=0
    length=min(len(x),len(buf)-offset)
    if length<=0:return
    angle=(pan+1)*np.pi/4
    buf[offset:offset+length,0]+=x[:length]*gain*np.cos(angle)
    buf[offset:offset+length,1]+=x[:length]*gain*np.sin(angle)

drum_events=[]
def hit(bar,beat,kind,velocity,pan=0):
    drum_events.append(dict(track='drums',start=bar*4+beat,duration=.15,note={'kick':36,'snare':38,'hat':42,'openhat':46,'crash':49,'tom':45,'metal':56}[kind],velocity=velocity,kind=kind,pan=pan))

for bar in range(56):
    if bar<4:
        if bar in (0,2):hit(bar,0,'metal',.34)
        continue
    if bar<8:
        for beat in [0,1.5,3]:hit(bar,beat,'kick',.62)
        if bar>=6:
            for beat in np.arange(0,4,.5):hit(bar,float(beat),'hat',.26,-.2)
        if bar==7:
            for b in [2.5,3,3.25]:hit(bar,b,'tom',.5,.1)
        continue
    if bar>=54:
        if bar==54:
            hit(bar,0,'kick',.95);hit(bar,0,'snare',.66);hit(bar,0,'crash',.65,.25)
        continue
    half=32<=bar<40
    big=24<=bar<32 or 40<=bar<48
    ending=bar>=52
    kick_beats=([0,1.5,3.25] if bar%2==0 else [0,.5,2.5,3.5])
    if half:kick_beats=[0,1.5] if bar<36 else [0,1.5,3.5]
    if ending:kick_beats=[0,2] if bar==52 else [0,1.5]
    for b in kick_beats:hit(bar,b,'kick',float(.82+rng.uniform(-.05,.05)))
    for b in ([2] if half else [1,3]):
        if ending and b>2:continue
        hit(bar,b,'snare',float(.76+rng.uniform(-.045,.045)))
    step=1 if half or ending else .5
    for j,b in enumerate(np.arange(0,4,step)):
        if bar in [15,23,31,39,47,51,53] and b>=3.5:continue
        vv=(.25 if j%2 else .39)*(1.12 if big else 1)
        if half:vv*=.7
        hit(bar,float(b+rng.uniform(-.004,.004)),'hat',float(vv),-.23)
    if bar in [8,16,24,40,48]:hit(bar,0,'crash',.60 if big else .48,.3)
    if big and bar%2:hit(bar,3.5,'openhat',.34,-.2)
    if bar in [15,23,31,47,51]:
        for b,v,p in [(3.25,.60,-.2),(3.5,.7,.1),(3.75,.78,.35)]:hit(bar,b,'tom',v,p)
    if bar in [37,38]:
        for b in [1,3]:hit(bar,b,'tom',.42+(bar-37)*.14,.2)
    if bar==39:
        for b in [0,1,2,2.5,3]:hit(bar,b,'tom',.50+b*.06,0)

mix=np.zeros((N,2),np.float32)
track_specs={'guitar_left':(-.8,.38),'guitar_right':(.8,.38),'bass':(0,.45),'lead':(-.06,.28),'pad':(.0,.15)}
levels={}
for track,(pan,gain) in track_specs.items():
    stem=np.zeros((N,2),np.float32)
    for i,e in enumerate(score['events']):
        if e['track']!=track:continue
        x=render_note(track,int(e['note']),float(e['duration'])*SPB,float(e['velocity']),SR,1337+i)
        place(stem,x,float(e['start'])*SPB,pan,gain)
    # Short fixed taps create space without obscuring the low rhythm section.
    if track in ('lead','pad'):
        source=stem.copy()
        for delay,amount in [(SPB*.75,.14),(SPB*1.5,.075)]:
            k=round(delay*SR)
            stem[k:]+=source[:-k,::-1]*amount
    tail=min(round(SR*1.5),len(stem));stem[-tail:]*=np.linspace(1,0,tail,dtype=np.float32)[:,None]
    levels[track]={'peak':float(abs(stem).max()),'rms':float(np.sqrt(np.mean(stem**2)))}
    sf.write(STEMS/(track.replace('_','-')+'.wav'),stem,SR,subtype='PCM_24')
    mix+=stem
    print('Rendered',track,flush=True)

stem=np.zeros((N,2),np.float32)
for i,e in enumerate(drum_events):
    x=drum(e['kind'],e['velocity'],3000+i)
    place(stem,x,e['start']*SPB,e['pan'],.68)
# Brief room reflections on drums.
source=stem.copy()
for delay,amount in [(.031,.06),(.061,.04),(.113,.025)]:
    k=round(delay*SR);stem[k:]+=source[:-k,::-1]*amount
stem=np.tanh(stem*1.5)/1.5
levels['drums']={'peak':float(abs(stem).max()),'rms':float(np.sqrt(np.mean(stem**2)))}
sf.write(STEMS/'drums.wav',stem,SR,subtype='PCM_24');mix+=stem

fx=np.zeros((N,2),np.float32)
for bar in [0,2,4,32,34,54]:
    place(fx,drum('metal',.8,bar+100),(bar*4)*SPB,.2 if bar%4 else -.2,.23)
# Original resonant optic tone, with pitch rise and air; no animal or recording samples.
for bar,dur,gain in [(1.5,2.0,.045),(6,2*BAR,.06),(37,3*BAR-.28,.065)]:
    count=round(dur*SR);t=np.arange(count)/SR
    f=220+440*(t/dur)**2
    tone=(np.sin(2*np.pi*np.cumsum(f)/SR)+.32*np.sin(2*np.pi*997*t))*.5
    noise=filt(rng.normal(0,1,count),1800,'highpass')*.3
    shape=np.sin(np.linspace(0,np.pi/2,count))**2*envelope(count,.1,.10)
    place(fx,(tone+noise)*shape,bar*BAR,.15,gain)
sf.write(STEMS/'mechanical-fx.wav',fx,SR,subtype='PCM_24');mix+=fx

# Guarantee clean transitions at the initial frame and final decay.
mix[:400]*=np.linspace(0,1,400)[:,None]
mix[-SR:]*=np.linspace(1,0,SR)[:,None]
peak=float(np.max(np.abs(mix)))
gain=min(1,.82/max(peak,1e-9))
mix*=gain
sf.write(OUT/'iron-verdict-premaster.wav',mix,SR,subtype='PCM_24')
# Delivered stems reproduce the premaster at unity, including fades/headroom.
for stem_path in STEMS.glob('*.wav'):
    stem,rate=sf.read(stem_path,dtype='float32',always_2d=True)
    stem[:400]*=np.linspace(0,1,400)[:,None]
    stem[-SR:]*=np.linspace(1,0,SR)[:,None]
    stem*=gain
    sf.write(stem_path,stem,rate,subtype='PCM_24')

# Standard MIDI type 1: editable performance, section markers and instrument cues.
mf=mido.MidiFile(type=1,ticks_per_beat=480)
meta=mido.MidiTrack();mf.tracks.append(meta)
meta.append(mido.MetaMessage('track_name',name='MurderBird - Iron Verdict',time=0))
meta.append(mido.MetaMessage('set_tempo',tempo=mido.bpm2tempo(score['bpm']),time=0))
meta.append(mido.MetaMessage('time_signature',numerator=4,denominator=4,time=0))
markers=[]
for s in score['sections']:markers.append((round(s['start_bar']*4*480),s['name']))
last=0
for tick,name in sorted(markers):meta.append(mido.MetaMessage('marker',text=name,time=tick-last));last=tick
meta.append(mido.MetaMessage('end_of_track',time=max(0,56*4*480-last)))
programs={'guitar_left':30,'guitar_right':30,'bass':34,'lead':81,'pad':89,'drums':0}
for ch,(track,program) in enumerate(programs.items()):
    channel=9 if track=='drums' else ch
    mt=mido.MidiTrack();mf.tracks.append(mt)
    mt.append(mido.MetaMessage('track_name',name=track.replace('_',' ').title(),time=0))
    if track!='drums':mt.append(mido.Message('program_change',channel=channel,program=program,time=0))
    mt.append(mido.Message('control_change',channel=channel,control=10,value=25 if track=='guitar_left' else 102 if track=='guitar_right' else 64,time=0))
    events=[]
    source=drum_events if track=='drums' else [e for e in score['events'] if e['track']==track]
    source=sorted(source,key=lambda e:(e['start'],e['note']))
    for event_index,e in enumerate(source):
        on=max(0,round(float(e['start'])*480));off=on+max(1,round(float(e['duration'])*480))
        # Avoid a previous same-note NoteOff cutting off a later re-articulation.
        next_same=next((other for other in source[event_index+1:] if other['note']==e['note']),None)
        if next_same is not None:
            next_tick=round(float(next_same['start'])*480)
            if next_tick>on:off=min(off,next_tick)
        events.append((on,1,int(e['note']),max(1,min(127,round(float(e['velocity'])*110)))))
        events.append((off,0,int(e['note']),0))
    last=0
    for tick,on,pitch,velocity in sorted(events):
        mt.append(mido.Message('note_on' if on else 'note_off',channel=channel,note=pitch,velocity=velocity,time=tick-last));last=tick
    mt.append(mido.Message('control_change',channel=channel,control=123,value=0,time=1))
mf.save(OUT/'iron-verdict-editable.mid')
score['drum_events']=drum_events
(OUT/'composition-and-arrangement.json').write_text(json.dumps(score,indent=2))
metrics={'bpm':score['bpm'],'bars':score['bars'],'duration_seconds':N/SR,'sample_rate':SR,'premaster_peak':float(abs(mix).max()),'premaster_rms':float(np.sqrt(np.mean(mix**2))),'premaster_gain':gain,'stem_levels':levels,'note_events':len(score['events']),'drum_events':len(drum_events),'external_recording_samples':0,'original_synthesis':True}
(OUT/'audio-validation.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2),flush=True)

"""Original deterministic electronic score and UX effects. No sampled third-party audio."""
from pathlib import Path
import json, wave
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
cfg=json.loads((ROOT/'src/data/audio.json').read_text())
SR=cfg['sampleRate']; DUR=cfg['duration']; N=int(SR*DUR)
rng=np.random.default_rng(cfg['seed'])
music=np.zeros((N,2),dtype=np.float64); effects=np.zeros_like(music)
beat=60/cfg['tempo']
def hz(note):return 440*2**((note-69)/12)
def add(target,signal,start,gain=1,pan=0):
 start=int(start*SR)
 if start<0 or start>=N:return
 end=min(N,start+len(signal));signal=signal[:end-start]*gain
 target[start:end,0]+=signal*np.sqrt((1-pan)/2)
 target[start:end,1]+=signal*np.sqrt((1+pan)/2)
def tone(note,duration,kind='pluck'):
 t=np.arange(int(duration*SR))/SR;f=hz(note)
 if kind=='pad':
  sound=(np.sin(2*np.pi*f*t)+.25*np.sin(2*np.pi*f*1.0017*t)+.12*np.sin(2*np.pi*2*f*t))
  env=np.minimum(t/.25,1)*np.minimum((duration-t)/.5,1)
 else:
  sound=np.sin(2*np.pi*f*t)+.28*np.sin(2*np.pi*2*f*t)*np.exp(-t*9)+.08*np.sin(2*np.pi*3*f*t)*np.exp(-t*15)
  env=(1-np.exp(-t*280))*np.exp(-t*4.8)*np.minimum((duration-t)/.07,1)
 return sound*env
chords=[[50,57,61,66,69],[47,54,57,62,66],[43,50,54,59,62],[45,52,57,59,64]]
for bar in range(20):
 start=bar*4*beat;notes=chords[(bar//2)%4]
 for i,n in enumerate(notes):add(music,tone(n,4*beat+.6,'pad'),start,.035,pan=(i-2)*.27)
 for sub in range(8):
  if bar<1 and sub%2:continue
  n=notes[[2,3,4,3,1,4,3,2][sub]]+12
  add(music,tone(n,.85),start+sub*beat/2,.095 if bar>=6 else .075,(-1 if sub%2 else 1)*.3)
 for b in range(4):
  onset=start+b*beat
  if onset<3:continue
  t=np.arange(int(.23*SR))/SR
  kick=np.sin(2*np.pi*(48*t+40*.018*(1-np.exp(-t/.018))))*(1-np.exp(-t*700))*np.exp(-t*23)
  add(music,kick,onset,.28 if onset>=12.5 else .18)
  bassnote=notes[0]-12
  add(music,tone(bassnote,.38),onset,.20)
  if b in (1,3):
   tn=np.arange(int(.1*SR))/SR;noise=rng.normal(0,1,len(tn));noise=np.r_[0,np.diff(noise)]
   add(music,noise*np.exp(-tn*62)*(1-np.exp(-tn*900)),onset,.027,.08)
 for h in range(8):
  onset=start+h*beat/2
  if onset<7.5:continue
  t=np.arange(int(.045*SR))/SR;noise=rng.normal(0,1,len(t));noise=np.r_[0,np.diff(noise)]
  add(music,noise*np.exp(-t*115),onset,.011 if h%2 else .016,.45 if h%2 else -.35)
# Score resolves at the end-card, with a deliberate release instead of an abrupt cut.
timeline=np.arange(N)/SR
fade=np.clip(timeline/.45,0,1)*np.clip((43-timeline)/1.45,0,1)
duck=cfg['approvalDuck']
reduce=np.interp(timeline,[0,duck['start']-.25,duck['start']+.3,duck['end']-.1,duck['end']+.25,38,38.8,43],[1,1,duck['gain'],duck['gain'],1,1,.56,.56])
music*= (fade*reduce*cfg['musicGain'])[:,None]
for n in [50,57,62,66,69,73]:add(music,tone(n,4.1,'pad'),38.8,.035,(n%3-1)*.4)
for when,kind in cfg['cues']:
 if kind in ('send','receive','tick'):
  dur=.16 if kind=='send' else .13;t=np.arange(int(SR*dur))/SR
  f0=610 if kind=='send' else 1050
  slope=1400 if kind=='send' else -1200
  sig=np.sin(2*np.pi*(f0*t+.5*slope*t*t))*np.sin(np.pi*t/dur)**2*np.exp(-t*9)
  add(effects,sig,when,.19 if kind=='send' else .13,.18 if kind=='send' else -.18)
 elif kind in ('paper','expand'):
  dur=.22 if kind=='paper' else .42;t=np.arange(int(SR*dur))/SR
  noise=rng.normal(0,1,len(t));noise=np.convolve(noise,np.ones(45)/45,mode='same')
  sig=noise*np.sin(np.pi*t/dur)**2
  add(effects,sig,when,.22 if kind=='paper' else .32,-.10)
 else:
  for delay,n in [(0,74),(.07,78),(.13,81)]:add(effects,tone(n,.72),when+delay,.11,(n%3-1)*.25)
effects*=cfg['effectsGain']
mix=music+effects
mix*=np.clip((DUR-timeline)/.2,0,1)[:,None]
peak=np.max(np.abs(mix));scale=.82/max(peak,.82)
def write(name,a):
 with wave.open(str(ROOT/'public/audio'/name),'wb') as w:
  w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
  w.writeframes((np.clip(a*scale,-1,1)*32767).astype('<i2').tobytes())
write('music-original.wav',music);write('effects-original.wav',effects);write('mix-premaster.wav',mix)
print(json.dumps({'duration':DUR,'sample_rate':SR,'tempo':cfg['tempo'],'seed':cfg['seed'],'premaster_peak':float(np.max(np.abs(mix*scale))),'source':'Original procedural synthesis; no third-party samples.'}))

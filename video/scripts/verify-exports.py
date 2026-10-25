from pathlib import Path
import subprocess,json,struct
ROOT=Path(__file__).resolve().parents[1]
def probe(path):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def atoms(path):
 names=[]
 with path.open('rb') as f:
  while True:
   head=f.read(8)
   if len(head)<8:break
   size,kind=struct.unpack('>I4s',head);hsize=8
   if size==1:size=struct.unpack('>Q',f.read(8))[0];hsize=16
   names.append(kind.decode('ascii'))
   if size==0:break
   f.seek(size-hsize,1)
 return names
summary={}
for name,has_audio in [('job-ledger-launch-silent.mp4',False),('job-ledger-launch-1080x1920.mp4',True)]:
 path=ROOT/'deliverables'/name
 p=probe(path);v=next(s for s in p['streams'] if s['codec_type']=='video')
 assert (v['width'],v['height'])==(1080,1920),v
 assert v['codec_name']=='h264' and v['pix_fmt']=='yuv420p',v
 assert v['r_frame_rate']=='60/1',v
 assert int(v['nb_frames'])==2580,v
 assert abs(float(p['format']['duration'])-43)<.1,p
 a=[s for s in p['streams'] if s['codec_type']=='audio']
 assert bool(a)==has_audio
 if has_audio:assert a[0]['codec_name']=='aac'
 order=atoms(path);assert order.index('moov')<order.index('mdat'),order
 subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(path),'-f','null','-'],check=True)
 summary[name]={'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'frames':v['nb_frames'],'duration':p['format']['duration'],'video':v['codec_name'],'pixel_format':v['pix_fmt'],'audio':a[0]['codec_name'] if a else None,'fast_start':True,'full_decode':'passed','bytes':int(p['format']['size'])}
 r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-vf','blackdetect=d=0.10:pix_th=0.05','-an','-f','null','-'],capture_output=True,text=True,check=True)
 black=[line for line in r.stderr.splitlines() if 'black_start' in line];assert not black,black
 summary[name]['black_frames']='none detected (0.10s threshold)'
 if has_audio:
  r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-vn','-af','loudnorm=I=-14:TP=-1:LRA=8:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
  j=json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0]
  summary[name]['audio_measurement']={'integrated_lufs':float(j['input_i']),'true_peak_dbtp':float(j['input_tp']),'lra':float(j['input_lra'])}
  assert -15<=float(j['input_i'])<=-13,j
  assert float(j['input_tp'])<=-1,j
  (ROOT/'deliverables/audio-verification.json').write_text(json.dumps(j,indent=2))
(ROOT/'deliverables/verification.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))

from pathlib import Path
import json,subprocess
root=Path(__file__).resolve().parents[1]
def measured(text):
 start=text.rfind('{')
 return json.JSONDecoder().raw_decode(text[start:])[0]
r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(root/'public/audio/mix-premaster.wav'),'-af','loudnorm=I=-14:TP=-1.5:LRA=8:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
(root/'output/loudness-pass1.log').write_text(r.stderr)
j=measured(r.stderr)
(root/'output/loudness-pass1.json').write_text(json.dumps(j,indent=2))
f='loudnorm=I=-14:TP=-1.5:LRA=8:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}:linear=true:print_format=json'.format(**j)
r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-y','-i',str(root/'public/audio/mix-premaster.wav'),'-af',f,'-ar','48000','-c:a','pcm_s24le',str(root/'public/audio/launch-master.wav')],capture_output=True,text=True,check=True)
(root/'output/loudness-pass2.log').write_text(r.stderr)
print(json.dumps(measured(r.stderr),indent=2))

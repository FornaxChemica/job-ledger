from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'deliverables';VIDEO=OUT/'job-ledger-launch-silent.mp4'
frames=[('Opening hook',2),('Supplied background',6.6),('Opportunity',10.8),('Tailoring',19.4),('Review package',25.9),('Submission approval',33),('Application dashboard',37),('Brand and CTA',41)]
stills=ROOT/'output/final-stills';stills.mkdir(parents=True,exist_ok=True)
for name,time in frames:
 f=stills/(name.lower().replace(' ','-')+'.png')
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(time),'-i',str(VIDEO),'-frames:v','1',str(f)],check=True)
canvas=Image.new('RGB',(1440,1360),'#17222f');d=ImageDraw.Draw(canvas)
font=ImageFont.truetype(str(ROOT/'public/fonts/SourceSans3-Regular.ttf'),22)
for i,(name,time) in enumerate(frames):
 f=stills/(name.lower().replace(' ','-')+'.png')
 image=Image.open(f).convert('RGB').resize((360,640),Image.Resampling.LANCZOS)
 x=i%4*360;y=i//4*680;canvas.paste(image,(x,y));d.text((x+13,y+647),f'{time:04.1f}s  {name}',fill='white',font=font)
canvas.save(OUT/'job-ledger-storyboard.jpg',quality=95)
Image.open(stills/'brand-and-cta.png').save(OUT/'job-ledger-poster.png')
# Explicit first/last checks: extract exact frame numbers, not a seek after EOF.
for label,number in [('first',0),('last',2579)]:
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(VIDEO),'-vf',f'select=eq(n\\,{number})','-frames:v','1',str(stills/f'{label}.png')],check=True)
 im=Image.open(stills/f'{label}.png').convert('L');assert im.getextrema()[1]>200
print('Poster, eight-shot contact sheet and first/last-frame checks complete.')

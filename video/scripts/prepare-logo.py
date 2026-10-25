"""Crop dark surround from the user's original image; never synthesize a replacement.
Usage: .audio-venv/bin/python scripts/prepare-logo.py /path/to/original.png
Requires Pillow (use the Job Ledger venv on this prepared machine).
"""
from pathlib import Path
import sys,json,shutil,hashlib
from PIL import Image
root=Path(__file__).resolve().parents[1];src=Path(sys.argv[1]);source=Image.open(src);im=source.convert('RGB')
# Locate the white avatar using bright, nearly neutral pixels. Preserve original geometry.
px=im.load();m=Image.new('L',im.size);mp=m.load()
for y in range(im.height):
 for x in range(im.width):
  r,g,b=px[x,y]
  if min(r,g,b)>225 and max(r,g,b)-min(r,g,b)<20:mp[x,y]=255
box=m.getbbox()
if not box:raise RuntimeError('No white avatar detected; inspect the source manually.')
side=max(box[2]-box[0],box[3]-box[1]);cx=(box[0]+box[2])/2;cy=(box[1]+box[3])/2
crop=(round(cx-side/2),round(cy-side/2),round(cx+side/2),round(cy+side/2))
out=root/'public/brand';out.mkdir(parents=True,exist_ok=True)
extension={'JPEG':'.jpeg','PNG':'.png','WEBP':'.webp'}.get(source.format,src.suffix.lower())
original=out/('cubbie-original'+extension)
if src.resolve()!=original.resolve():shutil.copy2(src,original)
im.crop(crop).save(out/'cubbie-avatar.png')
manifest={'original':'brand/'+original.name,'uploaded_source':'brand/'+src.name,'prepared':'brand/cubbie-avatar.png','status':'Prepared from the actual supplied image, without redrawing or recoloring. Circular CSS mask preserves intentional white avatar.','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'original_size':im.size,'crop':crop}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
p=root/'src/components/BrandAvatar.tsx';s=p.read_text().replace('HAS_ORIGINAL_LOGO = false','HAS_ORIGINAL_LOGO = true');p.write_text(s)
print(json.dumps(manifest,indent=2))

"""Prepare supplied camera media for the homepage. Originals remain untouched.
Requires macOS sips, FFmpeg 9 and Pillow. Run from this repository.
"""
from pathlib import Path
from PIL import Image, ImageOps
import json, subprocess, tempfile, concurrent.futures
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'Immagini:Video'
DEST=ROOT/'img/real'; DEST.mkdir(exist_ok=True)
FF='/opt/homebrew/bin/ffmpeg'
# Normalize iPhone HLG footage to SDR, retaining original content and framing.
# peak=1 clipped diffuse whites in the previous export. The reviewed peak=2
# mapping preserves flour, dough and room highlights. Version paths defeat caches.
COLOR='fps=30,scale=1280:-2,scale=out_transfer=linear:out_primaries=bt709,format=gbrpf32le,tonemap=tonemap=hable:desat=0:peak=2,scale=out_transfer=bt709:out_color_matrix=bt709,format=yuv420p,sidedata=mode=delete'
clips=[('stesura','IMG_8359.MOV',24,20,36),('condimento','IMG_8361.MOV',8,30,32),('cottura','IMG_8364.MOV',0,35,29)]
def export_clip(item):
 name,source,start,duration,poster=item
 target=ROOT/'videos'/f'{name}-sdr-v2.mp4'
 cmd=[FF,'-v','error','-noautorotate','-display_rotation:v:0','0','-ss',str(start),'-i',str(SOURCE/source),'-t',str(duration),'-map','0:v:0','-map','0:a:0?','-vf',COLOR,'-r','30','-c:v','libx264','-preset','fast','-crf','24','-threads','2','-c:a','aac','-b:a','96k','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-metadata:s:v:0','rotate=0','-map_metadata','-1','-movflags','+faststart','-y',str(target)]
 if not target.exists():subprocess.run(cmd,check=True)
 with tempfile.TemporaryDirectory() as tmp:
  still=Path(tmp)/'poster.jpg'
  subprocess.run([FF,'-v','error','-ss',str(poster-start),'-i',str(target),'-frames:v','1','-y',str(still)],check=True)
  variants=export_image(Image.open(still),name+'-sdr-v2')
 print(name,round(target.stat().st_size/1024/1024,2),'MB',flush=True)
 return name,{'id':name,'name':{'stesura':'Stesura dell’impasto da Sorriso Bistrot','condimento':'Preparazione della pizza da Sorriso Bistrot','cottura':'Pizza appena sfornata da Sorriso Bistrot'}[name],'illustrative':False,'source':source,'excerpt_start':start,'excerpt_duration':duration,'video':'videos/'+target.name,'variants':variants}
def export_image(im,name):
 im=ImageOps.exif_transpose(im).convert('RGB');variants=[]
 for w in sorted({min(w,im.width) for w in [480,960,1280]}):
  h=round(im.height*w/im.width);f=DEST/f'{name}-{w}.webp';im.resize((w,h),Image.Resampling.LANCZOS).save(f,'WEBP',quality=84,method=6);variants.append({'src':f.relative_to(ROOT).as_posix(),'width':w,'height':h})
 return variants
def export_loop(name,source,start,duration,width,title):
 target=ROOT/'videos'/f'{name}-sdr-v2.mp4'
 color=COLOR.replace('scale=1280:',f'scale={width}:')
 cmd=[FF,'-v','error','-ss',str(start),'-i',str(source),'-t',str(duration),'-map','0:v:0','-an','-vf',color,'-r','30','-c:v','libx264','-preset','fast','-crf','24','-threads','2','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-map_metadata','-1','-movflags','+faststart','-y',str(target)]
 if not target.exists():subprocess.run(cmd,check=True)
 with tempfile.TemporaryDirectory() as tmp:
  still=Path(tmp)/'poster.jpg'
  subprocess.run([FF,'-v','error','-ss','1','-i',str(target),'-frames:v','1','-y',str(still)],check=True)
  variants=export_image(Image.open(still),name+'-sdr-v2')
 print(name,round(target.stat().st_size/1024/1024,2),'MB',flush=True)
 return {'id':name,'name':title,'illustrative':False,'source':source.name,'excerpt_start':start,'excerpt_duration':duration,'video':'videos/'+target.name,'variants':variants}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: assets={'home/'+n:a for n,a in pool.map(export_clip,clips)}
 with tempfile.TemporaryDirectory() as tmp:
  file=Path(tmp)/'fritto.jpg';subprocess.run(['sips','-s','format','jpeg',str(SOURCE/'IMG_8366.HEIC'),'--out',str(file)],stdout=subprocess.DEVNULL,check=True)
  assets['home/fritti']={'id':'fritti','name':'Un fritto preparato da Sorriso Bistrot','illustrative':False,'source':'IMG_8366.HEIC','variants':export_image(Image.open(file),'fritti')}
 assets['home/sala']=export_loop('sala-via-sarnano',Path.home()/'Downloads/IMG_6202.mov',0,2.555,720,'La sala di Sorriso Bistrot')
 assets['home/dough-canapa']=export_loop('impasto-canapa-5s',SOURCE/'IMG_8326.mov',2,5,960,'Impasto con semi di canapa bio italiani')
 (ROOT/'real-media.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n')

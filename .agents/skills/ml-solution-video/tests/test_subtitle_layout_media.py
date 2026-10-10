from fixtures import *
import subprocess,io
from PIL import Image
from solution_video.subtitles import burn_subtitles
from solution_video.media import ffmpeg

class SubtitleLayoutMediaTests(Sandbox):
 def test_libass_respects_explicit_lines(self):
  master=self.run/'master.mp4'
  subprocess.run([ffmpeg(),'-y','-v','error','-f','lavfi','-i','color=c=black:s=1920x1080:r=30:d=1',
                  '-c:v','libx264','-pix_fmt','yuv420p',str(master)],check=True,capture_output=True)
  font=S/'assets/fonts/Pretendard-Bold.ttf'
  for count,text in [(1,'전류는 2ΔI입니다.'),(2,'저항으로 흐르는 전류는\n(I₀ + ΔI) − (I₀ − ΔI)입니다.')]:
   with self.subTest(lines=count):
    srt=self.run/'test.srt';srt.write_text('1\n00:00:00,000 --> 00:00:01,000\n'+text+'\n')
    final=burn_subtitles(master,srt,self.run/'final.mp4',font)
    data=subprocess.run([ffmpeg(),'-v','error','-ss','0.5','-i',str(final),'-frames:v','1','-f','image2pipe','-vcodec','png','-'],check=True,capture_output=True).stdout
    pic=Image.open(io.BytesIO(data)).convert('RGB');pixels=pic.load();rows=[];xs=[]
    for y in range(900,1080):
     found=[x for x in range(1920) if min(pixels[x,y])>=230]
     if len(found)>=3:rows.append(y);xs.extend(found)
    bands=[]
    for y in rows:
     if not bands or y-bands[-1][-1]>3:bands.append([y])
     else:bands[-1].append(y)
    self.assertEqual(len(bands),count)
    self.assertTrue(xs);self.assertGreater(min(xs),0);self.assertLess(max(xs),1919)
    self.assertGreaterEqual(rows[0],900);self.assertLess(rows[-1],1080)

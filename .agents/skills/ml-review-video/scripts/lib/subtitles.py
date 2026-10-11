"""하드 자막 굽기: narration.srt를 짧은 한 줄 자막으로 쪼개 하단 중앙에 넣는다. 설정은 고정이다."""
from pathlib import Path
import os,re,shutil,subprocess
from .render import dark_failures

FONT_DIR=Path(__file__).resolve().parents[2]/'assets/fonts'
# libass 기본 PlayRes(288) 기준 값이다. 1080p에서 글자 약 52px, 하단에서 약 80px 위.
# BorderStyle=3은 외곽선 대신 박스를 그린다. 색은 OutlineColour(박스)·BackColour, 알파 4D는 약 70% 불투명, Outline=4가 박스 패딩이다.
STYLE=("FontName=Pretendard,FontSize=14,Bold=1,Alignment=2,MarginV=22,Outline=4,Shadow=0,"
       "BorderStyle=3,PrimaryColour=&HFFFFFF&,OutlineColour=&H4D0E0B0B,BackColour=&H4D0E0B0B")
MAX_SENTENCE=36; MAX_CHUNK=34; WRAP_AT=40

def _seconds(stamp):
    h,m,rest=stamp.split(':'); s,ms=rest.split(',')
    return int(h)*3600+int(m)*60+int(s)+int(ms)/1000

def _stamp(x):
    ms=round(x*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

def _chunks(text):
    out=[]
    for sentence in (s for s in re.split(r'(?<=[.!?])\s+',text) if s):
        if len(sentence)<=MAX_SENTENCE: out.append(sentence); continue
        cur=''
        for part in re.split(r'(?<=[,])\s+|(?<=[요죠다])\s+(?=[가-힣])',sentence):
            if cur and len(cur)+len(part)>MAX_CHUNK: out.append(cur); cur=part
            else: cur=(cur+' '+part).strip()
        if cur: out.append(cur)
    return out

# Keep numeric values and attached units in one wrapping atom, including Korean suffixes.
_NUMBER = r'[+−-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][+−-]?\d+)?(?:/\d+)?(?:[–~]\d+(?:\.\d+)?)?'
_UNIT = r'(?:MHz|kHz|Hz|ms|cm|mm|mV|mA|kg|μs|us|m|s|V|A|W|Ω|°C|g|%|초|밀리초|개|회|배|차원)'
_WRAP_ATOM = re.compile(r'[([{]?' + _NUMBER + r'[^\S\r\n]+' + _UNIT + r'(?:[가-힣]+)?[.,!?;:)\]}]*(?=\s|$)|\S+')

def split_srt(source):
    """긴 문단 자막을 문장·쉼표 단위로 쪼개고 글자 수에 비례해 시간을 나눈다."""
    cues=[]; n=1
    for block in Path(source).read_text(encoding='utf-8').strip().split('\n\n'):
        lines=block.split('\n'); start,end=(_seconds(x) for x in lines[1].split(' --> '))
        chunks=_chunks(' '.join(lines[2:])); total=sum(len(c) for c in chunks) or 1; cursor=start
        for chunk in chunks:
            length=(end-start)*len(chunk)/total
            words=_WRAP_ATOM.findall(chunk)
            if len(chunk)>WRAP_AT and len(words)>1:
                cut=min(range(1,len(words)),key=lambda i:abs(len(' '.join(words[:i]))-len(' '.join(words[i:]))))
                chunk=' '.join(words[:cut])+'\n'+' '.join(words[cut:])
            cues.append(f'{n}\n{_stamp(cursor)} --> {_stamp(cursor+length)}\n{chunk}\n'); n+=1; cursor+=length
    return '\n'.join(cues)

def _subtitle_ffmpeg(candidates=None):
    """Use a libass-capable executable without changing the user's PATH."""
    if candidates is None:
        candidates=[shutil.which('ffmpeg'),'/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg','/usr/local/opt/ffmpeg-full/bin/ffmpeg']
    for executable in dict.fromkeys(x for x in candidates if x):
        try:
            probe=subprocess.run([executable,'-hide_banner','-filters'],capture_output=True,text=True,timeout=15)
        except (OSError,subprocess.TimeoutExpired):continue
        if probe.returncode==0 and any(len(line.split())>1 and line.split()[1]=='subtitles' for line in probe.stdout.splitlines()):
            return executable
    raise RuntimeError('FFmpeg with the subtitles/libass filter is required (macOS: brew install ffmpeg-full)')

def burn_subtitles(video,srt,destination):
    """video를 재인코딩해 자막을 굽고 destination에 쓴다. 원본은 수정하지 않는다."""
    video,destination=Path(video).resolve(),Path(destination).resolve()
    if video==destination: raise ValueError('refusing to overwrite source')
    ffmpeg=_subtitle_ffmpeg()
    if not (FONT_DIR/'Pretendard-Bold.ttf').is_file(): raise RuntimeError('Pretendard Bold TTF is required; do not substitute a system font')
    light=dark_failures(video)
    if light: raise ValueError(f'source video is not dark mode at {light}s; re-render scenes via render_parts')
    work=destination.parent/(destination.stem+'.subwork'); work.mkdir(parents=True,exist_ok=True)
    try:
        (work/'subs.srt').write_text(split_srt(srt),encoding='utf-8')
        fonts=work/'fonts'; fonts.mkdir(exist_ok=True)
        for ttf in FONT_DIR.glob('*.ttf'): shutil.copy2(ttf,fonts/ttf.name)
        pending=destination.with_name(destination.stem+'.pending.mp4')
        # 상대 경로로 넘겨 Windows 드라이브 문자·한글 경로 문제를 피한다.
        r=subprocess.run([ffmpeg,'-y','-v','error','-i',str(video),
            '-vf',f"subtitles=subs.srt:fontsdir=fonts:force_style='{STYLE}'",
            '-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(pending)],
            cwd=work,capture_output=True,text=True,encoding='utf-8',errors='replace',
            creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        if r.returncode: raise RuntimeError('subtitle burn failed: '+r.stderr[-400:])
        os.replace(pending,destination)
    finally: shutil.rmtree(work,ignore_errors=True)
    return destination

import sys
from PIL import Image
from pathlib import Path
src, cols, TW = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
for f in sorted(src.glob('*.png')):
    if '-grid' in f.name: continue
    im = Image.open(f); H = im.size[1]; n = (im.size[0] + 8)//(TW + 8)
    tiles = [im.crop((i*(TW+8), 0, i*(TW+8)+TW, H)) for i in range(n)]
    rows = (n + cols - 1)//cols
    g = Image.new('RGB', (cols*(TW+8), rows*(H+8)), 'gray')
    for i,t in enumerate(tiles): g.paste(t, ((i%cols)*(TW+8), (i//cols)*(H+8)))
    g.save(f.with_name(f.stem + '-grid.png')); print(f.name, n, g.size)

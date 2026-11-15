import hashlib
import json
from pathlib import Path
import unicodedata
import unittest
from _util import REPO
from review_pdf_cards import read_cards,normalize_cards
from review_sources import discover_reviews, legacy_digest, source_markdown
from manifest import PACK_DIR,pdf_names

COUNTS={'0909':5,'0914':7,'0916':6,'0921':6,'0923':7,'0928':8,'0930':8}
class TestMigration(unittest.TestCase):
    def test_all_47_cards_have_preserving_layouts(self):
        notes=next(p for p in REPO.iterdir() if unicodedata.normalize('NFC',p.name)=='복습노트')
        counts={};names=[]
        for date in COUNTS:
            source, = discover_reviews(notes/date)
            pack=read_cards(source);counts[date]=len(pack.cards);names.extend(pdf_names(pack.range,pack.slug))
            layout_path=REPO/f'workbook/layouts/{date}_{pack.slug}.json'
            self.assertTrue(layout_path.exists(),f'{date}: missing layout')
            normalized=normalize_cards(pack,json.loads(layout_path.read_text()),source)
            self.assertEqual(len(normalized),COUNTS[date])
        self.assertEqual(counts,COUNTS);self.assertEqual(sum(counts.values()),47);self.assertEqual(len(set(names)),14)

    def test_published_pairs_and_originals_preserved(self):
        notes=next(p for p in REPO.iterdir() if unicodedata.normalize('NFC',p.name)=='복습노트')
        for date,count in COUNTS.items():
            folder=notes/date;pack_dir=folder/PACK_DIR
            source, = discover_reviews(folder)
            pack=read_cards(source);layout=json.loads((REPO/f'workbook/layouts/{date}_{pack.slug}.json').read_text())
            self.assertEqual(legacy_digest(source),layout['source_sha256'])
            self.assertEqual(hashlib.sha256(source_markdown(source).read_bytes()).hexdigest(),layout['review_md_sha256'])
            for rel,sha in layout['figures_sha256'].items():self.assertEqual(hashlib.sha256((pack_dir/rel).read_bytes()).hexdigest(),sha)
            for name in pdf_names(date,pack.slug):
                self.assertTrue((pack_dir/name).is_file(),name)
                self.assertIn(f'{PACK_DIR}/{name}',next(folder.glob('정리노트*html')).read_text())
                self.assertIn(f'({name})',next(pack_dir.glob('정리노트*md')).read_text())

    def test_published_pairs_are_widescreen_and_caption_safe(self):
        import fitz
        from build_review_pdf import _verify_pdf
        notes=next(p for p in REPO.iterdir() if unicodedata.normalize('NFC',p.name)=='복습노트')
        paths=[p for date in COUNTS for p in (notes/date/PACK_DIR).glob('*.pdf')]
        self.assertEqual(len(paths),14)
        for path in paths:
            with fitz.open(path) as doc:
                for page in doc:
                    self.assertAlmostEqual(page.rect.width,1440,delta=.1)
                    self.assertAlmostEqual(page.rect.height,810,delta=.1)
                    self.assertFalse(page.get_text(clip=fitz.Rect(0,675,1440,810)).strip())
                _verify_pdf(path,len(doc),'video-16x9')

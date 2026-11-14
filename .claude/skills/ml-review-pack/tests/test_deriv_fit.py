"""Run the template's deriv-fit script and check the 식 줄 + 주석 CSS contract."""
import json
from pathlib import Path
import re
import subprocess
import unittest


TEMPLATE = Path(__file__).resolve().parents[1] / "assets/note-template.html"


class TestDerivFit(unittest.TestCase):
    def wide_flags(self, sizes):
        script = re.search(r'<script id="deriv-fit">(.*?)</script>', TEMPLATE.read_text(), re.S).group(1)
        harness = r"""
const vm = require('node:vm');
const sizes = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
const rows = sizes.map(([sw, cw]) => {
  const set = new Set(['is-wide']);  // stale class must be recomputed
  return {
    classList: { remove: c => set.delete(c), toggle: (c, on) => on ? set.add(c) : set.delete(c), has: c => set.has(c) },
    querySelector: () => (sw === null ? null : { scrollWidth: sw, clientWidth: cw })
  };
});
const list = { children: rows, clientWidth: 600 };
const ctx = {
  window: {}, document: { readyState: 'complete', querySelectorAll: () => [list] }
};
vm.createContext(ctx);
vm.runInContext(process.argv[1], ctx);
process.stdout.write(JSON.stringify(rows.map(r => r.classList.has('is-wide'))));
"""
        out = subprocess.run(["node", "-e", harness, script], input=json.dumps(sizes),
                             capture_output=True, text=True, check=True)
        return json.loads(out.stdout)

    def test_only_overflowing_rows_become_wide(self):
        self.assertEqual(self.wide_flags([[300, 300], [521, 379], [380, 379], [None, None]]),
                         [False, True, False, False])

    def test_css_contract_present(self):
        src = TEMPLATE.read_text()
        for needle in (".deriv-body", ".deriv > li.is-wide", ".deriv > li.deriv-gen",
                       '.deriv .katex [style*="color:#"]', "@container (max-width: 620px)"):
            self.assertIn(needle, src)
        self.assertNotIn("deriv-switch", src)


if __name__ == "__main__":
    unittest.main()

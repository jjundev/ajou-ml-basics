"""Run the template's actual navigation script with measured layout scenarios."""
import json
from pathlib import Path
import re
import subprocess
import unittest


TEMPLATE = Path(__file__).resolve().parents[1] / "assets/note-template.html"


class TestStageNavigation(unittest.TestCase):
    def active_stage(self, scroll_top, heading_tops):
        script = re.search(
            r'<script id="note-stage-navigation">(.*?)</script>',
            TEMPLATE.read_text(), re.S,
        ).group(1)
        # No browser dependency: geometry inputs reproduce the observed short final
        # stage at the end of a scroll container. Execute production JS unchanged.
        harness = r"""
const vm = require('node:vm');
const input = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
const links = input.tops.map((top, i) => ({
  hash: '#stage-' + i, attrs: {},
  getAttribute(k) { return this.attrs[k]; },
  setAttribute(k, v) { this.attrs[k] = v; },
  removeAttribute(k) { delete this.attrs[k]; },
  getBoundingClientRect() { return { left: 0, right: 80 }; }
}));
const nav = {
  querySelectorAll() { return links; },
  getBoundingClientRect() { return { bottom: 101, left: 0, right: 632 }; },
  scrollLeft: 0
};
const topic = {
  querySelector() { return nav; },
  getClientRects() { return [{}]; }
};
const scroller = {
  scrollTop: input.scrollTop, clientHeight: 764, scrollHeight: 5664,
  addEventListener() {}
};
const document = {
  querySelector() { return scroller; },
  querySelectorAll() { return [topic]; },
  getElementById(id) {
    return { getBoundingClientRect() { return { top: input.tops[+id.slice(6)] }; } };
  },
  addEventListener() {}
};
vm.runInNewContext(input.script, {
  document, window: { addEventListener() {} },
  requestAnimationFrame(callback) { callback(); }
});
console.log(JSON.stringify(links.findIndex(link => link.attrs['aria-current'] === 'step')));
"""
        result = subprocess.run(
            ["node", "-e", harness],
            input=json.dumps({"script": script, "scrollTop": scroll_top, "tops": heading_tops}),
            text=True, capture_output=True, check=True,
        )
        return json.loads(result.stdout)

    def test_short_final_stage_is_current_at_scroll_end(self):
        self.assertEqual(self.active_stage(4900.5, [-4000, -2000, -300, 432]), 3)

    def test_midpage_keeps_the_stage_at_the_reading_boundary(self):
        self.assertEqual(self.active_stage(3000, [-2100, -700, 144, 900]), 2)

    def test_top_does_not_jump_to_a_later_visible_heading(self):
        self.assertEqual(self.active_stage(0, [280, 900, 1400, 2000]), 0)

"""Remove redundant paragraph labels only inside explicitly headed subparts."""
import re
from mpe_shared import Node, parse, inner


def normalize_subpart_labels(markup):
    root = parse(markup)
    changed = False

    def text_leaves(node):
        for index, child in enumerate(node.children):
            if isinstance(child, str):
                yield node, index, child
            elif isinstance(child, Node):
                yield from text_leaves(child)

    for section in root.find_all(lambda n: n.attrs.get('data-explanation') in ('solve', 'verify')):
        for block in section.find_all(lambda n: 'data-subpart' in n.attrs):
            label = block.attrs['data-subpart']
            if not re.fullmatch('[a-z]', label):
                continue
            heading = re.compile(r'^\(' + label + r'\)(?:\s|$)')
            if not any(isinstance(n, Node) and n.tag in ('h3', 'h4', 'h5', 'h6')
                       and heading.match(n.text().strip()) for n in block.children):
                continue
            prefix = re.compile(r'^\s*\(' + label + r'\)\s+')
            for paragraph in block.find_all(lambda n: n.tag == 'p'):
                for parent, index, text in text_leaves(paragraph):
                    if not text.strip():
                        continue
                    match = prefix.match(text)
                    if match:
                        parent.children[index] = text[match.end():]
                        changed = True
                    break
    return inner(root) if changed else markup

"""Verify that the GitHub Pages artifact has no broken local links or assets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

SITE = Path(__file__).resolve().parent.parent / 'docs'

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ['src', 'href', 'poster', 'data-image'] and value:
                self.references.append(value)

missing = []
total = 0
files = list(SITE.rglob('*.html'))
assert (SITE / 'index.html').is_file(), 'Build the site first.'
assert (SITE / '.nojekyll').is_file()
for file in files:
    parser = References()
    parser.feed(file.read_text(encoding='utf-8'))
    for reference in parser.references:
        url = urlsplit(reference)
        if url.scheme or reference.startswith('#'):
            continue
        total += 1
        target = (file.parent / unquote(url.path)).resolve()
        if not target.is_relative_to(SITE.resolve()) or not target.exists():
            missing.append(f'{file.relative_to(SITE)}: {reference}')
assert not missing, '\n'.join(missing)
print(f'Checked {len(files)} pages and {total} local links/assets.')

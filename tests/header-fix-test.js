// The page script rewrites only unraid.net home links in the header logo and keeps watching the DOM.
const assert = require('node:assert/strict'), fs = require('node:fs'), vm = require('node:vm');
const page = fs.readFileSync('src/usr/local/emhttp/plugins/header-fix/HeaderFix.page', 'utf8');
assert.match(page, /^Menu="Buttons:299"\nLink="nav-user"\n---\n<script>\n/);
const script = page.split('<script>\n')[1].split('</script>')[0];

const link = href => ({
  href, attrs: { target: '_blank', rel: 'noopener' },
  removeAttribute(name) { delete this.attrs[name]; },
});
let links = [], selectors = null, observed = null, observerCallback = null, frames = [];
const context = {
  URL,
  document: {
    documentElement: {},
    querySelectorAll: selector => { selectors = selector; return links; },
  },
  MutationObserver: class { constructor(cb) { observerCallback = cb; } observe(target, options) { observed = [target, options]; } },
  requestAnimationFrame: fn => frames.push(fn),
};

const legacy = link('https://unraid.net'), rc2 = link('https://unraid.net/'), docs = link('https://docs.unraid.net/x');
const deep = link('https://unraid.net/blog'), query = link('https://unraid.net/?ref=x'), broken = link('not a url');
links = [legacy, rc2, docs, deep, query, broken];
vm.runInNewContext(script, context);

for (const selector of ['unraid-header-os-version a[href]', 'unraid-header .uh-logo-block a[href]',
  'unraid-header a.uh-logo', '.unraid-header-boot-logo a']) {
  assert.ok(selectors.split(', ').includes(selector), selector);
}
for (const l of [legacy, rc2]) assert.deepEqual([l.href, l.attrs], ['/', {}]);
for (const l of [docs, deep, query, broken]) assert.equal(l.attrs.target, '_blank', l.href);
assert.equal(docs.href, 'https://docs.unraid.net/x');
assert.equal(observed[0], context.document.documentElement);
assert.deepEqual({ ...observed[1], attributeFilter: [...observed[1].attributeFilter] },
  { childList: true, subtree: true, attributes: true, attributeFilter: ['href'] });

// The mounted Vue logo replaces the boot placeholder; several mutations share one frame.
const mounted = link('https://unraid.net');
links = [mounted];
observerCallback(); observerCallback();
assert.equal(frames.length, 1);
frames.shift()();
assert.deepEqual([mounted.href, mounted.attrs], ['/', {}]);
observerCallback();
assert.equal(frames.length, 1, 'A new frame is scheduled after the previous one ran');
console.log('Header logo links are rewritten on load and after mount; other links stay unchanged.');

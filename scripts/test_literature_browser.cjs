// Exercise the generated browser's real script without a browser dependency.
// This checks filtering/rendering logic, not visual layout.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'literature/literature_browser.html'), 'utf8');
const records = JSON.parse(fs.readFileSync(path.join(root, 'literature/literature_database.json'), 'utf8')).records;
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const element = () => ({
  value: '', innerHTML: '', textContent: '', handlers: {},
  addEventListener(event, handler) { this.handlers[event] = handler; },
});
const nodes = new Map([...html.matchAll(/id="([^"]+)"/g)].map(m => ['#' + m[1], element()]));
const shortcuts = [...html.matchAll(/data-connection="([^"]+)"/g)].map(m =>
  Object.assign(element(), { dataset: { connection: m[1] } }));
const document = {
  querySelector(selector) { assert(nodes.has(selector), selector); return nodes.get(selector); },
  querySelectorAll(selector) { assert.equal(selector, '[data-connection]'); return shortcuts; },
};
vm.runInNewContext(script, { document });
const shown = () => (nodes.get('#results').innerHTML.match(/<article /g) || []).length;
const reset = () => nodes.get('#reset').handlers.click();
const filter = (id, value) => {
  nodes.get('#' + id).value = value;
  nodes.get('#' + id).handlers.input();
};
assert.equal(shown(), records.length);
assert(nodes.get('#build').textContent.includes(records.length + ' registros'));
filter('q', 'autorkausik2026');
assert.equal(shown(), 1);
assert(nodes.get('#results').innerHTML.includes('Terminología de la fuente'));
reset();
for (const button of shortcuts) {
  button.handlers.click();
  const expected = records.filter(x => (x.connection_themes || '').split(';')
    .map(s => s.trim()).includes(button.dataset.connection)).length;
  assert.equal(shown(), expected, button.dataset.connection);
  assert(expected > 0);
}
reset();
filter('reading', 'reviewed');
assert.equal(shown(), records.filter(x => x.reading_status === 'pasajes originales revisados').length);
filter('reading', 'pending');
assert.equal(shown(), records.filter(x => x.reading_status !== 'pasajes originales revisados').length);
reset();
filter('paper', 'rewrite');
filter('priority', 'alta');
assert.equal(shown(), records.filter(x => x.cited_in_rewrite === 'yes' && x.review_priority === 'alta').length);
filter('q', 'no-such-reference-987654321');
assert.equal(shown(), 0);
assert(nodes.get('#results').innerHTML.includes('No hay resultados'));
reset();
assert.equal(shown(), records.length);
console.log('PASS: initial render, search, seven shortcuts, reading status, combined filters, empty result, reset.');

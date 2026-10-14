'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const cli = require('../bin/vibe-os.cjs');
const entry = path.resolve(__dirname, '../bin/vibe-os.cjs');

function fixture(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'vibe-os-node-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
}
function run(cwd, ...args) { return spawnSync(process.execPath, [entry, ...args], { cwd, encoding: 'utf8' }); }

test('version command', () => {
  const result = run(process.cwd(), '--version');
  assert.equal(result.status, 0);
  assert.match(result.stdout, /^1\.0\.0\s*$/);
});
test('help documents GitHub npx bootstrap', () => {
  const result = run(process.cwd(), '--help');
  assert.equal(result.status, 0);
  assert.match(result.stdout, /npx --yes github:priyansh985\/vibe-os/);
});
test('default init installs every integration without Python', (t) => {
  const project = fixture(t);
  const result = run(project, 'init');
  assert.equal(result.status, 0, result.stderr);
  for (const f of ['.agents/skills/vibe-os/SKILL.md', '.claude/skills/vibe-os/SKILL.md', '.cursor/rules/vibe-os.mdc', '.vibeos/config.json', '.vibeos/context.md']) {
    assert.ok(fs.statSync(path.join(project, f)).isFile(), f);
  }
  assert.equal(cli.doctor(project, () => {}), 0);
});
test('agent option only installs selected adapter', (t) => {
  const project = fixture(t);
  assert.equal(run(project, 'init', '--agent', 'cursor').status, 0);
  assert.equal(fs.existsSync(path.join(project, '.agents')), false);
  assert.equal(fs.existsSync(path.join(project, '.claude')), false);
  assert.ok(fs.existsSync(path.join(project, '.cursor/rules/vibe-os.mdc')));
});
test('repeated installation preserves edits without force', (t) => {
  const project = fixture(t);
  assert.equal(run(project, 'init', '--agent', 'codex').status, 0);
  const file = path.join(project, '.agents/skills/vibe-os/SKILL.md');
  fs.writeFileSync(file, 'customized');
  const result = run(project, 'init', '--agent', 'codex');
  assert.equal(result.status, 0);
  assert.equal(fs.readFileSync(file, 'utf8'), 'customized');
  assert.match(result.stdout, /SKIPPED/);
});
test('explicit force refreshes managed files and preserves extra files', (t) => {
  const project = fixture(t);
  assert.equal(run(project, 'init', '--agent', 'codex').status, 0);
  const dir = path.join(project, '.agents/skills/vibe-os');
  const file = path.join(dir, 'SKILL.md');
  fs.writeFileSync(file, 'customized');
  fs.writeFileSync(path.join(dir, 'my-notes.md'), 'unmanaged');
  assert.equal(run(project, 'init', '--agent', 'codex', '--force').status, 0);
  assert.match(fs.readFileSync(file, 'utf8'), /^---/);
  assert.equal(fs.readFileSync(path.join(dir, 'my-notes.md'), 'utf8'), 'unmanaged');
});
test('symlink traversal is rejected rather than writing outside project', (t) => {
  if (process.platform === 'win32') return t.skip('symlink creation may require privileges');
  const project = fixture(t);
  const outside = fixture(t);
  fs.symlinkSync(outside, path.join(project, '.agents'), 'dir');
  const result = run(project, 'init', '--agent', 'codex');
  assert.equal(result.status, 2);
  assert.match(result.stderr, /Refusing symlink/);
  assert.deepEqual(fs.readdirSync(outside), []);
});
test('existing skill symlink is rejected even with --force', (t) => {
  if (process.platform === 'win32') return t.skip('symlink creation may require privileges');
  const project = fixture(t);
  const outside = fixture(t);
  fs.mkdirSync(path.join(project, '.agents/skills'), { recursive: true });
  fs.symlinkSync(outside, path.join(project, '.agents/skills/vibe-os'), 'dir');
  const result = run(project, 'init', '--agent', 'codex', '--force');
  assert.equal(result.status, 2);
  assert.deepEqual(fs.readdirSync(outside), []);
});
test('doctor fails before initialization', (t) => {
  const project = fixture(t);
  assert.equal(run(project, 'doctor').status, 1);
});
test('bad and missing options return nonzero', (t) => {
  const project = fixture(t);
  assert.equal(run(project, 'init', '--agent', 'unknown').status, 2);
  assert.equal(run(project, 'init', '--project').status, 2);
  assert.equal(run(project, 'unknown').status, 2);
});
test('unsupported task commands identify native-Node boundary', (t) => {
  const project = fixture(t);
  const result = run(project, 'task', 'new feature');
  assert.equal(result.status, 2);
  assert.match(result.stderr, /Unknown command/);
});

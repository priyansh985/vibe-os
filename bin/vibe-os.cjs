#!/usr/bin/env node
'use strict';

// VIBE-OS native Node.js bootstrapper (no Python, network requests, or runtime dependencies).
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const PACKAGE = require('../package.json');
const SKILL = path.join(ROOT, 'vibeos', 'bundle', 'vibe-os');
const CURSOR = path.join(ROOT, 'vibeos', 'bundle', 'cursor-rule.mdc');
const AGENTS = new Set(['all', 'codex', 'claude', 'cursor']);

function help() {
  return `VIBE-OS ${PACKAGE.version} — Node.js skill installer

Usage:
  vibe-os init [--project PATH] [--agent all|codex|claude|cursor] [--force]
  vibe-os doctor [--project PATH]
  vibe-os --version
  vibe-os --help

Examples:
  npx --yes github:priyansh985/vibe-os init --agent all
  vibe-os init --project . --agent codex
  vibe-os doctor --project .

This Node.js CLI bootstraps project skills/rules and VIBE-OS state.
For task planning, assessment, verification, and reports, use the full Python CLI.
Files already present are preserved unless --force is specified.
`;
}

function parse(argv) {
  const [command = '--help', ...rest] = argv;
  if (['--help', '-h', 'help', '--version', '-v', 'version'].includes(command)) {
    if (rest.length) throw new Error(`Unexpected argument: ${rest[0]}`);
    return { command };
  }
  if (!['init', 'doctor'].includes(command)) throw new Error(`Unknown command: ${command}`);
  const opts = { command, project: '.', agent: 'all', force: false };
  for (let i = 0; i < rest.length; ++i) {
    const arg = rest[i];
    if (arg === '--force' && command === 'init') {
      opts.force = true;
    } else if (['--project', '--agent'].includes(arg)) {
      if (arg === '--agent' && command !== 'init') throw new Error('--agent only applies to init');
      if (i + 1 >= rest.length || rest[i + 1].startsWith('--')) throw new Error(`Missing value for ${arg}`);
      opts[arg.slice(2)] = rest[++i];
    } else {
      throw new Error(`Unknown option: ${arg}`);
    }
  }
  if (!AGENTS.has(opts.agent)) throw new Error(`Unsupported --agent: ${opts.agent}`);
  return opts;
}

function existingInfo(item) {
  try { return fs.lstatSync(item); }
  catch (error) { if (error.code === 'ENOENT') return null; throw error; }
}

function projectPath(value) {
  const resolved = path.resolve(value);
  const info = existingInfo(resolved);
  if (!info || !info.isDirectory()) throw new Error(`Project directory does not exist: ${resolved}`);
  return fs.realpathSync(resolved);
}

function safeRelative(root, relative) {
  const parts = relative.split('/');
  let current = root;
  for (const part of parts) {
    if (!part || part === '.' || part === '..') throw new Error(`Unsafe project path: ${relative}`);
    current = path.join(current, part);
    const stat = existingInfo(current);
    if (stat && stat.isSymbolicLink()) throw new Error(`Refusing symlink path: ${current}`);
  }
  return current;
}

function makeDir(root, relative) {
  const target = safeRelative(root, relative);
  const stat = existingInfo(target);
  if (stat) {
    if (!stat.isDirectory()) throw new Error(`Expected directory: ${target}`);
  } else {
    fs.mkdirSync(target, { recursive: true });
  }
  return target;
}

function writeFile(root, relative, content, force = false) {
  const target = safeRelative(root, relative);
  const found = existingInfo(target);
  if (found && !found.isFile()) throw new Error(`Expected regular file: ${target}`);
  if (found && !force) return false;
  const parent = relative.split('/').slice(0, -1).join('/');
  if (parent) makeDir(root, parent);
  fs.writeFileSync(target, content, { encoding: 'utf8', flag: force ? 'w' : 'wx' });
  return true;
}

function copySkill(root, dest, force) {
  const destination = safeRelative(root, dest);
  const found = existingInfo(destination);
  if (found && !found.isDirectory()) throw new Error(`Expected skill directory: ${destination}`);
  if (found && !force) return false;
  if (!fs.statSync(SKILL).isDirectory()) throw new Error('Bundled skill missing; reinstall VIBE-OS');
  makeDir(root, dest);
  const visit = (source, relative) => {
    for (const entry of fs.readdirSync(source, { withFileTypes: true })) {
      if (entry.isSymbolicLink()) throw new Error(`Bundled skill contains symlink: ${entry.name}`);
      const subpath = `${relative}/${entry.name}`;
      if (entry.isDirectory()) {
        makeDir(root, subpath);
        visit(path.join(source, entry.name), subpath);
      } else if (entry.isFile()) {
        writeFile(root, subpath, fs.readFileSync(path.join(source, entry.name), 'utf8'), force);
      } else {
        throw new Error(`Unexpected bundled file type: ${entry.name}`);
      }
    }
  };
  visit(SKILL, dest);
  return true;
}

function init(project, agent, force, print = console.log) {
  const root = projectPath(project);
  if (!fs.existsSync(path.join(SKILL, 'SKILL.md'))) throw new Error('Bundled SKILL.md missing');
  makeDir(root, '.vibeos');
  makeDir(root, '.vibeos/tasks');
  makeDir(root, '.vibeos/reports');
  const files = [
    ['.vibeos/config.json', `${JSON.stringify({ schema_version: 1, framework_version: PACKAGE.version, default_mode: 'auto', verification_is_explicit: true }, null, 2)}\n`],
    ['.vibeos/context.md', '# Project context\n\n## Purpose\n(TODO)\n\n## Stack and conventions\n(TODO)\n\n## Commands and environments\n(TODO)\n\n## Important constraints\n(TODO)\n\n## Decisions\n(Keep concise; use ADRs for major decisions.)\n'],
  ];
  for (const [file, contents] of files) {
    const changed = writeFile(root, file, contents, force);
    print(`${changed ? 'CREATED' : 'SKIPPED'} ${file}`);
  }
  for (const selected of agent === 'all' ? ['codex', 'claude', 'cursor'] : [agent]) {
    if (selected === 'cursor') {
      const file = '.cursor/rules/vibe-os.mdc';
      const changed = writeFile(root, file, fs.readFileSync(CURSOR, 'utf8'), force);
      print(`${changed ? 'INSTALLED' : 'SKIPPED'} ${file}`);
    } else {
      const dest = selected === 'codex' ? '.agents/skills/vibe-os' : '.claude/skills/vibe-os';
      const changed = copySkill(root, dest, force);
      print(`${changed ? 'INSTALLED' : 'SKIPPED'} ${dest}`);
    }
  }
  print('Next: fill .vibeos/context.md and ask your coding agent to use VIBE-OS.');
  print('Existing files were preserved unless --force was specified.');
  return 0;
}

function doctor(project, print = console.log) {
  const root = projectPath(project);
  const checks = [
    ['bundled skill', fs.existsSync(path.join(SKILL, 'SKILL.md'))],
    ['project state', fs.existsSync(safeRelative(root, '.vibeos/config.json'))],
    ['project context', fs.existsSync(safeRelative(root, '.vibeos/context.md'))],
    ['Codex skill', fs.existsSync(safeRelative(root, '.agents/skills/vibe-os/SKILL.md'))],
    ['Claude skill', fs.existsSync(safeRelative(root, '.claude/skills/vibe-os/SKILL.md'))],
    ['Cursor rule', fs.existsSync(safeRelative(root, '.cursor/rules/vibe-os.mdc'))],
  ];
  for (const [item, ok] of checks) print(`${ok ? 'OK' : '--'}  ${item}`);
  print('One supported agent integration is sufficient.');
  return checks[0][1] && checks[1][1] && checks.slice(3).some(([, ok]) => ok) ? 0 : 1;
}

function main(argv = process.argv.slice(2)) {
  try {
    const opts = parse(argv);
    if (['--help', '-h', 'help'].includes(opts.command)) { console.log(help()); return 0; }
    if (['--version', '-v', 'version'].includes(opts.command)) { console.log(PACKAGE.version); return 0; }
    if (opts.command === 'init') return init(opts.project, opts.agent, opts.force);
    return doctor(opts.project);
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    console.error('Run vibe-os --help for usage.');
    return 2;
  }
}

if (require.main === module) process.exitCode = main();
module.exports = { main, parse, init, doctor };

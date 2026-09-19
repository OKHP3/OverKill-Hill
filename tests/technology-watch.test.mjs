import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import test from 'node:test';

// Exercise the actual workflow script against mocked GitHub and filesystem APIs.
const workflow = readFileSync(new URL('../.github/workflows/technology-watch.yml', import.meta.url), 'utf8');
const source = workflow.split('          script: |\n')[1].split('\n').map(line => line.slice(12)).join('\n');
const runScript = new (Object.getPrototypeOf(async function () {}).constructor)(
  'require', 'github', 'context', 'core', source);
const marker = '<!-- technology-version-watch -->';

async function execute(report, existing = [], fileExists = true) {
  const calls = [];
  const github = {
    paginate: async () => existing,
    rest: {issues: {
      listForRepo() {},
      create: async args => calls.push({type: 'create', ...args}),
      update: async args => calls.push({type: 'update', ...args}),
    }},
  };
  await runScript(
    () => ({existsSync: () => fileExists, readFileSync: () => JSON.stringify(report)}),
    github, {repo: {owner: 'owner', repo: 'repo'}},
    {setFailed: message => calls.push({type: 'failed', message})});
  return calls;
}

const row = overrides => ({name: 'Node.js', current: '22.19.0', latest: '26.9.0',
  target: '24.21.0', target_status: 'UPDATE', owner: 'review', status: 'UPDATE', ...overrides});
const issue = body => ({number: 7, body, user: {login: 'github-actions[bot]'}});

test('creates one issue and leaves identical findings quiet', async () => {
  const report = {findings: [], technologies: [row({})]};
  const first = await execute(report);
  assert.equal(first.length, 1);
  assert.equal(first[0].type, 'create');
  assert.deepEqual(await execute(report, [issue(first[0].body)]), []);
});

test('does not treat a compliant LTS selector as needing Current migration', async () => {
  const calls = await execute({findings: [], technologies: [row({current: '24', target_status: 'TRACKING'})]},
    [issue(marker + '\nOld findings')]);
  assert.equal(calls.length, 1);
  assert.equal(calls[0].state, 'closed');
});

test('failed registry lookups keep issues open even for Dependabot-owned entries', async () => {
  const calls = await execute({findings: [], technologies: [row({owner: 'dependabot',
    target_status: undefined, status: 'UNKNOWN', error: 'timeout'})]}, [issue(marker)]);
  assert.equal(calls.length, 1);
  assert.equal(calls[0].type, 'update');
  assert.equal(calls[0].state, undefined);
  assert.match(calls[0].body, /Lookup failed/);
});

test('missing report cannot close an existing issue', async () => {
  const calls = await execute({}, [issue(marker)], false);
  assert.deepEqual(calls.map(c => c.type), ['failed']);
});

test('does not overwrite an unrelated user-created issue with the marker', async () => {
  const calls = await execute({findings: ['Node mismatch'], technologies: []},
    [{number: 9, body: marker, user: {login: 'someone'}}]);
  assert.equal(calls[0].type, 'create');
});

test('does not duplicate Dependabot or Mermaid update issues', async () => {
  const report = {findings: [], technologies: [row({owner: 'dependabot'}),
    row({owner: 'parent dependency'}), row({owner: 'Mermaid Version Watch'})]};
  assert.deepEqual(await execute(report), []);
});

test('an unrecorded authoring version remains actionable', async () => {
  const calls = await execute({findings: [], technologies: [row({name: 'FFmpeg',
    current: 'unrecorded', target_status: undefined, status: 'UNKNOWN'})]});
  assert.equal(calls[0].type, 'create');
  assert.match(calls[0].body, /FFmpeg: unrecorded/);
});

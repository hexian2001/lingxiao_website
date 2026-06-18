#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const args = process.argv.slice(2);

if (args.length === 0) {
  console.error('Usage: npm run astro -- <dev|build|preview|check> [args...]');
  process.exit(1);
}

let astroPackageJson;
try {
  astroPackageJson = require.resolve('astro/package.json');
} catch {
  console.error('Astro is not installed. Run `npm install` in the site directory first.');
  process.exit(1);
}

const astroCli = join(dirname(astroPackageJson), 'astro.js');
const result = spawnSync(process.execPath, [astroCli, ...args], {
  cwd: process.cwd(),
  env: process.env,
  stdio: 'inherit',
});

if (result.error) {
  console.error(result.error.message);
  process.exit(1);
}

process.exit(result.status ?? 1);

#!/usr/bin/env node

const { spawnSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

const SEVERITY = { info: 0, low: 1, moderate: 2, high: 3, critical: 4 };

function advisoryId(via) {
  const ghsa = via.url && via.url.match(/GHSA-[a-z0-9-]+/i);
  return ghsa ? `GHSA-${ghsa[0].slice(5).toLowerCase()}` : String(via.source || via.url || 'unknown');
}

function collectAdvisories(name, vulnerabilities, visited = new Set()) {
  if (visited.has(name)) return [];
  visited.add(name);

  const vulnerability = vulnerabilities[name];
  if (!vulnerability) return [];

  return vulnerability.via.flatMap((via) => {
    if (typeof via === 'string') {
      return collectAdvisories(via, vulnerabilities, visited);
    }
    return [advisoryId(via)];
  });
}

function isCurrentException(entry, packageName, now) {
  if (!entry || !Array.isArray(entry.packages) || !entry.packages.includes(packageName)) {
    return false;
  }
  if (!entry.reason || !entry.reviewBy) return false;

  const reviewDeadline = new Date(`${entry.reviewBy}T23:59:59.999Z`);
  return !Number.isNaN(reviewDeadline.getTime()) && now <= reviewDeadline;
}

function evaluateAudit(report, allowlist, now = new Date(), threshold = 'high') {
  const vulnerabilities = report.vulnerabilities || {};
  const result = { blocking: [], allowed: [] };

  for (const vulnerability of Object.values(vulnerabilities)) {
    if (SEVERITY[vulnerability.severity] < SEVERITY[threshold]) continue;

    const advisories = [...new Set(collectAdvisories(vulnerability.name, vulnerabilities))];
    const allowed =
      advisories.length > 0 &&
      advisories.every((id) =>
        isCurrentException(allowlist[id], vulnerability.name, now)
      );

    result[allowed ? 'allowed' : 'blocking'].push({
      name: vulnerability.name,
      severity: vulnerability.severity,
      advisories,
    });
  }

  return result;
}

function runNpmAudit(projectDirectory) {
  const audit = spawnSync('npm', ['audit', '--json'], {
    cwd: projectDirectory,
    encoding: 'utf8',
    maxBuffer: 32 * 1024 * 1024,
  });
  if (audit.error) throw audit.error;

  let report;
  try {
    report = JSON.parse(audit.stdout);
  } catch {
    throw new Error(`npm audit returned invalid JSON: ${audit.stderr.trim()}`);
  }
  if (report.error) {
    throw new Error(
      `npm audit failed: ${report.error.summary || report.error.code || report.message || audit.stderr.trim()}`
    );
  }
  return report;
}

function main() {
  const projectRoot = path.resolve(__dirname, '..');
  const allowlist = JSON.parse(
    fs.readFileSync(
      path.join(projectRoot, 'security/npm-audit-allowlist.json'),
      'utf8'
    )
  );
  const projects = ['.', 'sample-compass-ts', 'sample-compass-makecode'];
  let hasBlockingVulnerabilities = false;

  for (const project of projects) {
    const report = runNpmAudit(path.join(projectRoot, project));
    const result = evaluateAudit(report, allowlist);

    console.log(`\n${project}:`);
    for (const item of result.allowed) {
      console.log(
        `  ALLOWED ${item.severity} ${item.name} (${item.advisories.join(', ')})`
      );
    }
    for (const item of result.blocking) {
      hasBlockingVulnerabilities = true;
      console.error(
        `  BLOCKING ${item.severity} ${item.name} (${item.advisories.join(', ') || 'no advisory ID'})`
      );
    }
    if (result.allowed.length === 0 && result.blocking.length === 0) {
      console.log('  No high or critical vulnerabilities.');
    }
  }

  if (hasBlockingVulnerabilities) process.exitCode = 1;
}

if (require.main === module) main();

module.exports = { evaluateAudit };

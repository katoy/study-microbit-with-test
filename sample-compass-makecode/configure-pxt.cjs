const fs = require('node:fs');
const path = require('node:path');

const projectDirectory = __dirname;
const targetDirectory = path.join(projectDirectory, 'node_modules', 'pxt-microbit');
const targetConfig = path.join(targetDirectory, 'pxtarget.json');

if (!fs.existsSync(targetConfig)) {
  throw new Error('pxt-microbit is not installed; run npm install first');
}

const cliConfig = path.join(projectDirectory, 'node_modules', 'pxtcli.json');
const contents = `${JSON.stringify({ targetdir: 'pxt-microbit' }, null, 2)}\n`;

if (!fs.existsSync(cliConfig) || fs.readFileSync(cliConfig, 'utf8') !== contents) {
  fs.writeFileSync(cliConfig, contents, 'utf8');
}

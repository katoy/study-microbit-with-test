const fs = require('node:fs');
const path = require('node:path');

const projectDirectory = __dirname;
const cliConfig = path.join(projectDirectory, 'node_modules', 'pxtcli.json');
const contents = `${JSON.stringify({ targetdir: 'pxt-microbit' }, null, 2)}\n`;

// Create pxtcli.json even if pxt-microbit isn't fully installed yet
// (this can happen during npm audit fix or other package installation processes)
try {
  // Create node_modules directory if it doesn't exist
  const nodeModulesDir = path.join(projectDirectory, 'node_modules');
  if (!fs.existsSync(nodeModulesDir)) {
    fs.mkdirSync(nodeModulesDir, { recursive: true });
  }

  // Create pxtcli.json
  if (!fs.existsSync(cliConfig) || fs.readFileSync(cliConfig, 'utf8') !== contents) {
    fs.writeFileSync(cliConfig, contents, 'utf8');
  }

  // Create symlinks for pxt-microbit, pxt-core, and pxt-common-packages from root node_modules
  const rootNodeModules = path.join(projectDirectory, '..', '..', 'node_modules');
  const packagesToLink = ['pxt-microbit', 'pxt-core', 'pxt-common-packages'];

  for (const pkg of packagesToLink) {
    const srcPath = path.join(rootNodeModules, pkg);
    const destPath = path.join(nodeModulesDir, pkg);

    if (fs.existsSync(srcPath) && !fs.existsSync(destPath)) {
      fs.symlinkSync(srcPath, destPath, 'dir');
    }
  }
} catch (error) {
  // node_modules might not exist yet during initial install, that's okay
  if (error.code !== 'ENOENT' && error.code !== 'EEXIST') {
    // Log but don't fail on symlink errors
    console.warn('Warning: Could not create symlinks:', error.message);
  }
}

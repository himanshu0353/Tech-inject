#!/usr/bin/env node

import fs from 'fs';
import path from 'path';

const API_BASE = process.env.TECH_INJECT_API || 'http://127.0.0.1:8000/api';

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const slug = args[1];

  if (command !== 'add' || !slug) {
    console.log('\x1b[36mTech Inject Design Library CLI\x1b[0m');
    console.log('Usage: npx tech-inject add <component-slug>');
    console.log('Example: npx tech-inject add button');
    process.exit(0);
  }

  // Path traversal security check on slug
  if (slug.includes('/') || slug.includes('\\') || slug.includes('..')) {
    console.error('\x1b[31mError: Invalid component slug. Path traversal detected.\x1b[0m');
    process.exit(1);
  }

  console.log(`\x1b[34m[Tech Inject]\x1b[0m Fetching component package for "${slug}"...`);

  try {
    const res = await fetch(`${API_BASE}/components/${slug}/install`);
    
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'HTTP Error' }));
      if (res.status === 403) {
        console.error(`\x1b[31mError: ${err.detail || 'Premium access required to install this component.'}\x1b[0m`);
      } else if (res.status === 404) {
        console.error(`\x1b[31mError: Component "${slug}" not found or unpublished.\x1b[0m`);
      } else {
        console.error(`\x1b[31mError: ${err.detail || 'Download failed.'}\x1b[0m`);
      }
      process.exit(1);
    }

    const payload = await res.json();
    const { name, version, files, dependencies } = payload;

    const targetDir = path.resolve(process.cwd(), 'src', 'components');

    // Safe path enforcement: Target dir MUST be within current working dir!
    const cwd = process.cwd();
    if (!targetDir.startsWith(cwd)) {
      console.error('\x1b[31mError: Target directory resolves outside current workspace.\x1b[0m');
      process.exit(1);
    }

    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir, { recursive: true });
    }

    console.log(`\x1b[32m[Tech Inject]\x1b[0m Installing ${name} v${version} into ./src/components/...`);

    for (const [filename, content] of Object.entries(files)) {
      // Path traversal check on individual filenames
      if (filename.includes('..') || path.isAbsolute(filename)) {
        console.error(`\x1b[31mError: Unsafe filename "${filename}" rejected.\x1b[0m`);
        continue;
      }

      const filePath = path.join(targetDir, filename);

      // Verify final file path is inside targetDir
      if (!filePath.startsWith(targetDir)) {
        console.error(`\x1b[31mError: Unsafe filepath traversal rejected for "${filename}".\x1b[0m`);
        continue;
      }

      // Overwrite protection warning
      if (fs.existsSync(filePath)) {
        console.log(`\x1b[33m[Warning]\x1b[0m Overwriting existing file: ${filename}`);
      }

      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`  \x1b[32m+ Created\x1b[0m ./src/components/${filename}`);
    }

    if (dependencies && dependencies.length > 0) {
      console.log('\n\x1b[34m[Dependencies]\x1b[0m Required npm packages:');
      const depCmd = dependencies.map((d) => `${d.name}@${d.version}`).join(' ');
      console.log(`  npm install ${depCmd}`);
    }

    console.log(`\n\x1b[32mSuccess!\x1b[0m ${name} component installed successfully.`);

  } catch (err) {
    console.error(`\x1b[31mError connecting to Tech Inject backend API:\x1b[0m`, err.message);
    process.exit(1);
  }
}

main();

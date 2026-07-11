import { copyFileSync, existsSync } from 'node:fs'

const indexPath = 'dist/index.html'
const notFoundPath = 'dist/404.html'

if (!existsSync(indexPath)) {
  console.error(`Missing ${indexPath}. Run vite build first.`)
  process.exit(1)
}

copyFileSync(indexPath, notFoundPath)
console.log(`Copied ${indexPath} -> ${notFoundPath} (GitHub Pages SPA fallback)`)

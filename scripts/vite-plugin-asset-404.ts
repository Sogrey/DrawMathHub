import fs from 'node:fs'
import path from 'node:path'
import type { IncomingMessage, ServerResponse } from 'node:http'
import type { Plugin } from 'vite'

/** 带扩展名的 public 静态资源；不存在时返回 404，避免 SPA 回退为 index.html */
const STATIC_ASSET = /\.(json|mp4|webm|svg|png|jpe?g|gif|ico|woff2?|ttf|txt|xml)$/i

function resolvePublicFile(url: string, base: string, root: string): string {
  let pathname = url.split('?')[0]
  const normalizedBase = base.endsWith('/') ? base.slice(0, -1) : base
  if (normalizedBase !== '/' && pathname.startsWith(normalizedBase)) {
    pathname = pathname.slice(normalizedBase.length) || '/'
  }
  const relative = pathname.replace(/^\//, '')
  return path.join(root, 'public', decodeURIComponent(relative))
}

function asset404Middleware(
  req: IncomingMessage,
  res: ServerResponse,
  next: () => void,
  root: string,
  base: string,
): void {
  const url = req.url?.split('?')[0] ?? ''
  if (!STATIC_ASSET.test(url)) {
    next()
    return
  }

  const filePath = resolvePublicFile(url, base, root)
  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    next()
    return
  }

  res.statusCode = 404
  res.setHeader('Content-Type', 'text/plain; charset=utf-8')
  res.end('Not Found')
}

export function asset404Plugin(): Plugin {
  return {
    name: 'asset-404',
    configureServer(server) {
      const { root, base } = server.config
      server.middlewares.use((req, res, next) => {
        asset404Middleware(req, res, next, root, base)
      })
    },
    configurePreviewServer(server) {
      const { root, base } = server.config
      server.middlewares.use((req, res, next) => {
        asset404Middleware(req, res, next, root, base)
      })
    },
  }
}

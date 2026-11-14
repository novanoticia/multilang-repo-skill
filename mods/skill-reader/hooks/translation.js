const MAX_SOURCE_BYTES = 64 * 1024
const MAX_RESPONSE_BYTES = 512 * 1024
const MAX_OUTPUT_CHARS = 90000
const MARKER_FAMILY = '__NN_LITERAL_'
const CONTROL = /[\u0000-\u0008\u000b-\u001f\u007f-\u009f]/

// Conserva el token completo cuando parece técnico. Es deliberadamente más
// conservador que un analizador Markdown y evita repeticiones ambiguas.
function technicalToken(token) {
  if (token.includes(MARKER_FAMILY) || /[\/\\]/.test(token)
    || /\$\.[A-Za-z_$]|\bmcp__/.test(token)
    || /^--?[A-Za-z][A-Za-z0-9-]*(?:=.*)?$/.test(token)
    || /\.[A-Za-z]|\d\.\d/.test(token)) return true
  for (const word of token.match(/[A-Za-z][A-Za-z0-9_]*/g) || []) {
    if (word === 'Bash' || word === 'Read' || word.includes('_')
      || /^(?:Doc|R|D|P|T|C|S|G|M)\d+$/.test(word)
      || /^[A-Z][A-Z0-9_]+$/.test(word)) return true
    for (let i = 1; i < word.length; i += 1) {
      if (word[i] >= 'A' && word[i] <= 'Z') return true
    }
  }
  return false
}

function fail(code) {
  const messages = {
    source: 'El original no es un texto válido para preparar la traducción.',
    target: 'Esta versión solo admite español como idioma de destino.',
    source_limit: 'El original supera el límite de 64 KiB.',
    fragment_limit: 'El documento genera demasiados fragmentos para preparar la traducción.',
    response_limit: 'La respuesta supera el límite permitido.',
    response_json: 'La respuesta no es el JSON esperado.',
    response_structure: 'La respuesta no contiene todos los segmentos esperados.',
    markers: 'La respuesta no conserva los fragmentos protegidos.',
    output: 'El texto reconstruido supera los límites o contiene controles no admitidos.',
  }
  const error = new Error(messages[code])
  error.name = 'TranslationError'
  error.code = code
  throw error
}

function validControls(text) {
  return !CONTROL.test(text.replace(/\r\n/g, '\n'))
}

function isRecord(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
}

function bodyOf(line) {
  return line.endsWith('\n') ? line.slice(0, line.endsWith('\r\n') ? -2 : -1) : line
}

// En citas y listas se conserva el resto del documento para evitar adivinar
// dónde termina un contenedor Markdown anidado.
function containerFence(body) {
  let cursor = 0
  while (cursor < body.length && /\s/.test(body[cursor])) cursor += 1
  let container = false
  while (body[cursor] === '>') {
    container = true
    cursor += 1
    while (cursor < body.length && /\s/.test(body[cursor])) cursor += 1
  }
  let rest = body.slice(cursor)
  const list = /^(?:[-+*]|\d+[.)])[ \t]+/.exec(rest)
  if (list) {
    container = true
    rest = rest.slice(list[0].length)
  }
  return container && /^(?:`{3,}|~{3,})/.test(rest)
}

export function prepareTranslation(source, target = 'es') {
  if (typeof source !== 'string' || !validControls(source)) fail('source')
  if (target !== 'es') fail('target')
  const encoder = new TextEncoder()
  if (source.length > MAX_SOURCE_BYTES || encoder.encode(source).length > MAX_SOURCE_BYTES) fail('source_limit')

  const usedSalts = new Set()
  for (const match of source.matchAll(/__NN_LITERAL_(\d+)_/g)) usedSalts.add(match[1])
  let salt = 0
  while (usedSalts.has(String(salt))) salt += 1
  const prefix = MARKER_FAMILY + salt + '_'
  const literals = new Map()
  const parts = []
  const segments = []
  const expected = new Map()

  const hide = literal => {
    const marker = prefix + literals.size + '__'
    literals.set(marker, literal)
    return marker
  }
  const maskText = text => text.replace(/[^\s]+/g, token => technicalToken(token) ? hide(token) : token)
  const maskInline = text => {
    const chunks = []
    let cursor = 0
    while (cursor < text.length) {
      const start = text.indexOf('`', cursor)
      if (start === -1) { chunks.push(maskText(text.slice(cursor))); break }
      chunks.push(maskText(text.slice(cursor, start)))
      let after = start
      while (text[after] === '`') after += 1
      const width = after - start
      let search = after
      let end = -1
      while (search < text.length) {
        const candidate = text.indexOf('`', search)
        if (candidate === -1) break
        let runEnd = candidate
        while (text[runEnd] === '`') runEnd += 1
        if (runEnd - candidate === width) { end = runEnd; break }
        search = runEnd
      }
      // Un delimitador sin pareja conserva literalmente el texto restante.
      if (end === -1) { chunks.push(hide(text.slice(start))); break }
      chunks.push(hide(text.slice(start, end)))
      cursor = end
    }
    return chunks.join('')
  }
  const fixed = text => { if (text) parts.push({ literal: text }) }
  const prose = raw => {
    let start = 0
    let end = raw.length
    while (start < end && /\s/.test(raw[start])) start += 1
    while (end > start && /\s/.test(raw[end - 1])) end -= 1
    const masked = maskInline(raw.slice(start, end))
    const markers = masked.match(/__NN_LITERAL_\d+_\d+__/g) || []
    const remainder = masked.replace(/__NN_LITERAL_\d+_\d+__/g, '')
    if (!/\p{L}/u.test(remainder)) { fixed(raw); return }
    fixed(raw.slice(0, start))
    const id = 's' + segments.length
    segments.push({ id, text: masked })
    expected.set(id, new Set(markers))
    parts.push({ id })
    fixed(raw.slice(end))
  }

  const lines = source.match(/[^\n]*\n|[^\n]+$/g) || []
  let pending = []
  const flush = () => { if (pending.length) prose(pending.join('')); pending = [] }
  let index = 0
  if (lines.length && /^\ufeff?---[ \t]*$/.test(bodyOf(lines[0]))) {
    let end = 1
    while (end < lines.length && !/^(?:---|\.\.\.)[ \t]*$/.test(bodyOf(lines[end]))) end += 1
    if (end < lines.length) end += 1
    fixed(lines.slice(0, end).join(''))
    index = end
  }
  while (index < lines.length) {
    const body = bodyOf(lines[index])
    if (containerFence(body)) {
      flush()
      fixed(lines.slice(index).join(''))
      index = lines.length
    } else if (body.includes('<!--')) {
      flush()
      let end = index
      let position = body.indexOf('<!--') + 4
      while (end < lines.length) {
        const closing = lines[end].indexOf('-->', position)
        if (closing === -1) { end += 1; position = 0; continue }
        const opening = lines[end].indexOf('<!--', closing + 3)
        if (opening === -1) { end += 1; break }
        position = opening + 4
      }
      fixed(lines.slice(index, end).join(''))
      index = end
    } else {
      const fence = /^ {0,3}(`{3,}|~{3,})/.exec(body)
      if (fence) {
        flush()
        const close = new RegExp('^ {0,3}' + fence[1][0] + '{' + fence[1].length + ',}[ \t]*$')
        let end = index + 1
        while (end < lines.length && !close.test(bodyOf(lines[end]))) end += 1
        if (end < lines.length) end += 1
        fixed(lines.slice(index, end).join(''))
        index = end
      } else if (/^(?: {4}|\t)/.test(body) || !body.trim() || /^ {0,3}\[[^\]]+\]:/.test(body)) {
        // La sangría también puede ser prosa de una lista: se conserva a propósito.
        flush()
        fixed(lines[index++])
      } else {
        pending.push(lines[index++])
      }
    }
  }
  flush()

  const payload = JSON.stringify({ target, segments })
  if (payload.length > MAX_RESPONSE_BYTES || encoder.encode(payload).length > MAX_RESPONSE_BYTES) fail('fragment_limit')
  const restore = responseText => {
    if (typeof responseText !== 'string') fail('response_json')
    if (responseText.length > MAX_RESPONSE_BYTES || encoder.encode(responseText).length > MAX_RESPONSE_BYTES) fail('response_limit')
    let response
    try { response = JSON.parse(responseText) } catch { fail('response_json') }
    if (!isRecord(response) || Object.keys(response).length !== 1 || !Array.isArray(response.segments)
      || response.segments.length !== segments.length) fail('response_structure')
    const restored = new Map()
    for (const segment of response.segments) {
      if (!isRecord(segment) || Object.keys(segment).length !== 2
        || !Object.hasOwn(segment, 'id') || !Object.hasOwn(segment, 'text')
        || typeof segment.id !== 'string' || typeof segment.text !== 'string'
        || !segment.text.trim() || !expected.has(segment.id) || restored.has(segment.id)) fail('response_structure')
      const allowed = expected.get(segment.id)
      const seen = new Set()
      const markerAt = /__NN_LITERAL_\d+_\d+__/y
      let cursor = 0
      while (cursor < segment.text.length) {
        const start = segment.text.indexOf(MARKER_FAMILY, cursor)
        if (start === -1) break
        markerAt.lastIndex = start
        const marker = markerAt.exec(segment.text)
        if (!marker || !allowed.has(marker[0]) || seen.has(marker[0])) fail('markers')
        seen.add(marker[0])
        cursor = start + marker[0].length
      }
      if (seen.size !== allowed.size) fail('markers')
      restored.set(segment.id, segment.text.replace(/__NN_LITERAL_\d+_\d+__/g, marker => literals.get(marker)))
    }
    const output = parts.map(part => Object.hasOwn(part, 'literal') ? part.literal : restored.get(part.id)).join('')
    if (output.length > MAX_OUTPUT_CHARS || !validControls(output)) fail('output')
    return output
  }
  return Object.freeze({ payload, segmentCount: segments.length, restore })
}

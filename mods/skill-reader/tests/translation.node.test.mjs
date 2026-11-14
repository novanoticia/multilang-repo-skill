import test from 'node:test'
import assert from 'node:assert/strict'
import { prepareTranslation } from '../hooks/translation.js'

const requestOf = plan => JSON.parse(plan.payload)
const replyOf = plan => ({ segments: requestOf(plan).segments.map(segment => ({ ...segment })) })
const identityOf = plan => plan.restore(JSON.stringify(replyOf(plan)))
const markersOf = text => text.match(/__NN_LITERAL_\d+_\d+__/g) ?? []

test('la identidad conserva CRLF, espacios y el documento original', () => {
  const source = '\uFEFF---\r\nname: prueba\r\n---\r\n\r\n# Encabezado\r\n\r\n  Lee `echo dato` con cuidado.  \r\n\r\n'
  const plan = prepareTranslation(source)
  assert.ok(Object.isFrozen(plan))
  assert.equal(requestOf(plan).target, 'es')
  assert.equal(plan.segmentCount, requestOf(plan).segments.length)
  assert.equal(identityOf(plan), source)
})

test('el payload serializable excluye metadatos, código y comentarios protegidos', () => {
  const source = [
    '---',
    'name: metadato reservado de prueba',
    '---',
    '',
    'Lee `comando opaco ficticio` con cuidado.',
    '',
    '```sh',
    'echo bloque reservado de prueba',
    '```',
    '',
    '<!-- comentario reservado de prueba -->',
    'Texto traducible.',
  ].join('\n')
  const plan = prepareTranslation(source)
  for (const literal of ['metadato reservado de prueba', 'comando opaco ficticio', 'bloque reservado de prueba', 'comentario reservado de prueba']) {
    assert.ok(!plan.payload.includes(literal), literal)
    assert.ok(!JSON.stringify(plan).includes(literal), literal)
  }
  assert.ok(plan.segmentCount > 0)
  assert.equal(identityOf(plan), source)
})

test('un documento compuesto solo por metadatos y código no necesita segmentos', () => {
  const source = '---\nname: prueba\n---\n\n```sh\necho dato\n```\n\n'
  const plan = prepareTranslation(source)
  assert.equal(plan.segmentCount, 0)
  assert.deepEqual(requestOf(plan).segments, [])
  assert.equal(plan.restore('{"segments":[]}'), source)
})

test('los fences de distinta longitud, carácter o sin cierre conservan su código', () => {
  const blocks = [
    '````sh\necho contenido reservado de prueba\n```\ncontenido opaco tras cierre corto\n~~~\n````\n',
    '~~~~sh\necho contenido reservado de prueba\n~~~\ncontenido opaco tras cierre corto\n```\n~~~~\n',
    '```sh\necho contenido reservado de prueba\n',
    '```sh\necho dato\n```t\ncontenido reservado de prueba\n```\n',
    '```sh\necho dato\n```\\\ncontenido reservado de prueba\n```\n',
  ]
  for (const block of blocks) {
    const source = 'Texto anterior.\n\n' + block
    const plan = prepareTranslation(source)
    assert.ok(!plan.payload.includes('contenido reservado de prueba'))
    assert.ok(!plan.payload.includes('contenido opaco tras cierre corto'))
    assert.equal(identityOf(plan), source)
  }
  const tabSource = '```sh\necho dato\n```\t\n\nTexto posterior traducible.\n'
  const tabPlan = prepareTranslation(tabSource)
  assert.ok(tabPlan.payload.includes('Texto posterior traducible.'))
  assert.equal(identityOf(tabPlan), tabSource)
})

test('los bloques de código en citas, listas y sangrías permanecen literales', () => {
  const blocks = [
    '> ```sh\n> echo contenido reservado de prueba\n> ```\n',
    '- ```sh\n  echo contenido reservado de prueba\n  ```\n',
    '    echo contenido reservado de prueba\n',
    '\techo contenido reservado de prueba\n',
  ]
  for (const block of blocks) {
    const source = 'Texto anterior.\n\n' + block + '\nTexto posterior.\n'
    const plan = prepareTranslation(source)
    assert.ok(!plan.payload.includes('contenido reservado de prueba'))
    assert.equal(identityOf(plan), source)
  }
})

test('los spans de código admiten varios backticks y más de una línea', () => {
  const source = 'Usa ``comando `opaco`\ncontinuación ficticia`` con cuidado.\n'
  const plan = prepareTranslation(source)
  assert.ok(!plan.payload.includes('comando `opaco`'))
  assert.ok(!plan.payload.includes('continuación ficticia'))
  assert.equal(identityOf(plan), source)
})

test('los comentarios HTML completos no se envían como prosa', () => {
  for (const prefix of ['Antes ', 'Texto --> antes ', '<!-- comentario previo --> antes ']) {
    const source = prefix + '<!-- comentario reservado de prueba\nsegunda línea --> después.\n'
    const plan = prepareTranslation(source)
    assert.ok(!plan.payload.includes('comentario reservado de prueba'))
    assert.ok(!plan.payload.includes('segunda línea'))
    assert.equal(identityOf(plan), source)
  }
})

test('URLs, rutas y nombres técnicos sobreviven aunque cambie toda la prosa', () => {
  const source = 'Consulta https://example.invalid/a_(b)?q=1 y `carpeta con espacios/SKILL.md` o docs/reference.md. Usa Bash y Read con mcp__demo__ticket, $.fs.read, someMethodName, PluginState, API_KEY, R17 y Doc1.\n'
  const plan = prepareTranslation(source)
  const literals = ['https://example.invalid/a_(b)?q=1', '`carpeta con espacios/SKILL.md`', 'docs/reference.md', 'Bash', 'Read', 'mcp__demo__ticket', '$.fs.read', 'someMethodName', 'PluginState', 'API_KEY', 'R17', 'Doc1']
  for (const literal of literals) {
    assert.ok(!plan.payload.includes(literal), literal)
  }
  assert.equal(identityOf(plan), source)
  const reply = replyOf(plan)
  for (const segment of reply.segments) {
    segment.text = segment.text.split(/(__NN_LITERAL_\d+_\d+__)/g)
      .map(part => /^__NN_LITERAL_\d+_\d+__$/.test(part) ? part : part ? 'prosa traducida' : '')
      .join('')
  }
  const translated = plan.restore(JSON.stringify(reply))
  for (const literal of literals) assert.ok(translated.includes(literal), literal)
})

test('un prefijo que ya está en el original no colisiona con los marcadores nuevos', () => {
  const first = prepareTranslation('Use `echo privado` now.')
  const existing = markersOf(requestOf(first).segments[0].text)[0]
  assert.ok(existing)
  const source = 'Conserva `' + existing + '`.\n\nUse `echo privado` now.'
  const plan = prepareTranslation(source)
  const generated = requestOf(plan).segments.flatMap(segment => markersOf(segment.text))
  assert.ok(generated.length >= 2)
  assert.ok(!generated.includes(existing))
  assert.equal(identityOf(plan), source)
})

test('la respuesta puede reordenar IDs, pero el documento conserva el orden original', () => {
  const source = 'First `echo alpha`.\n\nSecond `echo beta`.\n'
  const plan = prepareTranslation(source)
  const reply = replyOf(plan)
  assert.equal(reply.segments.length, 2)
  reply.segments = reply.segments.map(segment => ({
    ...segment,
    text: segment.text.replace('First', 'Primero').replace('Second', 'Segundo'),
  })).reverse()
  assert.equal(plan.restore(JSON.stringify(reply)), 'Primero `echo alpha`.\n\nSegundo `echo beta`.\n')
})

test('se rechazan envoltorios, JSON inválido y claves raíz adicionales', () => {
  const plan = prepareTranslation('Texto traducible.')
  const good = JSON.stringify(replyOf(plan))
  for (const response of ['no es JSON', 'null', '[]', '{}', '```json\n' + good + '\n```', 'Explicación\n' + good, JSON.stringify({ ...replyOf(plan), target: 'es' }), '{"segments":null}']) {
    assert.throws(() => plan.restore(response), undefined, response)
  }
})

test('se rechazan IDs ausentes, duplicados, desconocidos y segmentos mal formados', () => {
  const plan = prepareTranslation('Primera frase.\n\nSegunda frase.')
  const { segments } = replyOf(plan)
  assert.equal(segments.length, 2)
  const invalid = [
    [],
    segments.slice(1),
    [segments[0], segments[0]],
    [segments[0], { ...segments[1], id: 'desconocido' }],
    [segments[0], { ...segments[1], id: '__proto__' }],
    [segments[0], { ...segments[1], id: 1 }],
    [segments[0], { ...segments[1], text: null }],
    [segments[0], { ...segments[1], text: '   ' }],
    [segments[0], { ...segments[1], extra: true }],
    [segments[0], null],
    [...segments, { id: 'extra', text: 'sobrante' }],
  ]
  for (const candidate of invalid) {
    assert.throws(() => plan.restore(JSON.stringify({ segments: candidate })))
  }
})

test('se rechazan marcadores ausentes, duplicados, desconocidos o incompletos', () => {
  const plan = prepareTranslation('Use `echo privado` now.')
  const { segments } = replyOf(plan)
  const marker = markersOf(segments[0].text)[0]
  assert.ok(marker)
  const prefix = marker.replace(/\d+__$/, '')
  const invalid = [
    segments[0].text.replace(marker, ''),
    segments[0].text.replace(marker, marker + marker),
    segments[0].text.replace(marker, prefix + '999999__'),
    segments[0].text.replace(marker, marker.slice(0, -1)),
    segments[0].text.replace(marker, prefix + 'roto'),
  ]
  for (const text of invalid) {
    assert.throws(() => plan.restore(JSON.stringify({ segments: [{ ...segments[0], text }] })))
  }
})

test('intercambiar marcadores entre segmentos se rechaza aunque el inventario global coincida', () => {
  const plan = prepareTranslation('First `echo alpha`.\n\nSecond `echo beta`.')
  const reply = replyOf(plan)
  assert.equal(reply.segments.length, 2)
  const first = markersOf(reply.segments[0].text)[0]
  const second = markersOf(reply.segments[1].text)[0]
  assert.ok(first && second && first !== second)
  reply.segments[0].text = reply.segments[0].text.replace(first, second)
  reply.segments[1].text = reply.segments[1].text.replace(second, first)
  assert.throws(() => plan.restore(JSON.stringify(reply)))
})

test('el límite de entrada se cuenta en bytes UTF-8', () => {
  for (const source of ['a'.repeat(64 * 1024), 'ñ'.repeat(32 * 1024)]) {
    const plan = prepareTranslation(source)
    assert.equal(identityOf(plan), source)
  }
  assert.throws(() => prepareTranslation('a'.repeat(64 * 1024 + 1)))
  assert.throws(() => prepareTranslation('ñ'.repeat(32 * 1024 + 1)))
  const manyLiterals = 'Texto ' + 'R1 '.repeat(21000)
  assert.ok(Buffer.byteLength(manyLiterals) <= 64 * 1024)
  const manyPlan = prepareTranslation(manyLiterals)
  assert.ok(Buffer.byteLength(JSON.stringify(replyOf(manyPlan))) <= 512 * 1024)
  assert.equal(identityOf(manyPlan), manyLiterals)
  const manySegments = 'A\n\n'.repeat(21000)
  assert.ok(Buffer.byteLength(manySegments) <= 64 * 1024)
  assert.throws(() => prepareTranslation(manySegments), { name: 'TranslationError', code: 'fragment_limit' })
})

test('se limita el tamaño de la respuesta antes de aceptar JSON', () => {
  const plan = prepareTranslation('texto')
  const good = JSON.stringify(replyOf(plan))
  const boundary = ' '.repeat(512 * 1024 - Buffer.byteLength(good)) + good
  assert.equal(plan.restore(boundary), 'texto')
  assert.throws(() => plan.restore(' ' + boundary))
})

test('la reconstrucción no puede superar los 90000 caracteres', () => {
  const plan = prepareTranslation('texto')
  const segment = requestOf(plan).segments[0]
  assert.equal(plan.restore(JSON.stringify({ segments: [{ ...segment, text: 'a'.repeat(90000) }] })).length, 90000)
  assert.throws(() => plan.restore(JSON.stringify({ segments: [{ ...segment, text: 'a'.repeat(90001) }] })))
})

test('se rechazan controles no admitidos en entrada y respuesta', () => {
  for (const control of ['\u0000', '\u001b', '\u007f', '\u009b', '\r']) {
    assert.throws(() => prepareTranslation('texto' + control))
    const plan = prepareTranslation('texto')
    const segment = requestOf(plan).segments[0]
    assert.throws(() => plan.restore(JSON.stringify({ segments: [{ ...segment, text: 'texto' + control }] })))
  }
  const source = 'uno\tdos\r\n'
  assert.equal(identityOf(prepareTranslation(source)), source)
})

test('solo se admite español y una entrada de texto; el vacío no requiere segmentos', () => {
  assert.throws(() => prepareTranslation('texto', 'en'))
  assert.throws(() => prepareTranslation('texto', null))
  for (const value of [null, undefined, 1, {}, []]) assert.throws(() => prepareTranslation(value))
  const plan = prepareTranslation('')
  assert.equal(plan.segmentCount, 0)
  assert.equal(identityOf(plan), '')
})

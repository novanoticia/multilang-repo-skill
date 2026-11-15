import { expect, test } from 'claude-code/testing'

const PANE = {
  plugin: 'novanoticia-lector-skills',
  component: 'Pane',
  requestId: 'skill-reader',
  surface: 'terminal',
  props: {
    title: 'Lector de skills',
    isFocused: true,
    bodyColumns: 60,
    placement: 'inline',
    scroll: { offset: 0, bodyRows: 20 },
    view: {},
  },
} as const

const CONTENT = [
  '---',
  'name: metadato-reservado-ficticio',
  '---',
  '',
  'Please follow these instructions.',
  '',
  'Use `printf "dato fijo"` with Bash.',
  '',
  '```sh',
  'printf "bloque fijo"',
  '```',
].join('\n')

const TRANSLATED = CONTENT
  .replace('Please follow these instructions.', 'Sigue estas instrucciones.')
  .replace('Use ', 'Usa ')
  .replace(' with ', ' con ')

const FILE = { kind: 'file', size: 1024, mtimeMs: 0, isLink: false } as const
const USAGE = {
  input_tokens: 10,
  output_tokens: 8,
  cache_read_input_tokens: 0,
  cache_creation_input_tokens: 0,
}

function answerFor(prompt: string) {
  const request = JSON.parse(prompt)
  return {
    isAnswered: true as const,
    text: JSON.stringify({
      segments: request.segments.map((segment: { id: string, text: string }) => ({
        ...segment,
        text: segment.text
          .replace('Please follow these instructions.', 'Sigue estas instrucciones.')
          .replace('Use ', 'Usa ')
          .replace(' with ', ' con '),
      })),
    }),
    usage: USAGE,
  }
}

function deferred<T>() {
  let resolve!: (value: T) => void
  const promise = new Promise<T>(done => { resolve = done })
  return { promise, resolve }
}

test('abrir, cargar, elegir idioma y redibujar no llaman al modelo', async ($, on) => {
  let models = 0
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('fs.stat', () => ({ value: FILE }))
  on('fs.read', () => ({ value: CONTENT }))
  on('model.complete', () => { models += 1; return { deny: 'No debe traducir automáticamente.' } })

  expect(await $.command.run({ command: 'skill-reader', args: '' })).toEqual({})
  const ui = await $.ui.mount(PANE)
  expect(models).toBe(0)
  await ui.input({ key: 'skill-path', text: 'elegida/SKILL.md', kind: 'change' })
  await ui.press({ key: 'load-original' })
  await ui.select({ key: 'target-language', value: 'es' })
  await ui.redraw()
  expect(models).toBe(0)
  expect(await ui.find({ type: 'Text', text: /Haiku/i })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /consumo|coste|uso/i })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: CONTENT })).toBeDefined()
  await ui.unmount()
})

test('Traducir realiza una petición preparada y conserva los literales del original', async ($, on) => {
  let models = 0
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('fs.stat', () => ({ value: FILE }))
  on('fs.read', () => ({ value: CONTENT }))
  on('model.complete', ($, e) => {
    models += 1
    expect(e.model).toBe('haiku')
    expect(e.maxTokens).toBe(32000)
    expect(e.timeoutMs).toBe(120000)
    expect(typeof e.system).toBe('string')
    const request = JSON.parse(e.prompt)
    expect(Object.keys(request).sort()).toEqual(['segments', 'target'])
    expect(request.target).toBe('es')
    for (const literal of ['metadato-reservado-ficticio', 'printf', 'Bash', 'elegida/SKILL.md']) {
      expect(e.prompt.includes(literal)).toBe(false)
    }
    return { value: answerFor(e.prompt) }
  })

  await $.command.run({ command: 'skill-reader', args: '' })
  const ui = await $.ui.mount(PANE)
  await ui.input({ key: 'skill-path', text: 'elegida/SKILL.md', kind: 'change' })
  await ui.press({ key: 'load-original' })
  await ui.press({ key: 'translate' })
  expect(models).toBe(1)
  expect(await ui.find({ type: 'Text', text: 'Completado' })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: TRANSLATED })).toBeDefined()
  await ui.press({ key: 'view-original' })
  expect(await ui.find({ type: 'Text', text: CONTENT })).toBeDefined()
  await ui.press({ key: 'view-translation' })
  expect(await ui.find({ type: 'Text', text: TRANSLATED })).toBeDefined()
  expect(models).toBe(1)
  await ui.unmount()
})

test('los resultados sin respuesta muestran error y conservan el original sin reintentar', async ($, on) => {
  const failures = [
    { isAnswered: false, reason: 'api-error', status: 429, error: 'rate_limit', usage: USAGE },
    { isAnswered: false, reason: 'empty-reply', usage: USAGE },
    { isAnswered: false, reason: 'aborted', usage: USAGE },
  ] as const
  let result: typeof failures[number] = failures[0]
  let models = 0
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('fs.stat', () => ({ value: FILE }))
  on('fs.read', () => ({ value: CONTENT }))
  on('model.complete', () => { models += 1; return { value: result } })

  await $.command.run({ command: 'skill-reader', args: '' })
  const ui = await $.ui.mount(PANE)
  await ui.input({ key: 'skill-path', text: 'elegida/SKILL.md', kind: 'change' })
  await ui.press({ key: 'load-original' })
  for (let index = 0; index < failures.length; index += 1) {
    result = failures[index]!
    await ui.press({ key: 'translate' })
    expect(models).toBe(index + 1)
    expect(await ui.find({ type: 'Text', text: /^Error:/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: CONTENT })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: TRANSLATED })).toBeUndefined()
  }
  await ui.unmount()
})

test('una respuesta inválida no muestra traducción parcial ni altera el original', async ($, on) => {
  let invalid = 'json'
  let models = 0
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('fs.stat', () => ({ value: FILE }))
  on('fs.read', () => ({ value: CONTENT }))
  on('model.complete', ($, e) => {
    models += 1
    const answer = answerFor(e.prompt)
    if (invalid === 'json') answer.text = 'TRADUCCION_PARCIAL_NO_MOSTRAR'
    else if (invalid === 'segments') answer.text = '{"segments":[]}'
    else {
      const response = JSON.parse(answer.text)
      const segment = response.segments.find((part: { text: string }) => part.text.includes('__NN_LITERAL_'))
      segment.text = segment.text.replace(/__NN_LITERAL_\d+_\d+__/, '')
      answer.text = JSON.stringify(response)
    }
    return { value: answer }
  })

  await $.command.run({ command: 'skill-reader', args: '' })
  const ui = await $.ui.mount(PANE)
  await ui.input({ key: 'skill-path', text: 'elegida/SKILL.md', kind: 'change' })
  await ui.press({ key: 'load-original' })
  for (const variant of ['json', 'segments', 'markers']) {
    invalid = variant
    await ui.press({ key: 'translate' })
    expect(await ui.find({ type: 'Text', text: /^Error:/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: CONTENT })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: TRANSLATED })).toBeUndefined()
    expect(await ui.find({ type: 'Text', text: /TRADUCCION_PARCIAL_NO_MOSTRAR/ })).toBeUndefined()
  }
  expect(models).toBe(3)
  await ui.unmount()
})

test('cerrar durante una traducción descarta su respuesta y no ofrece otra petición en curso', async ($, on) => {
  const started = deferred<void>()
  const pending = deferred<void>()
  const closed = deferred<void>()
  let models = 0
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('fs.stat', () => ({ value: FILE }))
  on('fs.read', () => ({ value: CONTENT }))
  on('ui.close', () => { closed.resolve(); return { value: undefined } })
  on('model.complete', async ($, e) => {
    models += 1
    const answer = answerFor(e.prompt)
    started.resolve()
    // La respuesta simulada ignora el aborto para ejercitar el descarte tardío.
    await pending.promise
    return { value: answer }
  })

  await $.command.run({ command: 'skill-reader', args: '' })
  const ui = await $.ui.mount(PANE)
  await ui.input({ key: 'skill-path', text: 'elegida/SKILL.md', kind: 'change' })
  await ui.press({ key: 'load-original' })
  const translating = ui.press({ key: 'translate' })
  await started.promise
  expect(await ui.find({ key: 'translate' })).toBeUndefined()
  const closing = ui.press({ key: 'close' })
  await closed.promise
  pending.resolve()
  await Promise.all([translating, closing])
  expect(models).toBe(1)
  expect(await ui.find({ type: 'Text', text: TRANSLATED })).toBeUndefined()
  expect(await ui.find({ type: 'Text', text: 'Completado' })).toBeUndefined()
  await ui.unmount()
})

test('cambiar la ruta invalida una traducción pendiente sin traducir la nueva selección', async ($, on) => {
  const started = deferred<void>()
  const pending = deferred<void>()
  const edited = deferred<void>()
  let models = 0
  let reads = 0
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('fs.stat', () => ({ value: FILE }))
  on('fs.read', () => { reads += 1; return { value: CONTENT } })
  on('ui.input', {
    plugin: 'novanoticia-lector-skills',
    element: 'skill-path',
  }, async ($, e, next) => {
    const result = await next(e)
    if (e.kind === 'change' && e.value === 'otra/SKILL.md') edited.resolve()
    return result
  })
  on('model.complete', async ($, e) => {
    models += 1
    const answer = answerFor(e.prompt)
    started.resolve()
    await pending.promise
    return { value: answer }
  })

  await $.command.run({ command: 'skill-reader', args: '' })
  const ui = await $.ui.mount(PANE)
  await ui.input({ key: 'skill-path', text: 'elegida/SKILL.md', kind: 'change' })
  await ui.press({ key: 'load-original' })
  const translating = ui.press({ key: 'translate' })
  await started.promise
  const editing = ui.input({ key: 'skill-path', text: 'otra/SKILL.md', kind: 'change' })
  await edited.promise
  pending.resolve()
  await Promise.all([translating, editing])
  expect(models).toBe(1)
  expect(reads).toBe(1)
  expect(await ui.find({ type: 'Text', text: TRANSLATED })).toBeUndefined()
  expect(await ui.find({ type: 'Text', text: CONTENT })).toBeUndefined()
  await ui.unmount()
})

test('terminar la sesión descarta una traducción pendiente', async ($, on) => {
  const started = deferred<void>()
  const pending = deferred<void>()
  const ended = deferred<void>()
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('fs.stat', () => ({ value: FILE }))
  on('fs.read', () => ({ value: CONTENT }))
  on('session.end', ($, e) => { ended.resolve(); return { sessionId: e.sessionId } })
  on('model.complete', async ($, e) => {
    const answer = answerFor(e.prompt)
    started.resolve()
    await pending.promise
    return { value: answer }
  })

  await $.command.run({ command: 'skill-reader', args: '' })
  const ui = await $.ui.mount(PANE)
  await ui.input({ key: 'skill-path', text: 'elegida/SKILL.md', kind: 'change' })
  await ui.press({ key: 'load-original' })
  const translating = ui.press({ key: 'translate' })
  await started.promise
  const ending = $.session.end({ reason: 'clear', sessionId: 'sesion-de-prueba', resume: { id: 'sesion-de-prueba' } })
  await ended.promise
  pending.resolve()
  await Promise.all([translating, ending])
  expect(await ui.find({ type: 'Text', text: TRANSLATED })).toBeUndefined()
  expect(await ui.find({ type: 'Text', text: CONTENT })).toBeUndefined()
  await ui.unmount()
})

test('un archivo sin prosa traducible se conserva sin llamar al modelo', async ($, on) => {
  const content = '---\nname: prueba\n---\n\n```sh\necho dato\n```\n'
  let models = 0
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('fs.stat', () => ({ value: FILE }))
  on('fs.read', () => ({ value: content }))
  on('model.complete', () => { models += 1; return { deny: 'No hay prosa que traducir.' } })

  await $.command.run({ command: 'skill-reader', args: '' })
  const ui = await $.ui.mount(PANE)
  await ui.input({ key: 'skill-path', text: 'elegida/SKILL.md', kind: 'change' })
  await ui.press({ key: 'load-original' })
  await ui.press({ key: 'translate' })
  expect(models).toBe(0)
  expect(await ui.find({ type: 'Text', text: 'Completado' })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: content })).toBeDefined()
  await ui.unmount()
})

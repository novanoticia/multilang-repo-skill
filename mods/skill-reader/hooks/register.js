const PANE = 'skill-reader'
const MAX_FILE_BYTES = 64 * 1024

let panelOpen = false
let generation = 0
let draftPath = ''
let selectedPath = ''
let original = ''
let status = 'idle'
let errorMessage = ''

class ReaderError extends Error {}

function clearReader() {
  generation += 1
  panelOpen = false
  draftPath = ''
  selectedPath = ''
  original = ''
  status = 'idle'
  errorMessage = ''
}

function changePath($, value) {
  if (!panelOpen) return
  generation += 1
  draftPath = value
  selectedPath = ''
  original = ''
  status = 'idle'
  errorMessage = ''
  $.ui.invalidate('ui.render')
}

function validatePath(value) {
  if (!value.trim() || value.length > 4096 || /[\u0000-\u001f\u007f-\u009f]/.test(value)) {
    throw new ReaderError('Introduce una ruta local válida a un archivo SKILL.md.')
  }
  const path = value.trim()
  const hasScheme = /^[a-z][a-z0-9+.-]*:/i.test(path)
  const isWindowsDrive = /^[a-z]:[\\/]/i.test(path)
  if ((hasScheme && !isWindowsDrive) || /^[\\/]{2}/.test(path)) {
    throw new ReaderError('Selecciona una ruta local, no una URL ni una ruta de red.')
  }
  if (path.startsWith('~')) {
    throw new ReaderError('Usa una ruta relativa o absoluta; ~ no se expande.')
  }
  if (path.split(/[\\/]/).at(-1) !== 'SKILL.md') {
    throw new ReaderError('El archivo elegido debe llamarse exactamente SKILL.md.')
  }
  return path
}

async function loadOriginal($) {
  if (!panelOpen || status === 'loading') return
  const request = ++generation
  selectedPath = ''
  original = ''
  errorMessage = ''
  status = 'loading'
  $.ui.invalidate('ui.render')

  try {
    const path = validatePath(draftPath)
    const info = await $.fs.stat(path)
    // No iniciar una lectura después de cerrar o cambiar la selección.
    if (!panelOpen || request !== generation) return
    if (info.kind !== 'file') {
      throw new ReaderError('La ruta elegida no corresponde a un archivo.')
    }
    if (info.size > MAX_FILE_BYTES) {
      throw new ReaderError('El archivo supera el límite de 64 KiB de esta versión.')
    }

    const text = await $.fs.read(path)
    if (!panelOpen || request !== generation) return
    // El archivo puede haber crecido desde la consulta de tamaño.
    if (new TextEncoder().encode(text).length > MAX_FILE_BYTES) {
      throw new ReaderError('El archivo supera el límite de 64 KiB de esta versión.')
    }
    if (!text.trim()) {
      throw new ReaderError('El archivo está vacío.')
    }
    const displayText = text.replace(/\r\n/g, '\n')
    if (/[\u0000-\u0008\u000b-\u001f\u007f-\u009f]/.test(displayText)) {
      throw new ReaderError('El archivo contiene caracteres de control no admitidos.')
    }

    selectedPath = path
    original = text
    status = 'ready'
  } catch (error) {
    if (!panelOpen || request !== generation) return
    status = 'error'
    errorMessage = error instanceof ReaderError
      ? error.message
      : 'No se pudo cargar el archivo. Comprueba la ruta y los permisos de lectura.'
  }
  $.ui.invalidate('ui.render')
}

export function register(on) {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'skill-reader',
      description: 'Abrir el panel de lectura de skills (en desarrollo)',
    })
    return next(e)
  })

  on('command.run', { command: 'skill-reader' }, async ($) => {
    clearReader()
    panelOpen = true
    await $.ui.open({
      id: PANE,
      title: 'Lector de skills',
      focus: true,
      closeOnEscape: true,
    })
    // El contenido del panel no se añade al historial del agente.
    return {}
  })

  on('ui.close', { id: 'skill-reader' }, async ($, e, next) => {
    clearReader()
    $.ui.invalidate('ui.render')
    return next(e)
  })

  on('session.end', async ($, e, next) => {
    clearReader()
    $.ui.invalidate('ui.render')
    return next(e)
  })

  on('ui.render', { component: 'Pane' }, async ($, e, next) => {
    // Los paneles de otros componentes continúan sin cambios.
    if (e.requestId !== PANE) return next(e)

    const { Box, Text, Button, Input } = $.ui.resolve(e)
    return Box({
      flexDirection: 'column',
      children: [
        Text({ children: ['Lector de skills — en desarrollo'] }),
        Input({
          key: 'skill-path',
          label: 'Ruta de SKILL.md',
          placeholder: 'skills/mi-skill/SKILL.md',
          value: draftPath,
          submitLabel: 'cargar original',
          onInput: (value) => changePath($, value),
          onSubmit: async (value) => {
            if (value !== draftPath) changePath($, value)
            await loadOriginal($)
          },
        }),
        Text({ children: ['Ruta local sin comillas; se admiten espacios. Máximo: 64 KiB.'] }),
        ...(status === 'loading' ? [] : [Button({
          key: 'load-original',
          label: 'Cargar original',
          onPress: () => loadOriginal($),
        })]),
        Text({ children: [status === 'ready' ? 'Preparado'
          : status === 'loading' ? 'Leyendo…'
          : status === 'error' ? 'Error: ' + errorMessage
          : 'Sin archivo seleccionado.'] }),
        Text({ children: ['Solo se lee el archivo elegido. No se envía contenido a un modelo.'] }),
        Text({ children: [selectedPath ? 'Original — ' + selectedPath : 'Original'] }),
        Text({ children: [original ? original.replace(/\r\n/g, '\n') : 'Sin contenido.'] }),
        Text({ children: ['Traducción: pendiente de implementar.'] }),
        Button({
          key: 'close',
          label: 'Cerrar',
          onPress: async () => {
            clearReader()
            $.ui.invalidate('ui.render')
            await $.ui.close({ id: PANE })
          },
        }),
      ],
    })
  })
}

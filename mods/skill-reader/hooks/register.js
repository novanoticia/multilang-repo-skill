const PANE = 'skill-reader'

export function register(on) {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'skill-reader',
      description: 'Abrir el panel de lectura de skills (en desarrollo)',
    })
    return next(e)
  })

  on('command.run', { command: 'skill-reader' }, async ($) => {
    await $.ui.open({
      id: PANE,
      title: 'Lector de skills',
      focus: true,
      closeOnEscape: true,
    })
    // El contenido del panel no se añade al historial del agente.
    return {}
  })

  on('ui.render', { component: 'Pane' }, async ($, e, next) => {
    // Los paneles de otros componentes continúan sin cambios.
    if (e.requestId !== PANE) return next(e)

    const { Box, Text, Button } = $.ui.resolve(e)
    return Box({
      flexDirection: 'column',
      children: [
        Text({ children: ['Lector de skills — en desarrollo'] }),
        Text({ children: ['Sin archivo seleccionado.'] }),
        Text({ children: ['Esta entrega solo abre y cierra el panel.'] }),
        Text({ children: ['Original: sin contenido.'] }),
        Text({ children: ['Traducción: sin contenido.'] }),
        Button({
          key: 'close',
          label: 'Cerrar',
          onPress: () => $.ui.close({ id: PANE }),
        }),
      ],
    })
  })
}

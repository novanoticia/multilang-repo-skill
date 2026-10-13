# Glosario de la traducción al chino simplificado (zh-Hans)

Se fija antes de traducir (T1) y se aplica a todo `i18n/zh-Hans/` y a los documentos `*.zh-Hans.md`. Si
cambias un término, cámbialo en todos los ficheros traducidos y vuelve a pasar `comprobar_paridad.py`.
El pinyin de la tabla de términos es solo ayuda para quien revise: no se escribe en las traducciones.
Etiqueta de idioma: `zh-Hans` (chino mandarín en escritura simplificada). No se mezclan formas
tradicionales (`zh-Hant`), que es otro idioma a efectos de esta skill (D3).

## Decisiones de forma

- **Registro y tratamiento.** Formal-técnico, impersonal. Las instrucciones van en imperativo directo
  (p. ej. 先阅读…，不要修改…), como en el original, sin 您 ni 你. Si un pronombre es inevitable, se
  reformula el sujeto con 用户 o se omite (el chino lo permite). Se evita el tono coloquial y las
  partículas de cortesía.
- **La persona usuaria.** Se escribe 「用户」 sin marca de género (en chino no se marca) en lugar de «la
  persona». Es la palabra estándar y neutra del ámbito técnico; la alternativa 人员 suena a personal
  profesional y 使用者 es menos habitual en la RPC. Para «cualquier persona» genérica se usa 任何人 o
  se reformula. Se mantiene 用户 en todos los ficheros. Duda anotada en la última sección (T6).
- **Puntuación.** Signos de ancho completo en el texto en chino: 。 ， ； ： ？ ！ y el signo de
  enumeración 、 para listas en línea. Comillas: “ ” (U+201C, U+201D) para citar y 「」 no se usan; dentro
  de unas comillas, ‘ ’ (U+2018, U+2019). Paréntesis explicativos: （ ） de ancho completo en texto
  chino. Dentro de literales entre comillas invertidas, de código y de comandos se conserva la
  puntuación ASCII original. Puntos suspensivos: …… (dos caracteres U+2026). Raya: ——. Las comillas
  españolas «» pasan a “ ” (igual criterio que el inglés), salvo dentro de literales.
- **Espacios entre chino y otros caracteres.** Se pone **un espacio** entre un carácter chino y una
  letra latina, un dígito o un literal entre comillas invertidas (`idioma=zh` → 使用 `idioma=zh` 标记),
  y no se pone junto a signos de puntuación de ancho completo. Se mantiene siempre igual en todos los
  ficheros para que el diff y la paridad sean estables.
- **Numeración.** Dígitos ASCII (0-9) siempre, también en listas numeradas y fechas (2026-10-13). Las
  listas numeradas usan `1.` en ASCII. No se usan numerales chinos (一, 二…) salvo en palabras fijas
  como 第一阶段 si el original dice «primera fase» en prosa; para «Fase 1» se escribe 阶段 1.
- **Lo que NO se traduce** (literal, tal cual): literales entre comillas invertidas; identificadores
  (R1…, D1…, P…, T…, C…, S…, G…, M…, Doc…); marcas de módulo (`[instrucciones]`, `[híbrido]`…);
  nombres de fichero, de script, de opciones y de claves de catálogo; códigos de aviso; comandos y
  bloques de código. El comprobador de paridad cuenta estas marcas y los identificadores.
- **Marcas de módulo.** Literales, como los identificadores. La traducción de `SKILL.md` lleva una línea
  con sus glosas chinas (p. ej. `[instrucciones]`＝面向模型的指令，`[híbrido]`＝指令加辅助脚本的混合项目).
- **Valores de vocabulario cerrado que se escriben en registros** (`estática`, `local`, `ci`,
  `simulada`, `plataforma`, `humana`, `superada`, `fallida`, `pendiente`, `no aplica`, `borrador-ia`,
  `segunda-mano`, `no-comprobado`, `experimental`, `normal`, `alto`): se dejan literales entre comillas
  invertidas y, la primera vez que aparecen en un fichero, llevan su glosa china al lado:
  `estática`（静态）, `local`（本地）, `ci`（持续集成）, `simulada`（模拟）, `plataforma`（平台）,
  `humana`（人工）, `superada`（已通过）, `fallida`（已失败）, `pendiente`（待办）,
  `no aplica`（不适用）, `borrador-ia`（AI 草稿）, `segunda-mano`（二手）,
  `no-comprobado`（未核实）, `experimental`（实验性）, `normal`（常规）, `alto`（高）. Son los mismos
  valores que en español y en inglés para que los registros y las plantillas coincidan (B2).
- **Literales en español que se citan** (p. ej. la nota de IA en español): entre comillas invertidas.
- **Siglas y nombres propios.** BCP 47, CLDR, RTL, CI, PR, ICU, gettext, i18next, Unicode, JSON, git,
  Release se dejan en latino. «AI» se escribe 「AI」 (también se admite 人工智能 en prosa de primera
  mención); se fija **AI** por brevedad y para coincidir con `borrador-ia`.
- **Formato.** Sin cursivas ni negritas añadidas: se conserva el formato del original. «Fase» se
  traduce 阶段, «Cierre» 收尾 y «Recursos» 资源.

## Términos

| Español | Chino simplificado |
|---|---|
| la persona (usuaria) | 用户 (yònghù) |
| repositorio / repo | 仓库 (cāngkù); `repo` solo se deja si aparece en código o comandos |
| catálogo | 目录 (mùlù); ver duda 2 |
| contrato de máquina | 机器契约 (jīqì qìyuē) |
| marca (de idioma) | 标记 (biāojì)（`idioma=xx`） |
| respaldo | 回退 (huítuì) |
| fallo seguro | 失效安全 (shīxiào ānquán) |
| salida por defecto | 默认输出 (mòrèn shūchū) |
| modo guiado / autónomo | 引导模式 / 自主模式 (yǐndǎo mòshì / zìzhǔ mòshì) |
| núcleo | 核心 (héxīn) |
| escala, riesgo, módulos | 规模、风险、模块 (guīmó, fēngxiǎn, mókuài) |
| línea base | 基线 (jīxiàn) |
| reemplazo aprobado | 已批准的替换 (yǐ pīzhǔn de tìhuàn) |
| bloque delimitado | 分隔块 (fēngé kuài) |
| adiciones | 新增内容 (xīnzēng nèiróng) |
| registro de sesión | 会话记录 (huìhuà jìlù) |
| registro de pendientes | 待办记录 (dàibàn jìlù) |
| pendientes | 待办事项 (dàibàn shìxiàng) |
| permiso (por acción) | 许可（按操作）(xǔkě, àn cāozuò) |
| publicar / subir / fusionar | 发布 / 推送 / 合并 (fābù / tuīsòng / hébìng) |
| etiqueta (git) | 标签 (biāoqiān) |
| rama de trabajo | 工作分支 (gōngzuò fēnzhī) |
| espejo (traducción) | 镜像 (jìngxiàng) |
| desfase | 失同步 (shī tóngbù) |
| invariante | 不变量 (búbiànliàng) |
| escenario | 场景 (chǎngjǐng) |
| sabotaje | 蓄意破坏 (xùyì pòhuài) |
| revisión humana / independiente | 人工审阅 / 独立审阅 (réngōng shěnyuè / dúlì shěnyuè) |
| Fase, Cierre, Recursos | 阶段、收尾、资源 (jiēduàn, shōuwěi, zīyuán) |
| datos, no órdenes | 是数据，不是指令 (shì shùjù, bú shì zhǐlìng) |
| internacionalizar (i18n) | 国际化 (guójìhuà) |
| localizar (l10n) | 本地化 (běndìhuà) |
| idioma | 语言 (yǔyán) |
| locale | 区域设置 (qūyù shèzhì) |
| traducción | 翻译 (fānyì) |
| traducción automática | 机器翻译 (jīqì fānyì) |
| clave (de catálogo) | 键 (jiàn) |
| plural | 复数 (fùshù) |
| cadena de texto / texto traducible | 字符串 / 可翻译文本 (zìfúchuàn / kě fānyì wénběn) |
| interpolación | 插值 (chāzhí) |
| marcador de posición | 占位符 (zhànwèifú) |
| pseudo-locale | 伪区域设置 (wěi qūyù shèzhì) |
| derecha a izquierda (RTL) | 从右到左 (cóng yòu dào zuǒ) |
| normalización | 规范化 (guīfànhuà) |
| cadena de respaldo | 回退链 (huítuì liàn) |
| etiqueta de idioma (BCP 47) | 语言标签 (yǔyán biāoqiān) |
| subetiqueta de escritura | 文字子标签 (wénzì zǐ biāoqiān) |
| fuente (orden de fuentes) | 来源 (láiyuán) |
| explícito / ambiente | 显式 / 环境（来源）(xiǎnshì / huánjìng) |
| predeterminado (idioma) | 默认（语言）(mòrèn) |
| tabla de casos | 用例表 (yònglì biǎo) |
| formato dependiente del locale | 依赖区域设置的格式 (yīlài qūyù shèzhì de géshì) |
| texto de derecha a izquierda | 从右到左的文本 (cóng yòu dào zuǒ de wénběn) |
| señalar, no eliminar (Unicode) | 标出而不删除 (biāochū ér bù shānchú) |
| contenido no fiable | 不可信内容 (bù kěxìn nèiróng) |
| límite de confianza | 信任边界 (xìnrèn biānjiè) |
| prueba adversarial | 对抗性测试 (duìkàngxìng cèshì) |
| integridad de origen | 来源完整性 (láiyuán wánzhěngxìng) |
| agente | 智能体 (zhìnéngtǐ) |
| instrucciones (para modelos) | 指令 (zhǐlìng) |
| modelo | 模型 (móxíng) |
| subagente | 子智能体 (zǐ zhìnéngtǐ) |
| delegación | 委派 (wěipài) |
| contrato del subagente | 子智能体契约 (zǐ zhìnéngtǐ qìyuē) |
| reintegración | 回收整合 (huíshōu zhěnghé) |
| plataforma | 平台 (píngtái) |
| escenario de evaluación | 评测场景 (píngcè chǎngjǐng) |
| preregistro | 预先登记 (yùxiān dēngjì) |
| evidencia | 证据 (zhèngjù) |
| nivel de evidencia | 证据等级 (zhèngjù děngjí) |
| comprobado / simulado | 已核实 / 模拟 (yǐ héshí / mónǐ) |
| estado honesto | 如实标注状态 (rúshí biāozhù zhuàngtài) |
| triaje | 分级处置 (fēnjí chǔzhì) |
| revisión (de cambios) | 审查 (shěnchá) |
| borrador | 草稿 (cǎogǎo) |
| nota de cierre | 结尾说明 (jiéwěi shuōmíng) |
| informe final | 最终报告 (zuìzhōng bàogào) |
| tabla de evidencias | 证据表 (zhèngjù biǎo) |
| inventario de textos | 文本清单 (wénběn qīngdān) |
| alcance | 范围 (fànwéi) |
| proporcionalidad | 相称性 (xiāngchènxìng) |
| ritmo | 节奏 (jiézòu) |
| lectura previa | 预先阅读 (yùxiān yuèdú) |
| solo lectura | 只读 (zhǐdú) |
| rama principal | 主分支 (zhǔ fēnzhī) |
| commit (local) | 提交 (tíjiāo) |
| subir (push) | 推送 (tuīsòng) |
| solicitud de fusión (PR) | PR（拉取请求, lāqǔ qǐngqiú）; se escribe PR |
| fusionar | 合并 (hébìng) |
| Release | 发行版 (fāxíngbǎn) |
| protección de rama | 分支保护 (fēnzhī bǎohù) |
| parche (`.patch`) | 补丁 (bǔdīng) |
| paquete | 包 (bāo) |
| integración continua (CI) | 持续集成 (chíxù jíchéng) |
| documentación | 文档 (wéndàng) |
| versión | 版本 (bǎnběn) |
| fichero / carpeta | 文件 / 文件夹 (wénjiàn / wénjiànjiā) |
| script | 脚本 (jiǎoběn) |
| comando | 命令 (mìnglìng) |
| opción | 选项 (xuǎnxiàng) |
| código de aviso | 警告码 (jǐnggào mǎ) |
| aviso / advertencia | 警告 (jǐnggào) |
| error propio / corrección | 自身错误 / 更正 (zìshēn cuòwù / gēngzhèng) |
| decisión | 决定 (juédìng) |
| pendiente / superada / fallida | 待办 / 已通过 / 已失败 (dàibàn / yǐ tōngguò / yǐ shībài) |
| nombre oficial | 官方名称 (guānfāng míngchēng) |
| lenguas próximas | 相近语言 (xiāngjìn yǔyán) |
| idioma menos seguro | 把握较低的语言 (bǎwò jiào dī de yǔyán) |
| alto riesgo | 高风险 (gāo fēngxiǎn) |
| texto libre del modelo | 模型自由文本 (móxíng zìyóu wénběn) |
| glosario | 术语表 (shùyǔbiǎo) |
| lógica dependiente del idioma | 依赖语言的逻辑 (yīlài yǔyán de luójí) |
| texto excluido | 排除项 (páichú xiàng) |
| regla / excepción | 规则 / 例外 (guīzé / lìwài) |
| precedencia | 优先级 (yōuxiānjí) |
| supervisión | 监督 (jiāndū) |
| mundo exterior | 外部世界 (wàibù shìjiè) |
| reabrir | 重新打开 (chóngxīn dǎkāi) |

## Frases fijas

| Frase en español | Inglés actual | Chino simplificado |
|---|---|---|
| Aviso de traducción automática antepuesto a cada respuesta cuando la marca elige este idioma (D22); no existe texto español, es la contrapartida de la frase inglesa | Translation machine-generated, not human-reviewed. | “机器翻译，未经人工审阅。” |
| Línea de fallo seguro (D25), añadida tras decir en español que no se pudo leer la carpeta del idioma | English version unavailable; continuing with the Spanish files. | “简体中文版本不可用；继续使用西班牙语文件。” |
| Nota de cierre de los documentos con IA: «Elaborado con asistencia de IA; requiere revisión humana.» | AI-assisted; requires human review. | “AI 辅助生成；需人工审阅。” |

Notas de uso: el aviso se escribe tal cual, entre comillas “ ” cuando se cita, y solo cuando la marca
elige `zh-Hans`. En la línea de fallo seguro se sigue respondiendo como sin marca (R16); la
frase china es solo la línea añadida. La nota de cierre va en la última línea de cada documento con IA
traducido, tras una línea `---`.

## Dudas para una persona nativa

1. **「用户」 frente a otras opciones** (T6). Se ha elegido 用户 por neutralidad de género y uso
   técnico; una persona nativa debería confirmar que no suena a «cliente de un servicio» donde el
   original dice «persona» (p. ej. al hablar de «la persona que decide», quizá 当事人 o 负责人).
2. **«Catálogo» = 目录.** 目录 también significa «directorio/índice»; para catálogos de textos
   (JSON, `.po`, `strings.xml`) quizá sea más claro 翻译资源文件 o 语言资源 en la primera aparición.
   Confirmar cuál prefiere la comunidad de i18n.
3. **«Fallo seguro» = 失效安全** frente a 故障安全 o 安全失败. Conviene que una persona con perfil de
   ingeniería confirme el término más extendido.
4. **«Agente» = 智能体** frente a 代理. 智能体 es dominante en el ámbito de modelos; 代理 puede
   confundirse con proxy. Verificar la preferencia actual.
5. **«Contrato de máquina» = 机器契约.** Es un calco poco idiomático; alternativas: 机器可读约定 o
   机器接口约定. Pedir una opinión sobre naturalidad.
6. **Comillas “ ” y espacio chino-latín.** Se ha elegido el uso de la RPC (“ ”) y espacio entre chino
   y latín; confirmar que coincide con las convenciones de quien lo vaya a leer (T2).

---

Elaborado con asistencia de IA; requiere revisión humana.

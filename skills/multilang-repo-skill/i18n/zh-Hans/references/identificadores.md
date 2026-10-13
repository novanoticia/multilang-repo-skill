<!-- i18n fuente-sha256=22bfd9e76ce2 estado=borrador-ia -->

# 标识符索引

用于通过标识符定位某条规则、引用它或豁免它。标识符是稳定的：被撤销的规则不会被重新用于其他含义。

## 内容
- 各条规则在哪里
- 相对于先前框架（v7）的变化

## 各条规则在哪里

| 前缀 | 范围 | 标识符 | 文件 |
|---|---|---|---|
| R | 核心：工作、许可、证据 | R1–R20 | SKILL.md |
| D | 设计 | D1 | SKILL.md（阶段 3） |
| | | D2–D7 | references/seleccion-idioma.md |
| | | D8–D15、D17–D20 | references/diseno-catalogos.md |
| | | D16、D30、D31 | references/formatos-rtl-unicode.md |
| | | D21–D23、D25、D27–D29 | references/instrucciones-y-agentes.md |
| | | D24 | references/seguridad.md |
| | | D26 | references/traducciones.md |
| P | 测试、审查与分级处置 | P1–P15 | references/pruebas-y-evidencia.md |
| T | 翻译 | T1–T7 | references/traducciones.md |
| C | 外部内容 | C1–C9 | references/contenido-externo.md |
| S | 安全 | S1–S4、S6（S5 已撤销） | references/seguridad.md |
| Doc | 文档与包 | Doc1–Doc9 | references/documentacion-y-paquete.md |
| G | 发布 | G1–G9 | references/publicacion.md |
| M | 委派 | M1–M7 | references/delegacion.md |

各阶段保留 0–9 的编号。清单的类别是单个字母（A–H），不要与规则标识符混淆。

## 相对于先前框架（v7）的变化

R1–R16、D1–D29、P1–P12、T1–T6、C1–C8、G1–G9 和 M1–M7 的编号和含义均保留。部分规则扩大或收窄了范围，但对象不变：

| 标识符 | 变化 |
|---|---|
| R4、R5 | 摘要和提问的节奏取决于监督模式（R18）。 |
| R6 | 增加记录的位置，以及只需一次确认即可恢复。 |
| R7 | 六个等级：增加 `estática`（静态）和 `humana`（人工），并区分 `ci`（持续集成）与 `local`（本地）。 |
| R13 | 区分能力、需要与授权；永久许可不再重复请求。 |
| R16 | AI 说明只出现在面向人的公开文档中，绝不出现在机器文件中。 |
| D1 | 区分确定性输出（精确比较）与面向模型的指令（精确文本与不变量）。 |
| D3 | 保留文字子标签，把 `C`/`POSIX` 视为缺省，并允许显式环节。 |
| D4 | 区分显式输入与环境输入。 |
| D13 | 首先遵循生态的格式；NFC 不强加给参照字面量。 |
| D16 | 不再包含 RTL，RTL 改为 D30。 |
| D18 | 给默认输出添加 `lang` 需要例外（D23）。 |
| D22 | 警告绝不放进机器格式。 |
| P4 | 不适用于模型生成的文本；属于 `local` 等级。 |
| P5 | 不变性测试通过蓄意破坏来验证，而不是看到它们变红。 |
| P7 | 适用于你编写的检查，并与规模相称。 |
| M1–M7 | [multi-modelo] 模块改为 [delegación]，不再依赖外部协议。 |

新增标识符：R17（优先级，此前是没有标识符的一段）、R18（模式）、R19（请求的范围）、R20（相称性，此前是一段以及阶段 1.8 的表）、D30、D31、P13–P15（此前是没有标识符的阶段 8.2、8.1 和 8.3）、T7、C9、S1–S4、S6，以及 Doc1–Doc9（此前是没有标识符的阶段 7）。

模块标签：`[alto riesgo]` 改为 `[alto-riesgo]`，不再强制 L 规模；`[multi-modelo]` 改为 `[delegación]`；`[release]` 分拆为 `[paquete]` 和 `[publicación]`。新增 `[ecosistema]`、`[rtl-escrituras]`、`[seguridad]` 和 `[documentación]`。S、M、L 规模保留其字母，但现在只衡量结构；风险是另一条独立的轴。

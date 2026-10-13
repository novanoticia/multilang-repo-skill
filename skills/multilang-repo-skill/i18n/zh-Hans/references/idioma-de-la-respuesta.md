<!-- i18n fuente-sha256=5741eaf9c542 estado=borrador-ia -->

# 本技能的回复语言

这是 `SKILL.md` 中“回复语言”块的详细说明。当用户用 `idioma=xx` 或 `lang=xx` 指定语言，或者你不确定标记如何解析、各语言对应哪句固定用语、哪些内容不翻译时，阅读本文。选择规则和失效安全已在该块中给出；这里补充其余部分。

## 内容
- 可用语言及状态
- 标记如何解析
- 各语言的固定用语
- 不翻译的内容

## 可用语言及状态

| 语言 | 文件夹 | 状态 |
|---|---|---|
| `es` | 原始文件 | 基准 |
| `en` | `i18n/en/` | `borrador-ia`（AI 草稿） |
| `fr` | `i18n/fr/` | `borrador-ia` |
| `zh-Hans`（简体中文） | `i18n/zh-Hans/` | `borrador-ia` |
| `hi`（印地语） | `i18n/hi/` | `experimental`（实验性）：必须由母语者审阅（T6） |

所有翻译均未经人工审阅（T5）。标记选择的是回复语言，而不是仓库要翻译成的语言。

## 标记如何解析

不区分大小写，并去掉字符集部分（`en_US.UTF-8` 即 `en-US`）：

| 标记 | 结果 |
|---|---|
| `en`、`en-GB`、`en-US` | `en` |
| `fr`、`fr-CA`、`fr-FR` | `fr` |
| `hi`、`hi-IN` | `hi` |
| `zh`、`zh-CN`、`zh-SG`、`zh-Hans`、`zh-Hans-CN` | `zh-Hans` |
| `zh-Hant`、`zh-TW`、`zh-HK`、`zh-MO` | 不可用（D4）：不向要求繁体的用户提供简体中文（D3） |
| 其他任何标记（`de`、`pt-BR`……） | 不可用（D4）：说明情况，列出可用语言，并按无标记继续 |

[scripts/resolver_idioma.py](../../../scripts/resolver_idioma.py) 实现了这条规则；其来源 `defecto` 表示“无标记”，而不是“用西班牙语回复”。针对此列表：

```
python3 <skill>/scripts/resolver_idioma.py --disponibles es,en,fr,hi,zh-Hans --defecto es --respaldo zh=zh-Hans --respaldo zh-CN=zh-Hans --respaldo zh-SG=zh-Hans --respaldo zh-TW=zh-Hant --respaldo zh-HK=zh-Hant --respaldo zh-MO=zh-Hant
```

## 各语言的固定用语

仅当标记选择该语言时才显示（D22）：提示放在每条回复的开头；如果无法读取 `i18n/<idioma>/`，则追加失效安全行（D25）。

| 语言 | 机器翻译提示 | 失效安全行 |
|---|---|---|
| `en` | `Translation machine-generated, not human-reviewed.` | `English version unavailable; continuing with the Spanish files.` |
| `fr` | `Traduction automatique, non relue par une personne.` | `Version française indisponible ; poursuite avec les fichiers espagnols.` |
| `zh-Hans` | `机器翻译，未经人工审阅。` | `简体中文版本不可用；继续使用西班牙语文件。` |
| `hi` | `अनुवाद मशीन द्वारा तैयार किया गया है, मानव द्वारा समीक्षित नहीं। (Translation machine-generated, not human-reviewed.)` | `हिन्दी संस्करण उपलब्ध नहीं है; स्पैनिश फ़ाइलों के साथ आगे बढ़ा जा रहा है।` |

印地语的提示是双语的，因为该语言以 `experimental` 状态交付（T6）。

## 不翻译的内容

标识符（R1……Doc9）、模块标记、文件名和脚本名、选项、警告码、命令和代码块。脚本的消息仍为西班牙语。

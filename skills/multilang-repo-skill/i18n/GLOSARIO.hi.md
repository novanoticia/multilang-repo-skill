# Glosario de la traducción al hindi

Se fija antes de traducir (T1) y se aplica a todo `i18n/hi/` y a los documentos `*.hi.md`. Si cambias un
término, cámbialo en todos los ficheros traducidos y vuelve a pasar `comprobar_paridad.py`. Está escrito
en español para que lo revise quien mantiene el repositorio; la transliteración latina entre paréntesis
aparece solo en las tablas, para revisión por personas que no leen devanagari, y no se usa en las
traducciones. Hindi técnico: ver «Dudas para una persona nativa» (T6).

## Decisiones de forma

- **Registro y tratamiento.** Se usa «आप» (nivel cortés) con imperativos corteses en `-ें`: «पढ़ें»,
  «जाँचें», «लिखें», «रुकें». Es el registro habitual de la documentación técnica en hindi, no suena
  seco como «तू» ni confianzudo como «तुम», y el imperativo de cortesía no marca género. Se documenta el
  tratamiento elegido (T1). Instrucciones al agente y a la persona van igual: imperativo directo, como en
  el original. No se usa «आप» explícito salvo que la frase lo necesite.
- **La persona usuaria y el género.** El original dice «la persona» y evita marcar género. En hindi se
  usa «व्यक्ति» (*vyakti*), nunca «उपयोगकर्ता» (*upyogkarta*, masculino y más «producto») ni «यूज़र».
  «व्यक्ति» es masculino por gramática pero se usa con valor genérico y el hindi lo admite sin marca
  de sexo. Para no marcar género al conjugar: (1) preferir imperativos cortesía («पूछें», «बताएँ»);
  (2) preferir subjuntivo/pasivo con «चाहिए», «होना चाहिए», «किया जाए» antes que perfectivos
  concordados («चाहता/चाहती»); (3) cuando haga falta un pronombre, usar el honorífico plural «वे/उन्हें/
  उनका», que no marca género en el pronombre, y construir el verbo en subjuntivo («वे चाहें तो») y no
  en presente («वे चाहते हैं», que sería masculino plural); (4) si la frase se vuelve forzada, repetir
  «व्यक्ति» en lugar del pronombre. Nunca «वह/उसे» con verbo en perfectivo.
- **Préstamos del inglés frente a calcos.** Se usa el término que un desarrollador hindi-hablante
  emplea de verdad. Los préstamos habituales se escriben en devanagari, con nukta cuando corresponde:
  रिपॉज़िटरी, ब्रांच, कमिट, मर्ज, टैग, कैटलॉग, फ़ॉलबैक, बेसलाइन, स्क्रिप्ट, फ़ाइल, फ़ोल्डर, टेस्ट,
  लोकेल, यूनिकोड. Cuando existe un calco hindi vivo y comprensible (अनुवाद, समीक्षा, अनुमति, सुरक्षा,
  चरण) se prefiere el hindi. Se mantienen en alfabeto latino solo los identificadores y literales de
  código: `idioma=xx`, nombres de fichero, scripts, opciones, claves, códigos de aviso, comandos y
  bloques de código. «AI» se escribe «AI» en latino en la nota de cierre (como se lee en la práctica) y
  «एआई» no se usa.
- **Puntuación.** Danda «।» al final de oración (no punto «.»), y se mantiene en todos los ficheros.
  Coma, punto y coma, dos puntos y signos de interrogación/exclamación son los latinos (`,` `;` `:` `?`
  `!`). El punto «.» se conserva dentro de literales, rutas, versiones, abreviaturas latinas y listas
  numeradas («1.»). Comillas: las españolas «» pasan a “ ”. Los literales entre comillas invertidas no
  se tocan. Elección revisable por una persona nativa (T2).
- **Numeración.** Dígitos ASCII (0–9), no devanagari (०–९): así coinciden con los identificadores,
  versiones, fechas y claves de los scripts.
- **No se traducen:** literales entre comillas invertidas; identificadores (R1…, D1…, P…, T…, C…, S…,
  G…, M…, Doc…); marcas de módulo (`[instrucciones]`, `[híbrido]`…) —igual que en inglés, la
  traducción de `SKILL.md` lleva una línea con sus glosas hindi—; nombres de fichero, de script y de
  opción; claves de catálogo; códigos de aviso; comandos; bloques de código. El comprobador de paridad
  los cuenta.
- **Valores de vocabulario cerrado que se escriben en registros** (`estática`, `local`, `ci`,
  `simulada`, `plataforma`, `humana`, `superada`, `fallida`, `pendiente`, `no aplica`, `borrador-ia`,
  `segunda-mano`, `no-comprobado`, `experimental`, `normal`, `alto`): se dejan literales entre comillas
  invertidas (en español, no se transliteran) y, la primera vez que aparecen en un fichero, llevan su
  glosa hindi al lado: `estática` (स्थैतिक), `local` (स्थानीय), `ci` (CI), `simulada` (सिम्युलेटेड),
  `plataforma` (प्लेटफ़ॉर्म), `humana` (मानवीय), `superada` (उत्तीर्ण), `fallida` (विफल), `pendiente`
  (लंबित), `no aplica` (लागू नहीं), `borrador-ia` (AI-मसौदा), `segunda-mano` (द्वितीयक स्रोत),
  `no-comprobado` (असत्यापित), `experimental` (प्रायोगिक), `normal` (सामान्य), `alto` (उच्च). Son los
  mismos valores en español y en hindi para que registros y plantillas coincidan (B2).
- **Literales en español que se citan** (p. ej. la nota de IA en español): entre comillas invertidas.

## Términos

La transliteración latina es solo de revisión; no se copia a las traducciones.

| Español | Hindi |
|---|---|
| la persona (usuaria) | व्यक्ति (*vyakti*) |
| repositorio / repo | रिपॉज़िटरी / रेपो (*ripozitari / repo*) |
| catálogo | कैटलॉग (*kailog*) |
| clave (de catálogo) | कुंजी (*kunji*) |
| contrato de máquina | मशीन अनुबंध (*mashīn anubandh*) |
| marca (de idioma) | मार्कर (*mārkar*) `idioma=xx` |
| respaldo | फ़ॉलबैक (*fālbaik*) |
| fallo seguro | सुरक्षित विफलता-व्यवहार (*surakshit viphalta-vyavahār*) |
| salida por defecto | डिफ़ॉल्ट आउटपुट (*difolt āutpuṭ*) |
| modo guiado / autónomo | निर्देशित / स्वायत्त मोड (*nirdeshit / svāyatt mod*) |
| núcleo | कोर (*kor*) |
| escala, riesgo, módulos | पैमाना, जोखिम, मॉड्यूल (*paimānā, jokhim, moḍyūl*) |
| línea base | बेसलाइन (*beslāin*) |
| reemplazo aprobado | अनुमोदित प्रतिस्थापन (*anumodit pratisthāpan*) |
| bloque delimitado | सीमांकित ब्लॉक (*sīmānkit blok*) |
| adiciones | परिवर्धन (*parivardhan*) |
| registro de sesión | सत्र-लॉग (*satra-log*) |
| registro de pendientes | लंबित-सूची लॉग (*lambit-sūchī log*) |
| pendientes | लंबित बिंदु (*lambit bindu*) |
| permiso (por acción) | अनुमति (प्रति कार्रवाई) (*anumati (prati kārravāī)*) |
| publicar | प्रकाशित करना (*prakāshit karnā*) |
| subir (push) | पुश करना (*push karnā*) |
| fusionar (merge) | मर्ज करना (*marj karnā*) |
| etiqueta (git) | टैग (*taig*) |
| rama de trabajo | कार्य-ब्रांच (*kārya-brānch*) |
| espejo (traducción) | प्रतिबिंब (*pratibimb*) |
| desfase | अंतर / असंगति (*antar / asangati*) |
| invariante | अपरिवर्तनीय नियम (*aparivartanīy niyam*) |
| escenario | परिदृश्य (*paridrishya*) |
| sabotaje | तोड़फोड़ परीक्षण (*todfod parīkshan*) |
| revisión humana / independiente | मानवीय / स्वतंत्र समीक्षा (*mānavīy / svatantra samīkshā*) |
| Fase, Cierre, Recursos | चरण, समापन, संसाधन (*charan, samāpan, sansādhan*) |
| datos, no órdenes | डेटा, आदेश नहीं (*ḍeṭā, ādesh nahīṃ*) |
| regla | नियम (*niyam*) |
| aviso | चेतावनी (*chetāvanī*) |
| excepción | अपवाद (*apvād*) |
| precedencia | प्राथमिकता-क्रम (*prāthmikatā-kram*) |
| seguridad | सुरक्षा (*surakshā*) |
| contenido no fiable | अविश्वसनीय सामग्री (*avishvasnīy sāmagrī*) |
| límite de confianza | विश्वास-सीमा (*vishvās-sīmā*) |
| evidencia | प्रमाण (*pramāṇ*) |
| nivel de evidencia | प्रमाण-स्तर (*pramāṇ-star*) |
| afirmación | दावा (*dāvā*) |
| honesto / honestidad | ईमानदार / ईमानदारी (*īmāndār / īmāndārī*) |
| borrador | मसौदा (*masauda*) |
| revisión | समीक्षा (*samīkshā*) |
| revisión nativa | मातृभाषी समीक्षा (*mātṛbhāshī samīkshā*) |
| triaje | प्राथमिकता-छँटाई (*prāthmikatā-chhantāī*) |
| plan | योजना (*yojanā*) |
| prueba (test) | परीक्षण / टेस्ट (*parīkshan / ṭesṭ*) |
| pseudo-locale | छद्म-लोकेल (*chhadma-lokel*) |
| validación | सत्यापन (*satyāpan*) |
| validador | सत्यापक (*satyāpak*) |
| comprobar | जाँचना (*jānchnā*) |
| lectura previa | पूर्व-पठन (*pūrva-pāṭhan*) |
| solo lectura | केवल-पठन (*keval-paṭhan*) |
| descubrir | खोज (*khoj*) |
| decidir | निर्णय लेना (*nirṇay lenā*) |
| diseño | डिज़ाइन (*ḍizāin*) |
| entorno | परिवेश (*pariveshh*) |
| alcance | दायरा (*dāyrā*) |
| proporcionalidad | अनुपातिकता (*anupātikatā*) |
| ritmo | गति (*gati*) |
| método | पद्धति (*paddhati*) |
| preguntas | प्रश्न (*prashn*) |
| supervisión | पर्यवेक्षण (*paryavekshan*) |
| reabrir | दोबारा खोलना (*dobārā kholnā*) |
| corregir en voz alta | खुलकर सुधारना (*khulkar sudhārnā*) |
| error propio | अपनी गलती (*apnī galtī*) |
| mundo exterior | बाहरी दुनिया (*bāhrī duniyā*) |
| ecosistema | पारितंत्र / इकोसिस्टम (*pāritantra / ikosisṭam*) |
| catálogo y claves | कैटलॉग और कुंजियाँ (*kailog aur kunjiyān*) |
| texto libre del modelo | मॉडल का मुक्त पाठ (*modal kā mukt pāṭh*) |
| agente (de IA) | एजेंट (*ejeṇṭ*) |
| subagente | सबएजेंट (*sabejeṇṭ*) |
| delegación | प्रत्यायोजन (*pratyāyojan*) |
| reintegración | पुनः एकीकरण (*punah ekīkaran*) |
| contrato del subagente | सबएजेंट अनुबंध (*sabejeṇṭ anubandh*) |
| roles, no nombres | भूमिकाएँ, नाम नहीं (*bhūmikāen, nām nahīṃ*) |
| traducción | अनुवाद (*anuvād*) |
| idioma / lengua | भाषा (*bhāshā*) |
| lenguas próximas | निकट भाषाएँ (*nikaṭ bhāshāen*) |
| idioma menos seguro | कम आत्मविश्वास वाली भाषा (*kam ātmavishvās vālī bhāshā*) |
| nombres oficiales | आधिकारिक नाम (*ādhikārik nām*) |
| alto riesgo | उच्च जोखिम (*uchch jokhim*) |
| frases de riesgo | जोखिम वाले वाक्य (*jokhim vāle vākya*) |
| glosario | शब्दावली (*shabdāvalī*) |
| tratamiento (tú/usted) | संबोधन-स्तर (*sambodhan-star*) |
| normalización | सामान्यीकरण (*sāmānyīkaran*) |
| formato dependiente del locale | लोकेल-आश्रित प्रारूप (*lokel-āshrit prārūp*) |
| texto de derecha a izquierda | दाएँ-से-बाएँ पाठ (*dāen-se-bāen pāṭh*) |
| escritura compleja | जटिल लिपि (*jaṭil lipi*) |
| política Unicode: señalar, no eliminar | यूनिकोड नीति: चिह्नित करें, हटाएँ नहीं (*yūnikod nīti: chihnit karen, haṭāen nahīṃ*) |
| inventario de textos | पाठ-सूची (*pāṭh-sūchī*) |
| datos y alcance | डेटा और दायरा (*ḍeṭā aur dāyrā*) |
| escenarios de evaluación | मूल्यांकन परिदृश्य (*mūlyānkan paridrishya*) |
| evidencias y cierre | प्रमाण और समापन (*pramāṇ aur samāpan*) |
| informe final | अंतिम रिपोर्ट (*antim ripoṛṭ*) |
| tabla de evidencias | प्रमाण-तालिका (*pramāṇ-tālikā*) |
| preregistro | पूर्व-पंजीकरण (*pūrva-panjīkaran*) |
| paquete | पैकेज (*paikej*) |
| versión | संस्करण (*sanskaran*) |
| documentación | दस्तावेज़ीकरण (*dastāvezīkaran*) |
| commit | कमिट (*kamiṭ*) |
| PR (solicitud de fusión) | पुल रिक्वेस्ट / PR (*pul rikvesṭ*) |
| Release | रिलीज़ (*rilīz*) |
| protección de rama | ब्रांच सुरक्षा (*brānch surakshā*) |
| CI | CI (*sī-āī*) |
| plataforma | प्लेटफ़ॉर्म (*pleṭfārm*) |
| irreversible | अपरिवर्तनीय (अपरिवर्तनीय कार्रवाई) (*aparivartanīy*) |
| confirmación | पुष्टि (*pushṭi*) |
| ejecución | निष्पादन / चलाना (*nishpādan / chalānā*) |
| interpolación | इंटरपोलेशन (*inṭarpoleshan*) |
| cadena de respaldo | फ़ॉलबैक शृंखला (*fālbaik shrinkhalā*) |
| plural (formas plurales) | बहुवचन (*bahuvachan*) |
| mensaje (de aviso) | संदेश (*sandesh*) |
| nota de IA | AI-नोट (*ei-āī noṭ*) |

## Frases fijas

| Frase en español | Inglés actual | Hindi |
|---|---|---|
| Traducción automática, sin revisión humana. (aviso que se antepone a cada respuesta cuando la marca elige este idioma) | Translation machine-generated, not human-reviewed. | अनुवाद मशीन द्वारा तैयार किया गया है, मानव द्वारा समीक्षित नहीं। |
| Versión en el idioma pedido no disponible; se continúa con los ficheros en español. (línea de fallo seguro) | English version unavailable; continuing with the Spanish files. | हिन्दी संस्करण उपलब्ध नहीं है; स्पैनिश फ़ाइलों के साथ आगे बढ़ा जा रहा है। |
| Elaborado con asistencia de IA; requiere revisión humana. (nota de cierre de documentos con IA) | AI-assisted; requires human review. | AI की सहायता से तैयार; मानवीय समीक्षा आवश्यक है। |

## Dudas para una persona nativa

1. **«आप» con imperativo en `-ें` frente a infinitivo («पढ़ना», «जाँचना»).** Elegí la cortesía
   imperativa; algunas guías técnicas hindi usan el infinitivo como instrucción impersonal. ¿Cuál suena
   más natural en documentación para desarrolladores?
2. **«व्यक्ति» como «la persona».** Evita «उपयोगकर्ता», pero ¿suena demasiado abstracto en un texto
   técnico? ¿Prefiere la comunidad «उपयोगकर्ता» pese al masculino genérico?
3. **Pronombre «वे/उन्हें» con subjuntivo.** Es mi solución para no marcar género; no sé si en frases
   largas resulta forzado o ambiguo (¿plural real o singular honorífico?).
4. **Nivel de préstamo.** Escribí en devanagari «रिपॉज़िटरी», «कमिट», «ब्रांच», «मर्ज», «फ़ॉलबैक»,
   «कैटलॉग», pero usé calcos para «समीक्षा», «अनुमति», «प्रमाण». ¿Dónde pasa el corte en la práctica?
   En particular «पुश करना» frente a «भेजना/अपलोड करना», y «फ़ॉलबैक» frente a «वैकल्पिक/आरक्षित».
5. **«फ़ॉलबैक» y «सुरक्षित विफलता-व्यवहार» (fail-safe).** El segundo es un calco mío largo; ¿existe un
   término establecido? Lo mismo con «अनुबंध» (contrato de máquina) frente a «करार/समझौता».
6. **«प्रतिबिंब» para «espejo» (traducción) y «परिदृश्य» para «escenario».** Posible confusión con el
   sentido de «mirror» (ऑनलाइन दर्पण/मिरर) y con «स्थिति»; ¿mejor «मिरर»?
7. **Nota de IA: «AI» en latino frente a «एआई».** Elegí «AI» porque así se escribe en la práctica;
   ¿lo ven como mezcla de escrituras molesta en una frase fija?
8. **Danda y comillas.** «।» al final y comillas “ ” en prosa; ¿es habitual en documentación técnica
   hindi o se prefiere el punto «.»? El aviso de traducción automática, ¿con «मशीन द्वारा» o «मशीनी
   अनुवाद»?

**Seguridad (T6).** Mi hindi técnico es notablemente menos seguro que mi francés o mi inglés: puedo
producir texto gramatical y comprensible, pero no juzgo bien los registros, la naturalidad de los
calcos ni las convenciones reales de documentación en hindi; por eso se entrega como `borrador-ia`
(y, si la persona no tiene revisión nativa, como `experimental`) y exige revisión nativa antes de
cualquier uso profesional.

---

Elaborado con asistencia de IA; requiere revisión humana.

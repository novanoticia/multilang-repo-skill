#!/usr/bin/env python3
"""Valida catálogos de traducción en JSON (un fichero o una carpeta por idioma) frente a la referencia.

Para catálogos JSON propios (p. ej. de una skill o un plugin) o de i18next cuando el proyecto no tiene ya
un validador. Si el ecosistema ofrece el suyo (msgfmt --check, i18next-parser,
formatjs, lint de Android…), úsalo primero; este script no los sustituye.

Uso:
    python3 validar_catalogos.py DIR --referencia es [--marcadores llave|doble-llave|printf|ninguno]
                                 [--clave-meta _meta] [--estricto] [--json]

Descubrimiento (añadir un idioma = soltar un fichero):
  - modo plano: DIR/<idioma>.json            (es.json, en.json, pt-BR.json…)
  - modo carpetas: DIR/<idioma>/<espacio>.json  (es/common.json, en/common.json…)
  Los ficheros cuyo nombre no parece una etiqueta de idioma (p. ej. glosario.json) se ignoran y se informa.

Comprueba, por idioma y clave: claves ausentes o sobrantes; JSON inválido y claves duplicadas; tipos y
longitud de listas; valores vacíos y marcas TODO/FIXME; marcadores de interpolación (mismo conjunto, solo
con nombre); fragmentos entre comillas invertidas idénticos (contratos); URL, correos o etiquetas HTML que
aparecen solo en la traducción; textos idénticos a la referencia no declarados invariables; longitudes
atípicas; forma del fichero (UTF-8, BOM, salto final, NFC en traducciones); caracteres Unicode de control,
invisibles, bidireccionales y de etiqueta; claves con caracteres invisibles o escrituras mezcladas; y la
coherencia del estado del catálogo (un idioma "revisado" exige revisor).

Opciones para i18next: --marcadores doble-llave y --plurales sufijo (clave_one, clave_other…: cada idioma
puede usar sus propias categorías CLDR; «other» es obligatoria y ninguna forma puede inventar marcadores).
Metadatos por clave: "@clave": {"contexto": …, "riesgo": …, "invariable": true} en la referencia (estilo ARB).
Un idioma con _meta.estado = "experimental" puede estar incompleto: las claves que faltan dan un aviso de
cobertura parcial, no un error. --idiomas limita la validación a una lista explícita.

Límites declarados: no interpreta la sintaxis plural/select de ICU MessageFormat (ARB, formatjs) ni Fluent, ni
descubre ficheros con prefijo (app_en.arb): para esos formatos usa las herramientas de su ecosistema; no juzga la calidad de la traducción; las comprobaciones Unicode y
estructurales SEÑALAN para revisión humana, no demuestran ausencia de inyección ni de errores. Nunca
modifica ni "limpia" los ficheros.

Metadatos opcionales por catálogo (clave configurable, por defecto "_meta"; se excluye de la paridad):
    "_meta": {"estado": "borrador-ia", "redactado_por": "…", "revisado_por": "", "invariables": ["clave.x"]}
Las claves que empiezan por "@" (metadatos de ARB) también se excluyen de la paridad.

Códigos de salida: 0 sin errores; 1 hay errores (o avisos con --estricto); 2 error de uso.
Solo biblioteca estándar (Python 3.8+).
"""

import argparse
import json
import os
import re
import string
import sys
import unicodedata

ESTADOS = ("referencia", "borrador-ia", "experimental", "revisado")
ETIQUETA_IDIOMA = re.compile(r"^[A-Za-z]{2,3}(?:[-_][A-Za-z0-9]{2,8})*$")
IDIOMAS_RTL = {"ar", "he", "iw", "fa", "ur", "ps", "sd", "yi", "dv", "ckb", "ug", "syr", "nqo", "arc"}
ESCRITURAS_RTL = {"Arab", "Hebr", "Thaa", "Syrc", "Nkoo", "Adlm", "Rohg", "Mand", "Samr"}
# Lenguas que se escriben sin espacios y usan U+200B como indicación legítima de corte de línea.
IDIOMAS_CON_ZWSP = {"th", "km", "lo", "my", "bo", "dz"}
MARCAS_PENDIENTE = re.compile(r"\b(TODO|FIXME|TBD)\b")
# Plurales por sufijo (formato JSON v4 de i18next): clave_one, clave_other… Las categorías son las de CLDR.
PLURAL = re.compile(r"^(.*)_(zero|one|two|few|many|other)$")
# Una traducción rara vez triplica la referencia salvo en cadenas muy cortas; por eso se exige además
# una diferencia absoluta. Es una heurística para priorizar la revisión, no un criterio de error.
PROPORCION_LONGITUD = 3.0
DIFERENCIA_MINIMA = 40
URL = re.compile(r"(?:https?://|www\.)[^\s<>\"'`)\]]+|[\w.+-]+@[\w-]+\.[\w.-]+")
ETIQUETA_HTML = re.compile(r"</?([A-Za-z][A-Za-z0-9-]*)\b[^<>]*>")
CODIGO = re.compile(r"(`+)(.+?)(?<!`)\1(?!`)", re.S)
DOBLE_LLAVE = re.compile(r"\{\{(.*?)\}\}", re.S)
ANIDADO_I18NEXT = re.compile(r"\$t\([^)]*\)")
PRINTF = re.compile(
    r"%(?:\((?P<nombre>[^)]*)\)|(?P<posicion>\d+)\$)?[-#0 +']*(?:\*|\d+)?(?:\.(?:\*|\d+))?"
    r"(?:hh|h|ll|l|L|q|j|z|t)?(?P<conv>[diouxXeEfFgGaAcsrp@])")


class ErrorUso(Exception):
    pass


class Informe:
    def __init__(self):
        self.incidencias = []

    def add(self, severidad, idioma, fichero, clave, codigo, mensaje):
        self.incidencias.append({"severidad": severidad, "idioma": idioma, "fichero": fichero,
                                 "clave": clave, "codigo": codigo, "mensaje": mensaje})

    def contar(self, severidad):
        return sum(1 for i in self.incidencias if i["severidad"] == severidad)


def es_rtl(etiqueta):
    partes = re.split(r"[-_]", etiqueta)
    escritura = next((p.title() for p in partes[1:] if len(p) == 4 and p.isalpha()), None)
    if escritura:
        return escritura in ESCRITURAS_RTL
    return partes[0].lower() in IDIOMAS_RTL


def descubrir(directorio, ignorar):
    if not os.path.isdir(directorio):
        raise ErrorUso("no existe la carpeta %s" % directorio)
    entradas = sorted(e for e in os.listdir(directorio) if not e.startswith("."))
    ficheros = [e for e in entradas if e.endswith(".json") and os.path.isfile(os.path.join(directorio, e))]
    carpetas = [e for e in entradas if os.path.isdir(os.path.join(directorio, e))]
    ignorados = []
    idiomas = {}
    if ficheros and carpetas:
        carpetas_idioma = [c for c in carpetas if ETIQUETA_IDIOMA.match(c) and c not in ignorar]
        ficheros_idioma = [f for f in ficheros if ETIQUETA_IDIOMA.match(f[:-5]) and f not in ignorar]
        if carpetas_idioma and ficheros_idioma:
            raise ErrorUso("%s mezcla ficheros y carpetas de idioma; valida cada estructura por separado" % directorio)
        if carpetas_idioma:
            ficheros = []
        else:
            carpetas = []
    if ficheros:
        modo = "plano"
        for nombre in ficheros:
            etiqueta = nombre[:-5]
            if nombre in ignorar or not ETIQUETA_IDIOMA.match(etiqueta):
                ignorados.append(nombre)
                continue
            idiomas[etiqueta] = {"": os.path.join(directorio, nombre)}
    else:
        modo = "carpetas"
        for carpeta in carpetas:
            if carpeta in ignorar or not ETIQUETA_IDIOMA.match(carpeta):
                ignorados.append(carpeta + "/")
                continue
            ruta = os.path.join(directorio, carpeta)
            espacios = sorted(f for f in os.listdir(ruta) if f.endswith(".json") and not f.startswith("."))
            idiomas[carpeta] = {f: os.path.join(ruta, f) for f in espacios}
    return modo, idiomas, ignorados


def cargar(ruta, informe, idioma, nombre, permitir_bom):
    try:
        with open(ruta, "rb") as fichero:
            datos = fichero.read()
    except OSError as exc:
        informe.add("error", idioma, nombre, "", "lectura", str(exc))
        return None
    if datos.startswith(b"\xef\xbb\xbf"):
        informe.add("aviso" if permitir_bom else "error", idioma, nombre, "", "bom",
                    "el fichero empieza por BOM UTF-8")
        datos = datos[3:]
    try:
        texto = datos.decode("utf-8")
    except UnicodeDecodeError as exc:
        informe.add("error", idioma, nombre, "", "utf8-invalido", "no es UTF-8 válido (byte %d)" % exc.start)
        return None
    if texto and not texto.endswith("\n"):
        informe.add("aviso", idioma, nombre, "", "sin-salto-final", "falta el salto de línea final")
    duplicadas = []

    def sin_duplicados(pares):
        resultado = {}
        for clave, valor in pares:
            if clave in resultado:
                duplicadas.append(clave)
            resultado[clave] = valor
        return resultado

    try:
        objeto = json.loads(texto, object_pairs_hook=sin_duplicados)
    except ValueError as exc:
        informe.add("error", idioma, nombre, "", "json-invalido", str(exc))
        return None
    for clave in duplicadas:
        informe.add("error", idioma, nombre, clave, "clave-duplicada",
                    "clave repetida en el mismo objeto; JSON conserva solo la última")
    if not isinstance(objeto, dict):
        informe.add("error", idioma, nombre, "", "json-invalido", "el catálogo debe ser un objeto JSON")
        return None
    return objeto


def aplanar(objeto, clave_meta, prefijo=""):
    """Devuelve {ruta: valor}; las listas se registran con su longitud en la entrada ruta + '[]'."""
    plano = {}
    if isinstance(objeto, dict):
        for clave, valor in objeto.items():
            if not prefijo and clave == clave_meta:
                continue
            if clave.startswith("@"):
                continue
            ruta = clave if not prefijo else prefijo + "." + clave
            plano.update(aplanar(valor, clave_meta, ruta))
    elif isinstance(objeto, list):
        plano[prefijo + "[]"] = len(objeto)
        for indice, valor in enumerate(objeto):
            plano.update(aplanar(valor, clave_meta, "%s[%d]" % (prefijo, indice)))
    else:
        plano[prefijo] = objeto
    return plano


def metadatos_por_clave(objeto, prefijo=""):
    """Devuelve {ruta: dict} con los metadatos "@clave" (estilo ARB) de cualquier nivel."""
    encontrados = {}
    if isinstance(objeto, dict):
        for clave, valor in objeto.items():
            if clave.startswith("@@"):
                continue
            if clave.startswith("@") and isinstance(valor, dict):
                nombre = clave[1:]
                encontrados[nombre if not prefijo else prefijo + "." + nombre] = valor
            elif isinstance(valor, dict):
                encontrados.update(metadatos_por_clave(valor, clave if not prefijo else prefijo + "." + clave))
    return encontrados


def marcadores(texto, modo):
    """Devuelve (firma_comparable, problemas). firma None si el texto no se puede analizar."""
    problemas = []
    if modo == "ninguno":
        return (), problemas
    if modo == "llave":
        nombres = set()

        def recorrer(cadena, profundidad=0):
            for _, campo, especificacion, _ in string.Formatter().parse(cadena):
                if campo is None:
                    continue
                if campo == "" or campo.isdigit():
                    problemas.append("marcador sin nombre {%s}" % campo)
                elif not re.fullmatch(r"[^\W\d]\w*", campo):
                    problemas.append("marcador compuesto {%s}: usa solo nombres simples" % campo)
                nombres.add(campo)
                if especificacion and "{" in especificacion and profundidad < 2:
                    recorrer(especificacion, profundidad + 1)

        try:
            recorrer(texto)
        except ValueError as exc:
            return None, ["llaves mal formadas: %s (escribe {{ y }} para llaves literales)" % exc]
        return tuple(sorted(nombres)), problemas
    if modo == "doble-llave":
        nombres = set()
        resto = DOBLE_LLAVE.sub(" ", texto)
        if "{{" in resto or "}}" in resto:
            return None, ["{{ o }} sin pareja"]
        for interior in DOBLE_LLAVE.findall(texto):
            nombre = interior.strip().lstrip("-").strip().split(",")[0].strip()
            if not nombre:
                problemas.append("marcador {{}} vacío")
            nombres.add(nombre)
        nombres.update(ANIDADO_I18NEXT.findall(texto))
        return tuple(sorted(nombres)), problemas
    if modo == "printf":
        limpio = texto.replace("%%", "")
        con_nombre, posicionales, sin_nombre = set(), set(), []
        for coincidencia in PRINTF.finditer(limpio):
            if coincidencia.group("nombre") is not None:
                con_nombre.add((coincidencia.group("nombre"), coincidencia.group("conv")))
            elif coincidencia.group("posicion") is not None:
                posicionales.add((coincidencia.group("posicion"), coincidencia.group("conv")))
            else:
                sin_nombre.append(coincidencia.group("conv"))
        if len(sin_nombre) > 1:
            problemas.append("varios marcadores sin nombre ni posición: la traducción no puede reordenarlos")
        return (tuple(sorted(con_nombre)), tuple(sorted(posicionales)), tuple(sin_nombre)), problemas
    raise ErrorUso("modo de marcadores desconocido: %s" % modo)


def es_ideograma(caracter):
    punto = ord(caracter)
    return (0x4E00 <= punto <= 0x9FFF or 0x3400 <= punto <= 0x4DBF or 0x20000 <= punto <= 0x3134F
            or 0xF900 <= punto <= 0xFAFF)


def revisar_unicode(valor, idioma):
    """Devuelve una lista de (severidad, codigo, mensaje). Señala; nunca corrige."""
    hallazgos = {}

    def anotar(severidad, codigo, mensaje, posicion):
        entrada = hallazgos.setdefault(codigo, [severidad, mensaje, []])
        entrada[2].append(posicion)

    rtl = es_rtl(idioma)
    base = idioma.split("-")[0].split("_")[0].lower()
    pila = []
    indice = 0
    while indice < len(valor):
        caracter = valor[indice]
        punto = ord(caracter)
        if 0xD800 <= punto <= 0xDFFF:
            anotar("error", "sustituto-aislado", "sustituto UTF-16 aislado (texto corrupto)", indice)
        elif 0x202A <= punto <= 0x202E:
            anotar("aviso", "bidi-incrustacion",
                   "controles de incrustación o anulación bidireccional (U+202A–U+202E): pueden reordenar "
                   "visualmente el texto y ocultar su orden lógico; en texto RTL suelen bastar los "
                   "aislamientos U+2066–U+2069", indice)
            if punto == 0x202C:
                if pila and pila[-1] == "incrustacion":
                    pila.pop()
                else:
                    anotar("aviso", "bidi-desequilibrado", "control bidireccional sin pareja", indice)
            else:
                pila.append("incrustacion")
        elif 0x2066 <= punto <= 0x2069 or punto in (0x200E, 0x200F, 0x061C):
            if not rtl:
                anotar("info", "bidi-en-idioma-ltr",
                       "marcas o aislamientos bidireccionales en un idioma LTR: confirma que son intencionados",
                       indice)
            if 0x2066 <= punto <= 0x2068:
                pila.append("aislamiento")
            elif punto == 0x2069:
                if pila and pila[-1] == "aislamiento":
                    pila.pop()
                else:
                    anotar("aviso", "bidi-desequilibrado", "control bidireccional sin pareja", indice)
        elif 0xE0000 <= punto <= 0xE007F:
            inicio = indice
            while indice + 1 < len(valor) and 0xE0000 <= ord(valor[indice + 1]) <= 0xE007F:
                indice += 1
            es_bandera = (inicio > 0 and ord(valor[inicio - 1]) == 0x1F3F4 and ord(valor[indice]) == 0xE007F)
            if not es_bandera:
                anotar("error", "etiqueta-unicode",
                       "caracteres de etiqueta Unicode (U+E0000–U+E007F) fuera de una bandera: son invisibles "
                       "y pueden ocultar texto a la revisión humana", inicio)
        elif 0xE0100 <= punto <= 0xE01EF:
            if indice == 0 or not es_ideograma(valor[indice - 1]):
                anotar("aviso", "selector-variacion",
                       "selector de variación suplementario (U+E0100–U+E01EF) que no sigue a un ideograma",
                       indice)
        elif punto == 0x200B:
            if base not in IDIOMAS_CON_ZWSP:
                anotar("aviso", "invisible", "espacio de anchura cero (U+200B): confirma que es intencionado", indice)
        elif punto in (0x2060, 0xFEFF, 0x180E) or 0x2061 <= punto <= 0x2064:
            anotar("aviso", "invisible", "carácter invisible (U+%04X): confirma que es intencionado" % punto, indice)
        elif punto == 0x00AD:
            anotar("info", "guion-blando", "guion blando (U+00AD): legítimo para partir palabras; confírmalo", indice)
        elif unicodedata.category(caracter) == "Cc" and caracter not in "\n\t":
            anotar("aviso", "control", "carácter de control U+%04X" % punto, indice)
        indice += 1
    if pila:
        anotar("aviso", "bidi-desequilibrado", "controles bidireccionales abiertos sin cerrar", len(valor))
    return [(sev, cod, "%s (posiciones %s)" % (msg, ", ".join(map(str, pos[:5]))))
            for cod, (sev, msg, pos) in hallazgos.items()]


def escrituras(texto):
    conjunto = set()
    for caracter in texto:
        if caracter.isalpha():
            try:
                conjunto.add(unicodedata.name(caracter).split(" ")[0])
            except ValueError:
                conjunto.add("DESCONOCIDA")
    return conjunto


def revisar_clave(ruta, informe, idioma, nombre):
    if any(unicodedata.category(c) in ("Cf", "Cc", "Zl", "Zp") or (c.isspace() and c != " ") for c in ruta):
        informe.add("error", idioma, nombre, ruta, "clave-con-invisible",
                    "la clave contiene caracteres de control, invisibles o saltos")
    if len(escrituras(ruta)) > 1:
        informe.add("error", idioma, nombre, ruta, "clave-escrituras-mezcladas",
                    "la clave mezcla escrituras (%s): posible homógrafo en un contrato de máquina"
                    % ", ".join(sorted(escrituras(ruta))))


def tiene_letras(texto):
    return any(c.isalpha() for c in texto)


def validar(directorio, referencia, modo_marcadores="llave", clave_meta="_meta", ignorar=(),
            permitir_bom=False, plurales="ninguno", idiomas=None):
    informe = Informe()
    modo, catalogos, ignorados = descubrir(directorio, set(ignorar))
    for nombre in ignorados:
        informe.add("info", "", nombre, "", "ignorado", "no parece un catálogo de idioma; no se valida")
    if idiomas:
        pedidos = set(idiomas) | {referencia}
        for etiqueta in sorted(set(catalogos) - pedidos):
            informe.add("info", etiqueta, "", "", "ignorado", "no está en la lista de --idiomas; no se valida")
            del catalogos[etiqueta]
        for etiqueta in sorted(pedidos - set(catalogos)):
            informe.add("error", etiqueta, "", "", "idioma-no-encontrado", "está en --idiomas pero no hay catálogo")
    if referencia not in catalogos:
        raise ErrorUso("no se encuentra el catálogo de referencia '%s' en %s (encontrados: %s)"
                       % (referencia, directorio, ", ".join(sorted(catalogos)) or "ninguno"))
    espacios_ref = catalogos[referencia]
    for idioma in sorted(catalogos):
        for espacio in sorted(set(catalogos[idioma]) - set(espacios_ref)):
            informe.add("aviso", idioma, espacio, "", "fichero-sobrante", "no existe en la referencia")
    for espacio, ruta_ref in sorted(espacios_ref.items()):
        nombre_ref = os.path.relpath(ruta_ref, directorio)
        datos_ref = cargar(ruta_ref, informe, referencia, nombre_ref, permitir_bom)
        if datos_ref is None:
            continue
        plano_ref = aplanar(datos_ref, clave_meta)
        revisar_meta(datos_ref, clave_meta, informe, referencia, nombre_ref, plano_ref, True)
        meta_claves = metadatos_por_clave(datos_ref)
        for clave in sorted(meta_claves):
            if clave not in plano_ref:
                informe.add("aviso", referencia, nombre_ref, clave, "metadato-huerfano",
                            "hay metadatos «@%s» pero no existe esa clave" % clave.split(".")[-1])
        invariables_ref = {c for c, m in meta_claves.items() if m.get("invariable") is True}
        firmas_ref = {}
        for clave, valor in plano_ref.items():
            revisar_clave(clave, informe, referencia, nombre_ref)
            if isinstance(valor, str):
                if not valor.strip():
                    informe.add("error", referencia, nombre_ref, clave, "valor-vacio", "valor vacío en la referencia")
                firma, problemas = marcadores(valor, modo_marcadores)
                firmas_ref[clave] = firma
                for problema in problemas:
                    informe.add("aviso" if firma is not None else "error", referencia, nombre_ref, clave,
                                "marcador-mal-formado", problema)
                for sev, cod, msg in revisar_unicode(valor, referencia):
                    informe.add(sev, referencia, nombre_ref, clave, cod, msg)
                if not unicodedata.is_normalized("NFC", valor):
                    informe.add("info", referencia, nombre_ref, clave, "no-nfc",
                                "la referencia no está en NFC; no la normalices si eso cambia la salida por defecto")
        for idioma in sorted(catalogos):
            if idioma == referencia:
                continue
            ruta = catalogos[idioma].get(espacio)
            nombre = os.path.relpath(ruta, directorio) if ruta else os.path.join(idioma, espacio)
            if ruta is None:
                informe.add("error", idioma, nombre, "", "fichero-ausente",
                            "falta el fichero %s que existe en la referencia" % espacio)
                continue
            datos = cargar(ruta, informe, idioma, nombre, permitir_bom)
            if datos is None:
                continue
            plano = aplanar(datos, clave_meta)
            invariables = revisar_meta(datos, clave_meta, informe, idioma, nombre, plano_ref, False)
            meta = datos.get(clave_meta)
            experimental = isinstance(meta, dict) and meta.get("estado") == "experimental"
            comparar_idioma(plano_ref, firmas_ref, plano, informe, idioma, nombre, modo_marcadores,
                            invariables | invariables_ref, plurales, experimental)
    return {"directorio": directorio, "modo": modo, "referencia": referencia,
            "idiomas": sorted(catalogos), "incidencias": informe.incidencias,
            "resumen": {s: informe.contar(s) for s in ("error", "aviso", "info")}}


def revisar_meta(datos, clave_meta, informe, idioma, nombre, plano_ref, es_referencia):
    meta = datos.get(clave_meta)
    if meta is None:
        return set()
    if not isinstance(meta, dict):
        informe.add("error", idioma, nombre, clave_meta, "meta-invalida", "los metadatos deben ser un objeto")
        return set()
    estado = meta.get("estado")
    if estado is not None and estado not in ESTADOS:
        informe.add("error", idioma, nombre, clave_meta, "estado-invalido",
                    "estado '%s' no es uno de: %s" % (estado, ", ".join(ESTADOS)))
    if estado == "revisado":
        revisor = meta.get("revisado_por")
        if not (isinstance(revisor, str) and revisor.strip()) and not (isinstance(revisor, list) and revisor):
            informe.add("error", idioma, nombre, clave_meta, "revisado-sin-revisor",
                        "un catálogo 'revisado' exige 'revisado_por' con una persona identificada")
    if es_referencia and estado not in (None, "referencia"):
        informe.add("aviso", idioma, nombre, clave_meta, "estado-referencia",
                    "el catálogo de referencia debería tener estado 'referencia'")
    invariables = meta.get("invariables", [])
    if not isinstance(invariables, list):
        informe.add("error", idioma, nombre, clave_meta, "meta-invalida", "'invariables' debe ser una lista")
        return set()
    for clave in invariables:
        if clave not in plano_ref:
            informe.add("aviso", idioma, nombre, clave, "invariable-inexistente",
                        "declarada invariable pero no existe en la referencia")
    return set(invariables)


def nombres_de(firma, modo):
    return set(firma) if firma is not None and modo in ("llave", "doble-llave") else None


def comparar_idioma(plano_ref, firmas_ref, plano, informe, idioma, nombre, modo, invariables,
                    plurales="ninguno", experimental=False):
    ausentes = {c for c in set(plano_ref) - set(plano) if not c.endswith("[]")}
    sobrantes = {c for c in set(plano) - set(plano_ref) if not c.endswith("[]")}
    grupo = {}
    if plurales == "sufijo":
        def base(clave):
            m = PLURAL.match(clave)
            return (m.group(1), m.group(2)) if m else (None, None)
        bases_ref = {base(c)[0] for c in plano_ref if base(c)[0]}
        bases = {base(c)[0] for c in plano if base(c)[0]}
        for clave in list(ausentes):
            b, _ = base(clave)
            if b in bases:
                ausentes.discard(clave)            # ese idioma no usa esa categoría; «other» se exige aparte
        for clave in list(sobrantes):
            b, _ = base(clave)
            if b in bases_ref:
                sobrantes.discard(clave)           # categoría propia de ese idioma
        for b in sorted(bases_ref & bases):
            if b + "_other" not in plano:
                informe.add("error", idioma, nombre, b, "plural-sin-other", "falta la forma «%s_other»" % b)
        for clave in plano:
            b, _ = base(clave)
            if b in bases_ref:
                union = set()
                for c in plano_ref:
                    if base(c)[0] == b and nombres_de(firmas_ref.get(c), modo) is not None:
                        union |= nombres_de(firmas_ref.get(c), modo)
                grupo[clave] = (b, union)
    if experimental and ausentes:
        informe.add("aviso", idioma, nombre, "", "cobertura-parcial",
                    "idioma experimental: faltan %d de %d claves (no se publica como completo; D8)"
                    % (len(ausentes), len([c for c in plano_ref if not c.endswith("[]")])))
    else:
        for clave in sorted(ausentes):
            informe.add("error", idioma, nombre, clave, "clave-ausente", "falta la clave")
    for clave in sorted(sobrantes):
        informe.add("error", idioma, nombre, clave, "clave-sobrante", "la clave no existe en la referencia")
    pares = [(c, plano_ref[c]) for c in sorted(set(plano) & set(plano_ref))]
    pares += [(c, plano_ref.get(grupo[c][0] + "_other", "")) for c in sorted(set(plano) - set(plano_ref)) if c in grupo]
    for clave, valor_ref in pares:
        valor = plano[clave]
        if clave.endswith("[]"):
            if valor != valor_ref:
                informe.add("error", idioma, nombre, clave[:-2], "lista-longitud",
                            "la lista tiene %d entradas y la referencia %d" % (valor, valor_ref))
            continue
        revisar_clave(clave, informe, idioma, nombre)
        if type(valor) is not type(valor_ref):
            informe.add("error", idioma, nombre, clave, "tipo-distinto",
                        "tipo %s; en la referencia %s" % (type(valor).__name__, type(valor_ref).__name__))
            continue
        if not isinstance(valor, str):
            if valor != valor_ref:
                informe.add("aviso", idioma, nombre, clave, "valor-de-maquina-distinto",
                            "valor no textual distinto de la referencia: %r frente a %r" % (valor, valor_ref))
            continue
        if not valor.strip():
            informe.add("error", idioma, nombre, clave, "valor-vacio", "valor vacío")
            continue
        if MARCAS_PENDIENTE.search(valor) and not MARCAS_PENDIENTE.search(valor_ref):
            informe.add("error", idioma, nombre, clave, "marca-pendiente", "contiene una marca de trabajo pendiente")
        firma, problemas = marcadores(valor, modo)
        if firma is None:
            informe.add("error", idioma, nombre, clave, "marcador-mal-formado", "; ".join(problemas))
        else:
            for problema in problemas:
                informe.add("aviso", idioma, nombre, clave, "marcador-mal-formado", problema)
            if clave in grupo and nombres_de(firma, modo) is not None:
                # Plural: una forma puede omitir el número (p. ej. «one» en árabe), pero no inventar
                # marcadores, y la forma «other» conserva todos los de la referencia.
                b, union = grupo[clave]
                if not nombres_de(firma, modo) <= union:
                    informe.add("error", idioma, nombre, clave, "marcadores-distintos",
                                "marcadores %s que no están en el grupo plural de la referencia %s"
                                % (sorted(nombres_de(firma, modo) - union), sorted(union)))
                referencia_other = nombres_de(firmas_ref.get(b + "_other"), modo)
                if clave == b + "_other" and referencia_other is not None and not referencia_other <= nombres_de(firma, modo):
                    informe.add("error", idioma, nombre, clave, "marcadores-distintos",
                                "la forma «other» pierde %s" % sorted(referencia_other - nombres_de(firma, modo)))
            elif firmas_ref.get(clave) is not None and firma != firmas_ref[clave]:
                informe.add("error", idioma, nombre, clave, "marcadores-distintos",
                            "marcadores %s; en la referencia %s" % (firma, firmas_ref[clave]))
        codigo, codigo_ref = sorted(m[1] for m in CODIGO.findall(valor)), sorted(m[1] for m in CODIGO.findall(valor_ref))
        if codigo != codigo_ref:
            informe.add("error", idioma, nombre, clave, "codigo-distinto",
                        "lo que va entre comillas invertidas es contrato y debe coincidir: %s frente a %s"
                        % (codigo, codigo_ref))
        nuevas = sorted(set(u.rstrip(".,;:!?") for u in URL.findall(valor))
                        - set(u.rstrip(".,;:!?") for u in URL.findall(valor_ref)))
        if nuevas:
            informe.add("aviso", idioma, nombre, clave, "url-nueva",
                        "URL o correos que no están en la referencia: %s" % ", ".join(nuevas))
        etiquetas, etiquetas_ref = sorted(ETIQUETA_HTML.findall(valor)), sorted(ETIQUETA_HTML.findall(valor_ref))
        if etiquetas != etiquetas_ref:
            informe.add("aviso", idioma, nombre, clave, "etiquetas-html-distintas",
                        "etiquetas %s; en la referencia %s" % (etiquetas, etiquetas_ref))
        if valor == valor_ref and clave not in invariables and tiene_letras(valor):
            informe.add("aviso", idioma, nombre, clave, "identico-a-referencia",
                        "idéntico a la referencia: tradúcelo o decláralo invariable con su razón")
        if len(valor) > PROPORCION_LONGITUD * max(len(valor_ref), 1) and len(valor) - len(valor_ref) > DIFERENCIA_MINIMA:
            informe.add("aviso", idioma, nombre, clave, "longitud-atipica",
                        "%d caracteres frente a %d en la referencia: revísalo (texto añadido)" % (len(valor), len(valor_ref)))
        for sev, cod, msg in revisar_unicode(valor, idioma):
            informe.add(sev, idioma, nombre, clave, cod, msg)
        if not unicodedata.is_normalized("NFC", valor):
            informe.add("aviso", idioma, nombre, clave, "no-nfc", "la traducción no está en Unicode NFC")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Valida catálogos JSON de traducción frente a la referencia.")
    parser.add_argument("directorio", help="carpeta con <idioma>.json o <idioma>/<espacio>.json")
    parser.add_argument("--referencia", required=True, help="etiqueta del catálogo de referencia (p. ej. es)")
    parser.add_argument("--marcadores", default="llave", choices=("llave", "doble-llave", "printf", "ninguno"),
                        help="sintaxis de interpolación: llave = {nombre}; doble-llave = {{nombre}}; "
                             "printf = %%s/%%(nombre)s (por defecto: %(default)s)")
    parser.add_argument("--clave-meta", default="_meta", help="clave de metadatos del catálogo (por defecto: %(default)s)")
    parser.add_argument("--ignorar", default="", help="ficheros o carpetas a ignorar, separados por comas")
    parser.add_argument("--idiomas", default="", help="validar solo estos idiomas, separados por comas (evita tomar "
                        "por idioma un fichero auxiliar de 2 o 3 letras como faq.json)")
    parser.add_argument("--plurales", default="ninguno", choices=("ninguno", "sufijo"),
                        help="sufijo = plurales por sufijo de i18next (clave_one, clave_other…): la paridad se "
                             "comprueba por grupo y cada idioma usa sus categorías CLDR (por defecto: %(default)s)")
    parser.add_argument("--permitir-bom", action="store_true", help="tratar el BOM como aviso y no como error")
    parser.add_argument("--estricto", action="store_true", help="los avisos también hacen fallar la validación")
    parser.add_argument("--json", action="store_true", help="salida JSON")
    args = parser.parse_args(argv)
    try:
        resultado = validar(args.directorio, args.referencia, args.marcadores, args.clave_meta,
                            [x.strip() for x in args.ignorar.split(",") if x.strip()], args.permitir_bom,
                            args.plurales, [x.strip() for x in args.idiomas.split(",") if x.strip()] or None)
    except ErrorUso as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    resumen = resultado["resumen"]
    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        print("Catálogos en %s (modo %s) · referencia: %s · idiomas: %s" % (
            resultado["directorio"], resultado["modo"], resultado["referencia"], ", ".join(resultado["idiomas"])))
        orden = {"error": 0, "aviso": 1, "info": 2}
        for inc in sorted(resultado["incidencias"], key=lambda i: (orden[i["severidad"]], i["idioma"], i["clave"])):
            print("[%s] %s %s %s %s: %s" % (inc["severidad"].upper(), inc["idioma"] or "-", inc["fichero"],
                                            inc["clave"] or "-", inc["codigo"], inc["mensaje"]))
        print("Resumen: %d error(es), %d aviso(s), %d informativo(s)." % (resumen["error"], resumen["aviso"], resumen["info"]))
    if resumen["error"] or (args.estricto and resumen["aviso"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

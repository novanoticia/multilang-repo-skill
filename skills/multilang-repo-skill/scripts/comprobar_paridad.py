#!/usr/bin/env python3
"""Comprueba que una traducción de un fichero Markdown conserva la estructura de su original.

Pensado para proyectos de instrucciones (SKILL.md, referencias, plantillas) cuya traducción es un
espejo del original: la prosa cambia, pero lo que consume una máquina o ancla las reglas no.

Uso:
    python3 comprobar_paridad.py --arbol RAIZ_ORIGINAL RAIZ_TRADUCCION [--completo]
    python3 comprobar_paridad.py --par ORIGINAL TRADUCCION [--nota-ia TEXTO] [--raiz-es DIR --raiz-trad DIR]
    python3 comprobar_paridad.py --hash ORIGINAL        # imprime la huella para la cabecera
    (todos admiten --json; --arbol y --par admiten --estricto)

--par resuelve los enlaces relativos desde la carpeta de cada fichero; para un fichero dentro de una
subcarpeta (references/…) indica las raíces de los dos árboles con --raiz-es y --raiz-trad.
--arbol compara SKILL.md, references/*.md y assets/*.md del original con el mismo fichero bajo la
raíz de la traducción (p. ej. skills/x y skills/x/i18n/en). Un fichero sin traducir es un aviso, o
un error con --completo. Un fichero traducido sin original es un error.

Cada traducción empieza (en sus 5 primeras líneas) por una cabecera con la huella del original:
    <!-- i18n fuente-sha256=0123456789ab estado=borrador-ia -->
    <!-- i18n fuente-sha256=0123456789ab estado=revisado-humano revisor=Nombre -->
La huella son los 12 primeros dígitos del SHA-256 del original; si el original cambia, la
traducción queda desfasada hasta que se revise y se actualice. Este script no escribe ficheros:
obtén la huella con --hash y escríbela tú.

Qué comprueba (error salvo que se diga lo contrario):
  ids_difieren           recuento de identificadores de regla (R1, D4, Doc3…) fuera de bloques de código
  marcas_difieren        recuento de marcas de módulo literales ([instrucciones], [híbrido]…)
  estructura_difiere     secuencia de niveles de encabezado
  tablas_difieren        número de líneas de tabla
  bloques_difieren       bloques de código: número, lenguaje y, si tienen lenguaje, su contenido sin
                         líneas de comentario y, en shell, sin el comentario del final de línea (los
                         bloques sin lenguaje solo cuentan, su texto se traduce)
  enlaces_difieren       destinos de enlace, sin fragmento y con las rutas relativas resueltas
  enlace_roto            (solo --arbol) enlace relativo de la traducción que no existe en disco
  cabecera_* / fuente_desfasada / estado_sin_revisor / nota_ia_ausente / no_utf8
  (una línea de prosa que contenga <!-- i18n:exento --> queda fuera de todas las comprobaciones de
   contenido; sirve para lo que difiere por diseño, como el enlace «también en inglés» y su espejo. Se
   ve en el diff y debe usarse en las dos versiones)
  texto_sin_traducir     AVISO: líneas con letras propias del español (ñ, ¿, ¡, vocales con tilde)
Qué NO comprueba: que la traducción sea correcta, fiel ni completa en sentido; solo que no ha roto la
estructura. Una traducción con paridad perfecta puede seguir siendo mala.

Códigos de salida: 0 sin errores; 1 con errores (con --estricto, también con avisos);
2 error de uso o de lectura. Solo biblioteca estándar (Python 3.8+). No escribe ficheros.
"""

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter

MODULOS = ("ecosistema", "programa", "instrucciones", "híbrido", "rtl-escrituras", "seguridad",
           "contenido", "alto-riesgo", "documentación", "paquete", "publicación", "delegación")
RE_ID = re.compile(r"(?<![\w/.\-])(?:Doc[1-9]|[RDPTCSGM][0-9]{1,2})(?!\w)")
RE_MARCA = re.compile(r"\[(%s)\](?!\()" % "|".join(re.escape(m) for m in MODULOS))
RE_ENLACE = re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
RE_APERTURA = re.compile(r"^ {0,3}(`{3,})(.*)$")
RE_ENCABEZADO = re.compile(r"^(#{1,6})\s+\S")
RE_CABECERA = re.compile(
    r"^<!-- i18n fuente-sha256=([0-9a-f]{12}) estado=(borrador-ia|revisado-humano)(?: revisor=(\S[^>]*?))? -->$")
LETRAS_ESPANOL = "ñÑ¿¡áéíóúÁÉÍÓÚü"
RE_ESPANOL = re.compile("[" + re.escape(LETRAS_ESPANOL) + "]")
RE_CODIGO_EN_LINEA = re.compile(r"`[^`]*`")
LENGUAJES_DE_PROSA = ("text", "txt", "markdown", "md")
MARCA_EXENTA = "<!-- i18n:exento -->"
LENGUAJES_DE_SHELL = ("bash", "sh", "shell", "zsh", "console")
MAX_EJEMPLOS = 5


class ErrorUso(Exception):
    """Error de invocación o de lectura: termina con código 2."""


def hash_fuente(datos):
    return hashlib.sha256(datos).hexdigest()[:12]


def incidencia(codigo, severidad, mensaje):
    return {"codigo": codigo, "severidad": severidad, "mensaje": mensaje}


def separar(texto):
    """Devuelve (prosa, bloques): prosa = [(nº de línea, texto)], bloques = [(info, [líneas])]."""
    prosa, bloques, actual, cierre = [], [], None, 0
    for n, linea in enumerate(texto.splitlines(), 1):
        if actual is None:
            apertura = RE_APERTURA.match(linea)
            if apertura:
                actual, cierre = (apertura.group(2).strip(), []), len(apertura.group(1))
            else:
                prosa.append((n, linea))
        else:
            resto = linea.strip()
            if len(resto) >= cierre and resto == "`" * len(resto):
                bloques.append(actual)
                actual = None
            else:
                actual[1].append(linea)
    if actual is not None:
        bloques.append(actual)
    return prosa, bloques


def es_comentario(linea):
    corta = linea.strip()
    return corta.startswith(("#", "//", "<!--"))


def quitar_comentario_final(linea):
    """En shell, corta el comentario que empieza en un «#» precedido de espacio y fuera de comillas."""
    comilla = ""
    for i, c in enumerate(linea):
        if comilla:
            if c == comilla:
                comilla = ""
        elif c in "\"'":
            comilla = c
        elif c == "#" and i > 0 and linea[i - 1] in " \t":
            return linea[:i].rstrip()
    return linea


def contenido_comparable(info, lineas):
    lenguaje = info.split()[0].lower() if info.split() else ""
    if lenguaje == "" or lenguaje in LENGUAJES_DE_PROSA:
        return None
    if lenguaje in LENGUAJES_DE_SHELL:
        lineas = [quitar_comentario_final(l) for l in lineas]
    return tuple(l.rstrip() for l in lineas if l.strip() and not es_comentario(l))


def regex_espanol(tolera=""):
    """Letras propias del español, sin las que la lengua de destino comparte (p. ej. «é» en francés)."""
    letras = "".join(c for c in LETRAS_ESPANOL if c not in tolera)
    return re.compile("[" + re.escape(letras) + "]")


def analizar(texto, tolera=""):
    prosa, bloques = separar(texto)
    prosa = [(n, l) for n, l in prosa if MARCA_EXENTA not in l]
    sin_destinos = [(n, RE_ENLACE.sub("](#)", l)) for n, l in prosa]
    juntas = "\n".join(l for _, l in sin_destinos)
    return {
        "ids": Counter(RE_ID.findall(juntas)),
        "marcas": Counter(RE_MARCA.findall(juntas)),
        "niveles": [len(RE_ENCABEZADO.match(l).group(1)) for _, l in prosa if RE_ENCABEZADO.match(l)],
        "tablas": sum(1 for _, l in prosa if l.lstrip().startswith("|")),
        "bloques": [(info.split()[0].lower() if info.split() else "", contenido_comparable(info, lineas))
                    for info, lineas in bloques],
        "enlaces": [m for _, l in prosa for m in RE_ENLACE.findall(l)],
        "sin_traducir": [n for n, l in sin_destinos
                         if regex_espanol(tolera).search(RE_MARCA.sub("", RE_CODIGO_EN_LINEA.sub("", l)))],
    }


def normalizar_enlace(destino, directorio, raiz_es, raiz_trad):
    if re.match(r"^[A-Za-z][A-Za-z0-9+.\-]*:", destino):
        return destino
    ruta = destino.split("#", 1)[0]
    if ruta == "":
        return "#"
    try:
        absoluta = os.path.normpath(os.path.join(directorio, ruta))
        if raiz_trad and raiz_trad != raiz_es and (absoluta == raiz_trad or absoluta.startswith(raiz_trad + os.sep)):
            absoluta = os.path.normpath(os.path.join(raiz_es, os.path.relpath(absoluta, raiz_trad)))
        return os.path.relpath(absoluta, raiz_es)
    except ValueError:
        return destino


def decodificar(datos):
    try:
        return datos.decode("utf-8")
    except UnicodeDecodeError:
        return None


def quitar_cabecera(texto):
    return "\n".join(l for l in texto.split("\n") if not l.startswith("<!-- i18n fuente"))


def diferencias(a, b):
    """Resumen corto de las claves cuyo recuento difiere entre dos Counter."""
    claves = sorted(k for k in set(a) | set(b) if a[k] != b[k])
    return ", ".join("%s (original %d, traducción %d)" % (k, a[k], b[k]) for k in claves[:MAX_EJEMPLOS]) + \
        (" …" if len(claves) > MAX_EJEMPLOS else "")


def revisar_cabecera(es_datos, trad_texto):
    primeras = trad_texto.split("\n")[:5]
    candidatas = [l.strip() for l in primeras if l.strip().startswith("<!-- i18n fuente")]
    if not candidatas:
        return [incidencia("cabecera_ausente", "error",
                           "falta la cabecera «<!-- i18n fuente-sha256=… estado=… -->» en las 5 primeras líneas")]
    m = RE_CABECERA.match(candidatas[0])
    if not m:
        return [incidencia("cabecera_mal_formada", "error",
                           "la cabecera no cumple el formato (huella de 12 hex y estado borrador-ia o revisado-humano)")]
    incs = []
    if m.group(1) != hash_fuente(es_datos):
        incs.append(incidencia("fuente_desfasada", "error",
                               "el original ya no coincide con la huella %s (ahora %s): revisa la traducción y actualízala"
                               % (m.group(1), hash_fuente(es_datos))))
    if m.group(2) == "revisado-humano" and not (m.group(3) or "").strip():
        incs.append(incidencia("estado_sin_revisor", "error", "«revisado-humano» exige revisor=<nombre> en la cabecera"))
    return incs


def comparar(es, trad, dir_es="/r", dir_trad="/r/i18n/en", raiz_es="/r", raiz_trad="/r/i18n/en", nota_ia=None, tolera=""):
    """Compara los bytes de un original con los de su traducción. Devuelve una lista de incidencias."""
    es_texto, trad_texto = decodificar(es), decodificar(trad)
    if es_texto is None or trad_texto is None:
        quien = "el original" if es_texto is None else "la traducción"
        return [incidencia("no_utf8", "error", "%s no es UTF-8 válido" % quien)]
    incs = revisar_cabecera(es, trad_texto)
    a, b = analizar(es_texto), analizar(quitar_cabecera(trad_texto), tolera)
    if a["ids"] != b["ids"]:
        incs.append(incidencia("ids_difieren", "error", "identificadores: " + diferencias(a["ids"], b["ids"])))
    if a["marcas"] != b["marcas"]:
        incs.append(incidencia("marcas_difieren", "error", "marcas de módulo: " + diferencias(a["marcas"], b["marcas"])))
    if a["niveles"] != b["niveles"]:
        pos = next((i for i, (x, y) in enumerate(zip(a["niveles"], b["niveles"])) if x != y), min(len(a["niveles"]), len(b["niveles"])))
        incs.append(incidencia("estructura_difiere", "error",
                               "encabezados: original %d, traducción %d; primera diferencia en el encabezado nº %d"
                               % (len(a["niveles"]), len(b["niveles"]), pos + 1)))
    if a["tablas"] != b["tablas"]:
        incs.append(incidencia("tablas_difieren", "error", "líneas de tabla: original %d, traducción %d" % (a["tablas"], b["tablas"])))
    if a["bloques"] != b["bloques"]:
        if len(a["bloques"]) != len(b["bloques"]):
            detalle = "original %d, traducción %d" % (len(a["bloques"]), len(b["bloques"]))
        else:
            n = next(i for i, (x, y) in enumerate(zip(a["bloques"], b["bloques"])) if x != y)
            detalle = "el bloque nº %d difiere en su lenguaje o en su contenido" % (n + 1)
        incs.append(incidencia("bloques_difieren", "error", "bloques de código: " + detalle))
    ea = Counter(normalizar_enlace(d, dir_es, raiz_es, raiz_trad) for d in a["enlaces"])
    eb = Counter(normalizar_enlace(d, dir_trad, raiz_es, raiz_trad) for d in b["enlaces"])
    if ea != eb:
        incs.append(incidencia("enlaces_difieren", "error", "destinos de enlace: " + diferencias(ea, eb)))
    if nota_ia is not None:
        lineas = [l.strip() for l in trad_texto.split("\n") if l.strip()]
        if not lineas or lineas[-1] != nota_ia:
            incs.append(incidencia("nota_ia_ausente", "error", "el documento debe terminar con «%s»" % nota_ia))
    if b["sin_traducir"]:
        ejemplos = ", ".join(str(n) for n in b["sin_traducir"][:MAX_EJEMPLOS])
        incs.append(incidencia("texto_sin_traducir", "aviso",
                               "%d línea(s) con letras propias del español (líneas del fichero sin cabecera: %s)"
                               % (len(b["sin_traducir"]), ejemplos)))
    return incs


def listar_originales(raiz_es):
    if not os.path.isfile(os.path.join(raiz_es, "SKILL.md")):
        raise ErrorUso("no encuentro SKILL.md en %s" % raiz_es)
    rutas = ["SKILL.md"]
    for sub in ("references", "assets"):
        carpeta = os.path.join(raiz_es, sub)
        if os.path.isdir(carpeta):
            rutas += [sub + "/" + n for n in sorted(os.listdir(carpeta)) if n.endswith(".md")]
    return rutas


def listar_traducidos(raiz_trad):
    rutas = []
    for base, _, nombres in os.walk(raiz_trad):
        for n in nombres:
            if n.endswith(".md"):
                rutas.append(os.path.relpath(os.path.join(base, n), raiz_trad).replace(os.sep, "/"))
    return sorted(rutas)


def leer(ruta):
    try:
        with open(ruta, "rb") as f:
            return f.read()
    except OSError as exc:
        raise ErrorUso(str(exc))


def resumir(ficheros):
    todas = [i for f in ficheros for i in f["incidencias"]]
    return {"ficheros": ficheros, "errores": sum(1 for i in todas if i["severidad"] == "error"),
            "avisos": sum(1 for i in todas if i["severidad"] == "aviso")}


def comprobar_arbol(raiz_es, raiz_trad, completo=False, nota_ia=None, tolera=""):
    raiz_es, raiz_trad = os.path.abspath(raiz_es), os.path.abspath(raiz_trad)
    originales = listar_originales(raiz_es)
    traducidos = listar_traducidos(raiz_trad) if os.path.isdir(raiz_trad) else []
    ficheros = []
    for rel in originales:
        ruta_trad = os.path.join(raiz_trad, rel)
        if not os.path.isfile(ruta_trad):
            ficheros.append({"ruta": rel, "incidencias": [incidencia(
                "traduccion_ausente", "error" if completo else "aviso", "no hay traducción de este fichero")]})
            continue
        es_datos, trad_datos = leer(os.path.join(raiz_es, rel)), leer(ruta_trad)
        dir_es, dir_trad = os.path.dirname(os.path.join(raiz_es, rel)), os.path.dirname(ruta_trad)
        incs = comparar(es_datos, trad_datos, dir_es, dir_trad, raiz_es, raiz_trad, nota_ia, tolera)
        texto = decodificar(trad_datos)
        if texto is not None:
            for destino in analizar(quitar_cabecera(texto))["enlaces"]:
                ruta = destino.split("#", 1)[0]
                if ruta and not re.match(r"^[A-Za-z][A-Za-z0-9+.\-]*:", ruta) and \
                        not os.path.exists(os.path.join(dir_trad, ruta)):
                    incs.append(incidencia("enlace_roto", "error", "el enlace «%s» no existe en disco" % destino))
        ficheros.append({"ruta": rel, "incidencias": incs})
    for rel in traducidos:
        if rel not in originales:
            ficheros.append({"ruta": rel, "incidencias": [incidencia(
                "traduccion_sin_original", "error", "hay una traducción sin fichero original")]})
    return resumir(ficheros)


def comprobar_par(ruta_es, ruta_trad, nota_ia=None, raiz_es=None, raiz_trad=None, tolera=""):
    es_datos, trad_datos = leer(ruta_es), leer(ruta_trad)
    for nombre, datos in (("original", es_datos), ("traducción", trad_datos)):
        if decodificar(datos) is None:
            raise ErrorUso("el %s no es UTF-8 válido" % nombre)
    dir_es, dir_trad = os.path.dirname(os.path.abspath(ruta_es)), os.path.dirname(os.path.abspath(ruta_trad))
    raiz_es = os.path.abspath(raiz_es) if raiz_es else dir_es
    raiz_trad = os.path.abspath(raiz_trad) if raiz_trad else dir_trad
    incs = comparar(es_datos, trad_datos, dir_es, dir_trad, raiz_es, raiz_trad, nota_ia, tolera)
    return resumir([{"ruta": os.path.basename(ruta_trad), "incidencias": incs}])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Comprueba que una traducción conserva la estructura de su original.")
    modo = parser.add_mutually_exclusive_group(required=True)
    modo.add_argument("--arbol", nargs=2, metavar=("RAIZ_ORIGINAL", "RAIZ_TRADUCCION"), help="compara dos árboles espejo")
    modo.add_argument("--par", nargs=2, metavar=("ORIGINAL", "TRADUCCION"), help="compara dos ficheros")
    modo.add_argument("--hash", metavar="ORIGINAL", help="imprime la huella del original para la cabecera")
    parser.add_argument("--raiz-es", metavar="DIR", help="con --par, raíz del original (por defecto, la carpeta del fichero)")
    parser.add_argument("--raiz-trad", metavar="DIR", help="con --par, raíz de la traducción (por defecto, la carpeta del fichero)")
    parser.add_argument("--completo", action="store_true", help="con --arbol, un fichero sin traducir es un error")
    parser.add_argument("--nota-ia", metavar="TEXTO", help="línea con la que debe terminar la traducción")
    parser.add_argument("--tolera-letras", default="", metavar="LETRAS",
                        help="letras del español que la lengua de destino también usa y no deben avisar como texto sin traducir (p. ej. éÉ para el francés)")
    parser.add_argument("--estricto", action="store_true", help="los avisos también hacen fallar")
    parser.add_argument("--json", action="store_true", help="salida JSON")
    args = parser.parse_args(argv)
    try:
        if (args.raiz_es or args.raiz_trad) and not args.par:
            raise ErrorUso("--raiz-es y --raiz-trad solo se usan con --par")
        if args.hash:
            print(hash_fuente(leer(args.hash)))
            return 0
        resultado = (comprobar_arbol(args.arbol[0], args.arbol[1], args.completo, args.nota_ia, args.tolera_letras) if args.arbol
                     else comprobar_par(args.par[0], args.par[1], args.nota_ia, args.raiz_es, args.raiz_trad, args.tolera_letras))
    except ErrorUso as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        for f in resultado["ficheros"]:
            print("%s: %s" % (f["ruta"], "sin incidencias" if not f["incidencias"] else ""))
            for i in f["incidencias"]:
                print("  [%s] %s: %s" % (i["severidad"].upper(), i["codigo"], i["mensaje"]))
        print("Resultado: %d error(es), %d aviso(s)" % (resultado["errores"], resultado["avisos"]))
    return 1 if resultado["errores"] or (args.estricto and resultado["avisos"]) else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Comprueba que un fichero de texto solo difiere de su original por bloques añadidos y delimitados.

Pensado para proyectos de instrucciones (SKILL.md, prompts, plantillas Markdown) en los que la
internacionalización se hace con adiciones delimitadas y el texto original no debe cambiar.

Uso:
    python3 verificar_adiciones.py ORIGINAL MODIFICADO
    python3 verificar_adiciones.py --git BASE MODIFICADO        # original = git show BASE:<ruta>
    python3 verificar_adiciones.py --git BASE MODIFICADO --reemplazos REEMPLAZOS.json --json

Qué comprueba:
  1. Los marcadores de inicio y fin ocupan líneas propias, están equilibrados y no se anidan.
  2. Ningún marcador cae dentro del frontmatter YAML (allí un comentario HTML no es comentario).
  3. Al quitar los bloques, el resultado es idéntico byte a byte al original (incluidos los finales
     de línea), salvo los reemplazos aprobados. Si un bloque está rodeado de líneas en blanco, se
     descuenta una de ellas: es la separación que exige Markdown al insertar un bloque.
  4. Opcionalmente, que el tamaño total de los bloques no supere un presupuesto (--max-bytes).
Qué NO comprueba: la calidad, el sentido ni la ubicación correcta del texto añadido.

Fichero de reemplazos aprobados (JSON). Las líneas se numeran sobre el ORIGINAL, desde 1:
    {"reemplazos": [
      {"linea": 12, "texto": "contenido exacto de la nueva línea", "motivo": "..."},
      {"linea": 30, "patron": "^version: \\\\d+\\\\.\\\\d+\\\\.\\\\d+$", "motivo": "versión mecanizada"},
      {"linea": 41, "eliminar": true, "motivo": "..."}
    ]}

Códigos de salida: 0 sin incidencias; 1 diferencias no aprobadas o bloques mal formados;
2 error de uso o de lectura. Solo biblioteca estándar (Python 3.8+). No modifica ningún fichero.
"""

import argparse
import difflib
import json
import os
import re
import subprocess
import sys

INICIO_POR_DEFECTO = "<!-- i18n:inicio -->"
FIN_POR_DEFECTO = "<!-- i18n:fin -->"


class ErrorUso(Exception):
    """Error de invocación o de lectura: termina con código 2."""


def leer_lineas(datos, nombre):
    """Decodifica UTF-8 estricto y separa en (contenido, final_de_línea) conservando los bytes."""
    try:
        texto = datos.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ErrorUso("%s no es UTF-8 válido (byte %d)" % (nombre, exc.start))
    lineas = []
    # Solo «\n» separa líneas, como en git y en los editores: str.splitlines también cortaría en \f,
    # \v, U+2028… y desplazaría la numeración de los reemplazos aprobados.
    for bruta in re.findall(r"[^\n]*\n|[^\n]+$", texto):
        contenido = bruta.rstrip("\r\n")
        lineas.append((contenido, bruta[len(contenido):]))
    return lineas


def leer_original_git(revision, ruta_modificado):
    carpeta = os.path.dirname(os.path.abspath(ruta_modificado))
    especificacion = "%s:./%s" % (revision, os.path.basename(ruta_modificado))
    try:
        proceso = subprocess.run(
            ["git", "show", especificacion], cwd=carpeta,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
    except OSError as exc:
        raise ErrorUso("no se pudo ejecutar git: %s" % exc)
    if proceso.returncode != 0:
        raise ErrorUso("git show %s falló: %s" % (especificacion, proceso.stderr.decode("utf-8", "replace").strip()))
    return proceso.stdout


def cargar_reemplazos(ruta):
    if not ruta:
        return {}
    try:
        with open(ruta, "rb") as fichero:
            datos = json.loads(fichero.read().decode("utf-8"))
    except (OSError, ValueError) as exc:
        raise ErrorUso("no se pudo leer el fichero de reemplazos %s: %s" % (ruta, exc))
    entradas = datos.get("reemplazos") if isinstance(datos, dict) else None
    if not isinstance(entradas, list):
        raise ErrorUso("el fichero de reemplazos debe contener una lista 'reemplazos'")
    aprobados = {}
    for entrada in entradas:
        if not isinstance(entrada, dict) or not isinstance(entrada.get("linea"), int) or entrada["linea"] < 1:
            raise ErrorUso("reemplazo sin 'linea' entera positiva: %r" % (entrada,))
        claves = [c for c in ("texto", "patron", "eliminar") if c in entrada]
        if len(claves) != 1:
            raise ErrorUso("el reemplazo de la línea %d debe tener exactamente uno de texto, patron o eliminar" % entrada["linea"])
        if "patron" in entrada:
            try:
                entrada = dict(entrada, _regex=re.compile(entrada["patron"]))
            except re.error as exc:
                raise ErrorUso("patrón inválido en la línea %d: %s" % (entrada["linea"], exc))
        if entrada["linea"] in aprobados:
            raise ErrorUso("la línea %d aparece dos veces en los reemplazos" % entrada["linea"])
        aprobados[entrada["linea"]] = entrada
    return aprobados


def fin_frontmatter(lineas):
    """Índice de la línea que cierra el frontmatter YAML, o -1 si no hay frontmatter."""
    if not lineas or lineas[0][0] != "---":
        return -1
    for indice in range(1, len(lineas)):
        if lineas[indice][0] in ("---", "..."):
            return indice
    return -1


def localizar_bloques(lineas, inicio, fin):
    """Devuelve (bloques, incidencias). Cada bloque es (indice_inicio, indice_fin)."""
    bloques, incidencias = [], []
    abierto = None
    en_cerca = False
    limite_frontmatter = fin_frontmatter(lineas)
    for indice, (contenido, _) in enumerate(lineas):
        recortado = contenido.strip()
        if recortado.startswith("```") or recortado.startswith("~~~"):
            en_cerca = not en_cerca
        es_inicio, es_fin = recortado == inicio, recortado == fin
        if not (es_inicio or es_fin):
            if inicio in contenido or fin in contenido:
                incidencias.append(("aviso", "marcador-no-aislado", indice + 1,
                                    "la línea contiene un marcador junto a otro texto; no cuenta como marcador"))
            continue
        if indice <= limite_frontmatter:
            incidencias.append(("error", "marcador-en-frontmatter", indice + 1,
                                "marcador dentro del frontmatter YAML; rompería el YAML"))
        if en_cerca:
            incidencias.append(("aviso", "marcador-en-codigo", indice + 1,
                                "marcador dentro de un bloque de código: se mostraría literalmente"))
        if es_inicio:
            if abierto is not None:
                incidencias.append(("error", "bloque-anidado", indice + 1,
                                    "inicio de bloque sin cerrar el abierto en la línea %d" % (abierto + 1)))
            abierto = indice
        else:
            if abierto is None:
                incidencias.append(("error", "fin-sin-inicio", indice + 1, "marcador de fin sin inicio"))
            else:
                bloques.append((abierto, indice))
                abierto = None
    if abierto is not None:
        incidencias.append(("error", "bloque-sin-cerrar", abierto + 1, "bloque abierto sin marcador de fin"))
    return bloques, incidencias


def reducir(lineas, bloques, blancos_de_cortesia=True):
    """Quita los bloques. Devuelve (lineas_reducidas, mapa_a_linea_modificada, bytes_en_bloques)."""
    dentro = set()
    for ini, fin in bloques:
        dentro.update(range(ini, fin + 1))
    reducidas, mapa = [], []
    bytes_bloques = sum(len((c + f).encode("utf-8")) for i, (c, f) in enumerate(lineas) if i in dentro)
    saltar = set()
    for ini, fin in bloques:
        siguiente = fin + 1
        anterior = ini - 1
        if not blancos_de_cortesia:
            continue
        anterior_blanca = anterior >= 0 and anterior not in dentro and lineas[anterior][0].strip() == ""
        if siguiente < len(lineas):
            if anterior_blanca and siguiente not in dentro and lineas[siguiente][0].strip() == "":
                saltar.add(siguiente)
        elif anterior_blanca:
            saltar.add(anterior)
    for indice, linea in enumerate(lineas):
        if indice in dentro or indice in saltar:
            continue
        reducidas.append(linea)
        mapa.append(indice + 1)
    return reducidas, mapa, bytes_bloques


def describir(linea):
    contenido, final = linea
    return repr(contenido + final)


def comparar(original, reducidas, mapa, aprobados):
    incidencias, aplicados = [], set()
    comparador = difflib.SequenceMatcher(a=original, b=reducidas, autojunk=False)
    for etiqueta, i1, i2, j1, j2 in comparador.get_opcodes():
        if etiqueta == "equal":
            continue
        lineas_orig = list(range(i1 + 1, i2 + 1))
        nuevas = reducidas[j1:j2]
        cubierto = bool(lineas_orig) and all(n in aprobados for n in lineas_orig)
        if cubierto:
            esperadas = [n for n in lineas_orig if not aprobados[n].get("eliminar")]
            if len(esperadas) != len(nuevas):
                cubierto = False
            else:
                for numero, nueva in zip(esperadas, nuevas):
                    entrada = aprobados[numero]
                    final_ok = nueva[1] == original[numero - 1][1]
                    if "texto" in entrada:
                        texto_ok = nueva[0] == entrada["texto"]
                    else:
                        regex = entrada.get("_regex") or re.compile(entrada["patron"])
                        texto_ok = regex.fullmatch(nueva[0]) is not None
                    if not (final_ok and texto_ok):
                        cubierto = False
                        break
        if cubierto:
            aplicados.update(lineas_orig)
            continue
        if etiqueta == "insert":
            donde = "tras la línea %d del original" % i1 if i1 else "al principio del original"
            mensaje = "%d línea(s) añadidas fuera de bloque %s (líneas %s del modificado): %s" % (
                len(nuevas), donde, ", ".join(str(mapa[j]) for j in range(j1, j2)),
                "; ".join(describir(x) for x in nuevas[:3]))
            incidencias.append(("error", "adicion-fuera-de-bloque", mapa[j1], mensaje))
        elif etiqueta == "delete":
            mensaje = "línea(s) %s del original eliminadas: %s" % (
                ", ".join(map(str, lineas_orig)), "; ".join(describir(original[n - 1]) for n in lineas_orig[:3]))
            incidencias.append(("error", "eliminacion-no-aprobada", lineas_orig[0], mensaje))
        else:
            mensaje = "líneas %s del original cambiadas por líneas %s del modificado: %s → %s" % (
                ", ".join(map(str, lineas_orig)), ", ".join(str(mapa[j]) for j in range(j1, j2)),
                "; ".join(describir(original[n - 1]) for n in lineas_orig[:3]),
                "; ".join(describir(x) for x in nuevas[:3]))
            incidencias.append(("error", "cambio-no-aprobado", lineas_orig[0], mensaje))
    for numero in sorted(set(aprobados) - aplicados):
        if numero > len(original):
            incidencias.append(("error", "reemplazo-fuera-de-rango", numero,
                                "el reemplazo aprobado apunta a la línea %d, pero el original tiene %d" % (numero, len(original))))
        else:
            incidencias.append(("info", "reemplazo-pendiente", numero,
                                "reemplazo aprobado aún no aplicado (línea %d del original)" % numero))
    return incidencias


def verificar(datos_original, datos_modificado, inicio=INICIO_POR_DEFECTO, fin=FIN_POR_DEFECTO,
              aprobados=None, max_bytes=None, blancos_de_cortesia=True):
    original = leer_lineas(datos_original, "el original")
    modificado = leer_lineas(datos_modificado, "el modificado")
    bloques, incidencias = localizar_bloques(modificado, inicio, fin)
    # Con blancos de cortesía se prueba también la variante sin ellos y se conserva la que deja
    # menos errores: ambas solo difieren en líneas en blanco contiguas a un bloque, así que
    # ninguna puede ocultar un cambio en otra parte del texto.
    variantes = [True, False] if blancos_de_cortesia else [False]
    mejor = None
    for cortesia in variantes:
        reducidas, mapa, bytes_bloques = reducir(modificado, bloques, cortesia)
        diferencias = comparar(original, reducidas, mapa, aprobados or {})
        errores = sum(1 for d in diferencias if d[0] == "error")
        if mejor is None or errores < mejor[0]:
            mejor = (errores, diferencias)
    incidencias += mejor[1]
    if max_bytes is not None and bytes_bloques > max_bytes:
        incidencias.append(("error", "presupuesto-superado", 0,
                            "los bloques suman %d bytes y el presupuesto es %d" % (bytes_bloques, max_bytes)))
    return {
        "bloques": [{"inicio": a + 1, "fin": b + 1} for a, b in bloques],
        "bytes_en_bloques": bytes_bloques,
        "lineas_original": len(original),
        "lineas_modificado": len(modificado),
        "incidencias": [
            {"severidad": s, "codigo": c, "linea": l, "mensaje": m} for s, c, l, m in incidencias
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Comprueba que un fichero solo cambia por bloques añadidos y delimitados.")
    parser.add_argument("original", nargs="?", help="fichero original (omítelo si usas --git)")
    parser.add_argument("modificado", help="fichero modificado")
    parser.add_argument("--git", metavar="REVISION", help="tomar el original de git show REVISION:<ruta del modificado>")
    parser.add_argument("--inicio", default=INICIO_POR_DEFECTO, help="marcador de inicio (por defecto: %(default)s)")
    parser.add_argument("--fin", default=FIN_POR_DEFECTO, help="marcador de fin (por defecto: %(default)s)")
    parser.add_argument("--reemplazos", metavar="JSON", help="fichero JSON con los reemplazos aprobados")
    parser.add_argument("--max-bytes", type=int, help="presupuesto máximo de bytes en bloques")
    parser.add_argument("--sin-blancos-de-cortesia", action="store_true",
                        help="no descontar la línea en blanco que rodea a cada bloque")
    parser.add_argument("--json", action="store_true", help="salida JSON")
    args = parser.parse_args(argv)
    try:
        if args.git and args.original:
            raise ErrorUso("indica el original o --git, no ambos")
        if not args.git and not args.original:
            raise ErrorUso("falta el fichero original (o --git REVISION)")
        try:
            with open(args.modificado, "rb") as fichero:
                datos_modificado = fichero.read()
            if args.git:
                datos_original = leer_original_git(args.git, args.modificado)
            else:
                with open(args.original, "rb") as fichero:
                    datos_original = fichero.read()
        except OSError as exc:
            raise ErrorUso(str(exc))
        resultado = verificar(datos_original, datos_modificado, args.inicio, args.fin,
                              cargar_reemplazos(args.reemplazos), args.max_bytes,
                              not args.sin_blancos_de_cortesia)
    except ErrorUso as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    errores = sum(1 for i in resultado["incidencias"] if i["severidad"] == "error")
    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        print("Bloques: %d · bytes añadidos en bloques: %d · líneas original/modificado: %d/%d" % (
            len(resultado["bloques"]), resultado["bytes_en_bloques"],
            resultado["lineas_original"], resultado["lineas_modificado"]))
        for inc in resultado["incidencias"]:
            print("[%s] %s (línea %s): %s" % (inc["severidad"].upper(), inc["codigo"], inc["linea"], inc["mensaje"]))
        print("Resultado: %s" % ("sin diferencias fuera de los bloques y reemplazos aprobados" if errores == 0
                                 else "%d error(es)" % errores))
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())

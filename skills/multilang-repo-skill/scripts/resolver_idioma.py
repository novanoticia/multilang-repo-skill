#!/usr/bin/env python3
"""Resuelve el idioma de una petición de forma total (nunca falla por la entrada) y devuelve JSON.

Implementación de referencia de la regla de selección de idioma para proyectos híbridos
(instrucciones que un modelo ejecuta + un script). Sirve para dos cosas:
  - probar la tabla de casos de selección contra los catálogos reales de un proyecto;
  - copiarla y adaptarla al proyecto, SOLO si el diseño aprobado lo prevé.

El mensaje del usuario entra en bruto por la entrada estándar, nunca como argumento ni dentro de un
heredoc: un apóstrofo («j'aimerais»), unas comillas o un $(...) romperían la orden, y un heredoc de
delimitador fijo se cierra antes de tiempo si el mensaje contiene una línea igual al delimitador, y lo
que sigue se ejecuta. Método seguro: el agente escribe el mensaje en un fichero temporal fuera del
repositorio con su herramienta de escritura de ficheros (sin pasar por el shell) y lo redirige:

    python3 resolver_idioma.py --disponibles es,en,fr --defecto es < /ruta/temporal/mensaje.txt

Las líneas que empiezan por «>» (texto citado) no aportan la marca.

Orden de fuentes: marca explícita (clave=valor, solo en la primera línea no vacía, para que una marca
dentro de un texto pegado no cuente) > --config > variables de entorno (solo si se pasa --entorno) >
--defecto. Si una fuente no se puede servir, se avisa y se continúa con la siguiente.

Salida (una línea JSON): idioma, solicitado, origen, cadena, avisos[{codigo, detalle, visible}],
disponibles. 'visible' indica que el agente debe mostrar el aviso a la persona, con el texto de su
catálogo localizado según 'codigo'; 'detalle' es un diagnóstico en español, no un texto para mostrar.

Códigos de salida: 0 siempre que la invocación sea correcta (la entrada nunca hace fallar);
2 si la configuración del propio script es inválida (p. ej. --defecto no está entre los disponibles).
Solo biblioteca estándar (Python 3.8+). No escribe ficheros.
"""

import argparse
import json
import os
import re
import sys

CLAVES_POR_DEFECTO = ("idioma", "lang")
# Códigos retirados de ISO 639 que aún aparecen en sistemas antiguos.
LEGADO = {"iw": "he", "in": "id", "ji": "yi", "jw": "jv", "mo": "ro"}
# Modificadores POSIX que codifican escritura o variante; los demás (@euro) se descartan.
MODIFICADORES_POSIX = {"latin": "Latn", "cyrillic": "Cyrl", "devanagari": "Deva", "valencia": "valencia"}
COMILLAS = "\"'«»“”‘’`"
PUNTUACION_FINAL = ".,;:!?)]}" + COMILLAS


class ErrorUso(Exception):
    pass


def normalizar(valor):
    """Devuelve (etiqueta_canonica, problema). (None, None) significa «sin preferencia»."""
    if valor is None:
        return None, None
    limpio = valor.strip().strip(COMILLAS).rstrip(PUNTUACION_FINAL).strip(COMILLAS)
    if limpio == "":
        return None, "vacio"
    limpio, _, modificador = limpio.partition("@")             # sr_RS@latin, ca_ES@valencia
    limpio = limpio.split(".", 1)[0]                             # fr_FR.UTF-8
    if limpio.upper() in ("C", "POSIX"):
        return None, None                                        # locale técnico: sin preferencia
    partes = limpio.replace("_", "-").split("-")
    if not re.fullmatch(r"[A-Za-z]{2,3}", partes[0]):
        return None, "mal_formado"
    lengua = LEGADO.get(partes[0].lower(), partes[0].lower())
    salida = [lengua]
    for parte in partes[1:]:
        if len(parte) == 1:                                      # extensiones -u-, -x-: no afectan al catálogo
            break
        if re.fullmatch(r"[A-Za-z]{4}", parte):
            salida.append(parte.title())                         # escritura: Hant, Latn, Cyrl
        elif re.fullmatch(r"[A-Za-z]{2}", parte):
            salida.append(parte.upper())                         # región ISO 3166
        elif re.fullmatch(r"\d{3}", parte):
            salida.append(parte)                                 # región UN M.49 (419)
        elif re.fullmatch(r"[A-Za-z0-9]{5,8}|\d[A-Za-z0-9]{3}", parte):
            salida.append(parte.lower())                         # variante
        else:
            return None, "mal_formado"
    extra = MODIFICADORES_POSIX.get(modificador.split(".", 1)[0].lower())
    if extra and len(extra) == 4:
        if not any(len(p) == 4 and p.isalpha() for p in salida[1:]):
            salida.insert(1, extra)                              # escritura: sr-Latn-RS
    elif extra:
        salida.append(extra)                                     # variante: ca-ES-valencia
    return "-".join(salida), None


def truncar(etiqueta):
    """Respaldo por truncamiento (RFC 4647, «lookup»): zh-Hant-TW → zh-Hant → zh."""
    partes = etiqueta.split("-")
    if len(partes) <= 1:
        return None
    partes.pop()
    if len(partes) > 1 and len(partes[-1]) == 1:
        partes.pop()
    return "-".join(partes)


def cadena_de(etiqueta, respaldos):
    cadena, actual, vistos = [], etiqueta, set()
    while actual and actual.lower() not in vistos:
        vistos.add(actual.lower())
        cadena.append(actual)
        actual = respaldos.get(actual.lower()) or truncar(actual)
    return cadena


def elegir(etiqueta, disponibles, respaldos):
    """Devuelve (idioma_disponible | None, cadena_probada)."""
    indice = {d.lower(): d for d in disponibles}
    cadena = cadena_de(etiqueta, respaldos)
    for posicion, candidata in enumerate(cadena):
        if candidata.lower() in indice:
            return indice[candidata.lower()], cadena[:posicion + 1]
    return None, cadena


def buscar_marca(mensaje, claves, todo_el_mensaje):
    # Las líneas citadas con «>» son texto ajeno (un correo, una respuesta): nunca aportan la marca.
    propias = [linea for linea in mensaje.splitlines() if not linea.lstrip().startswith(">")]
    if todo_el_mensaje:
        zona = "\n".join(propias)
    else:
        zona = next((linea for linea in propias if linea.strip()), "")
    patron = re.compile(r"(?<![\w=-])(?:%s)=(\S*)" % "|".join(re.escape(c) for c in claves), re.IGNORECASE)
    return [m.group(1) for m in patron.finditer(zona)]


def resolver(entrada, disponibles, defecto, claves=CLAVES_POR_DEFECTO, config=None, entorno=(),
             respaldos=None, todo_el_mensaje=False):
    """Función total: cualquier entrada produce un resultado; nunca lanza por la entrada."""
    respaldos = {k.lower(): v for k, v in (respaldos or {}).items()}
    avisos = []

    def avisar(codigo, detalle, visible):
        avisos.append({"codigo": codigo, "detalle": detalle, "visible": visible})

    if isinstance(entrada, bytes):
        try:
            mensaje = entrada.decode("utf-8")
        except UnicodeDecodeError:
            mensaje = entrada.decode("utf-8", "replace")
            avisar("entrada_invalida", "el mensaje no es UTF-8 válido; se ha leído con sustituciones", True)
    else:
        mensaje = entrada or ""
    fuentes = []
    marcas = buscar_marca(mensaje, claves, todo_el_mensaje)
    if len(marcas) > 1:
        avisar("marca_repetida", "hay %d marcas de idioma; se usa la primera" % len(marcas), True)
    if marcas:
        fuentes.append(("marca", marcas[0], True))
    if config is not None:
        fuentes.append(("config", config, True))
    for nombre, valor in entorno:
        for parte in (valor or "").split(":"):                   # LANGUAGE admite listas fr:en
            fuentes.append(("entorno:" + nombre, parte, False))
    for origen, valor, visible in fuentes:
        etiqueta, problema = normalizar(valor)
        tipo = origen.split(":")[0]
        if problema == "vacio":
            if visible:
                avisar(tipo + "_vacia", "se indicó %s sin valor; se continúa" % tipo, True)
            continue
        if problema:
            avisar(tipo + "_mal_formada", "%r no es una etiqueta de idioma válida (fuente: %s)" % (valor, origen), visible)
            continue
        if etiqueta is None:
            continue
        elegido, cadena = elegir(etiqueta, disponibles, respaldos)
        if elegido is None:
            avisar("no_disponible", "%s no está disponible (fuente: %s; disponibles: %s)"
                   % (etiqueta, origen, ", ".join(disponibles)), visible)
            continue
        if elegido.lower() != etiqueta.lower():
            avisar("respaldo", "%s no existe; se usa %s" % (etiqueta, elegido), False)
        return {"idioma": elegido, "solicitado": etiqueta, "origen": origen.split(":")[0],
                "cadena": cadena, "avisos": avisos, "disponibles": list(disponibles)}
    return {"idioma": defecto, "solicitado": None, "origen": "defecto", "cadena": [defecto],
            "avisos": avisos, "disponibles": list(disponibles)}


def descubrir_catalogos(directorio):
    if not os.path.isdir(directorio):
        raise ErrorUso("no existe la carpeta de catálogos %s" % directorio)
    encontrados = []
    for entrada in sorted(os.listdir(directorio)):
        nombre = entrada[:-5] if entrada.endswith(".json") else entrada
        ruta = os.path.join(directorio, entrada)
        if entrada.startswith(".") or not (entrada.endswith(".json") or os.path.isdir(ruta)):
            continue
        etiqueta, problema = normalizar(nombre)
        if etiqueta and not problema:
            encontrados.append(etiqueta)
    return encontrados


def main(argv=None):
    parser = argparse.ArgumentParser(description="Resuelve el idioma de un mensaje leído por la entrada estándar.")
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--disponibles", help="idiomas disponibles separados por comas (p. ej. es,en,pt-BR)")
    grupo.add_argument("--catalogos", help="carpeta con <idioma>.json o <idioma>/ para descubrirlos")
    parser.add_argument("--defecto", required=True, help="idioma por defecto; debe estar disponible")
    parser.add_argument("--claves", default=",".join(CLAVES_POR_DEFECTO), help="claves de la marca (por defecto: %(default)s)")
    parser.add_argument("--config", help="idioma configurado por la persona o el proyecto")
    parser.add_argument("--entorno", default="", help="variables de entorno a consultar, en orden (p. ej. LC_ALL,LANG); vacío = ninguna")
    parser.add_argument("--respaldo", action="append", default=[], metavar="ORIGEN=DESTINO",
                        help="eslabón explícito de respaldo (p. ej. zh-TW=zh-Hant, es-AR=es-419); repetible")
    parser.add_argument("--todo-el-mensaje", action="store_true", help="buscar la marca en todo el mensaje, no solo en la primera línea")
    args = parser.parse_args(argv)
    try:
        if args.catalogos:
            disponibles = descubrir_catalogos(args.catalogos)
        else:
            disponibles = []
            for valor in args.disponibles.split(","):
                if valor.strip():
                    etiqueta, problema = normalizar(valor)
                    if problema or etiqueta is None:
                        raise ErrorUso("idioma disponible inválido: %r" % valor)
                    disponibles.append(etiqueta)
        defecto, problema = normalizar(args.defecto)
        if problema or defecto is None or defecto.lower() not in {d.lower() for d in disponibles}:
            raise ErrorUso("--defecto %r debe ser uno de los disponibles: %s" % (args.defecto, ", ".join(disponibles) or "ninguno"))
        respaldos = {}
        for par in args.respaldo:
            origen, _, destino = par.partition("=")
            o, p1 = normalizar(origen)
            d, p2 = normalizar(destino)
            if not o or not d or p1 or p2:
                raise ErrorUso("--respaldo inválido: %r (usa ORIGEN=DESTINO)" % par)
            respaldos[o] = d
        claves = [c.strip() for c in args.claves.split(",") if c.strip()]
        if not claves:
            raise ErrorUso("--claves no puede estar vacío")
    except ErrorUso as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    entrada = b"" if sys.stdin is None or sys.stdin.isatty() else sys.stdin.buffer.read()
    entorno = [(n.strip(), os.environ.get(n.strip())) for n in args.entorno.split(",") if n.strip()]
    resultado = resolver(entrada, disponibles, defecto, claves, args.config, entorno, respaldos, args.todo_el_mensaje)
    print(json.dumps(resultado, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

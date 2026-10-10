"""Pruebas de verificar_adiciones.py. Ejecutar desde la raíz de la skill:
    python3 -B -m unittest discover -s scripts/tests -v
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPTS)
import verificar_adiciones as va  # noqa: E402

ORIGINAL = (
    "---\nname: demo\ndescription: Demo.\n---\n\n# Demo\n\nPaso 1: lee el caso.\n\nPaso 2: responde.\n"
).encode("utf-8")
INI, FIN = va.INICIO_POR_DEFECTO, va.FIN_POR_DEFECTO


def con_bloque(texto, despues_de, bloque="Responde en el idioma elegido.\n"):
    original = texto.decode("utf-8")
    insercion = "\n%s\n%s%s\n" % (INI, bloque, FIN)
    i = original.index(despues_de) + len(despues_de)
    return (original[:i] + insercion + original[i:]).encode("utf-8")


def errores(resultado):
    return [i for i in resultado["incidencias"] if i["severidad"] == "error"]


class PruebasVerificarAdiciones(unittest.TestCase):
    def test_sin_cambios(self):
        self.assertEqual(errores(va.verificar(ORIGINAL, ORIGINAL)), [])

    def test_bloque_entre_parrafos_con_blancos_de_cortesia(self):
        modificado = con_bloque(ORIGINAL, "Paso 1: lee el caso.\n")
        resultado = va.verificar(ORIGINAL, modificado)
        self.assertEqual(errores(resultado), [])
        self.assertEqual(len(resultado["bloques"]), 1)
        self.assertGreater(resultado["bytes_en_bloques"], 0)

    def test_bloque_al_final_del_fichero(self):
        modificado = ORIGINAL + ("\n%s\nTexto.\n%s\n" % (INI, FIN)).encode("utf-8")
        self.assertEqual(errores(va.verificar(ORIGINAL, modificado)), [])

    def test_dos_bloques_consecutivos(self):
        modificado = con_bloque(con_bloque(ORIGINAL, "Paso 2: responde.\n", "B\n"), "Paso 1: lee el caso.\n", "A\n")
        self.assertEqual(errores(va.verificar(ORIGINAL, modificado)), [])

    def test_cambio_de_una_palabra_fuera_del_bloque(self):
        modificado = con_bloque(ORIGINAL, "Paso 1: lee el caso.\n").replace(b"responde", b"contesta")
        codigos = [i["codigo"] for i in errores(va.verificar(ORIGINAL, modificado))]
        self.assertEqual(codigos, ["cambio-no-aprobado"])

    def test_numstat_no_basta_mismo_numero_de_lineas(self):
        # Mismo número de líneas añadidas y borradas que un reemplazo aprobado, pero en otra línea.
        aprobados = {8: {"linea": 8, "texto": "Paso 1: lee el caso completo."}}
        modificado = ORIGINAL.replace(b"Paso 2: responde.", b"Paso 2: responde ya.")
        codigos = [i["codigo"] for i in errores(va.verificar(ORIGINAL, modificado, aprobados=aprobados))]
        self.assertEqual(codigos, ["cambio-no-aprobado"])

    def test_reemplazo_aprobado_por_texto_y_por_patron(self):
        aprobados = {
            3: {"linea": 3, "patron": r"^description: .+$"},
            8: {"linea": 8, "texto": "Paso 1: lee el caso completo."},
        }
        modificado = ORIGINAL.replace(b"Paso 1: lee el caso.", b"Paso 1: lee el caso completo.")
        modificado = modificado.replace(b"description: Demo.", b"description: Demo multiidioma.")
        self.assertEqual(errores(va.verificar(ORIGINAL, modificado, aprobados=aprobados)), [])

    def test_reemplazo_aprobado_pendiente_es_informativo(self):
        aprobados = {8: {"linea": 8, "texto": "otra cosa"}}
        resultado = va.verificar(ORIGINAL, ORIGINAL, aprobados=aprobados)
        self.assertEqual(errores(resultado), [])
        self.assertIn("reemplazo-pendiente", [i["codigo"] for i in resultado["incidencias"]])

    def test_eliminacion_aprobada_y_no_aprobada(self):
        modificado = ORIGINAL.replace(b"Paso 2: responde.\n", b"")
        self.assertEqual([i["codigo"] for i in errores(va.verificar(ORIGINAL, modificado))],
                         ["eliminacion-no-aprobada"])
        aprobados = {10: {"linea": 10, "eliminar": True}}
        self.assertEqual(errores(va.verificar(ORIGINAL, modificado, aprobados=aprobados)), [])

    def test_adicion_fuera_de_bloque(self):
        modificado = ORIGINAL + b"Linea suelta.\n"
        self.assertEqual([i["codigo"] for i in errores(va.verificar(ORIGINAL, modificado))],
                         ["adicion-fuera-de-bloque"])

    def test_bloque_sin_cerrar_anidado_y_fin_sin_inicio(self):
        sin_cerrar = ORIGINAL + ("\n%s\nTexto.\n" % INI).encode("utf-8")
        self.assertIn("bloque-sin-cerrar", [i["codigo"] for i in errores(va.verificar(ORIGINAL, sin_cerrar))])
        anidado = ORIGINAL + ("\n%s\n%s\nx\n%s\n%s\n" % (INI, INI, FIN, FIN)).encode("utf-8")
        codigos = [i["codigo"] for i in errores(va.verificar(ORIGINAL, anidado))]
        self.assertIn("bloque-anidado", codigos)
        self.assertIn("fin-sin-inicio", codigos)

    def test_marcador_en_frontmatter(self):
        modificado = ORIGINAL.replace(b"name: demo\n", ("name: demo\n%s\nx: 1\n%s\n" % (INI, FIN)).encode("utf-8"))
        self.assertIn("marcador-en-frontmatter", [i["codigo"] for i in errores(va.verificar(ORIGINAL, modificado))])

    def test_final_de_linea_crlf_cuenta_como_cambio(self):
        modificado = ORIGINAL.replace(b"Paso 2: responde.\n", b"Paso 2: responde.\r\n")
        self.assertEqual([i["codigo"] for i in errores(va.verificar(ORIGINAL, modificado))], ["cambio-no-aprobado"])

    def test_presupuesto(self):
        modificado = con_bloque(ORIGINAL, "Paso 1: lee el caso.\n", "x" * 200 + "\n")
        self.assertIn("presupuesto-superado",
                      [i["codigo"] for i in errores(va.verificar(ORIGINAL, modificado, max_bytes=100))])
        self.assertEqual(errores(va.verificar(ORIGINAL, modificado, max_bytes=10000)), [])

    def test_marcador_dentro_de_codigo_es_aviso(self):
        modificado = ORIGINAL + ("\n```\n%s\nx\n%s\n```\n" % (INI, FIN)).encode("utf-8")
        resultado = va.verificar(ORIGINAL, modificado)
        self.assertIn("marcador-en-codigo", [i["codigo"] for i in resultado["incidencias"]])

    def test_marcador_no_aislado_no_abre_bloque(self):
        modificado = ORIGINAL + ("Texto %s\nañadido\n%s\n" % (INI, FIN)).encode("utf-8")
        resultado = va.verificar(ORIGINAL, modificado)
        codigos = [i["codigo"] for i in resultado["incidencias"]]
        self.assertIn("marcador-no-aislado", codigos)
        self.assertIn("adicion-fuera-de-bloque", [i["codigo"] for i in errores(resultado)])

    def test_reemplazo_aprobado_con_otro_final_de_linea_no_vale(self):
        aprobados = {8: {"linea": 8, "texto": "Paso 1: lee todo."}}
        modificado = ORIGINAL.replace(b"Paso 1: lee el caso.\n", b"Paso 1: lee todo.\r\n")
        self.assertEqual([i["codigo"] for i in errores(va.verificar(ORIGINAL, modificado, aprobados=aprobados))],
                         ["cambio-no-aprobado"])

    def test_linea_anadida_justo_tras_el_bloque_no_se_oculta(self):
        # El blanco de cortesía solo se descuenta si la línea siguiente también está en blanco.
        modificado = ORIGINAL.replace(
            b"Paso 1: lee el caso.\n\n",
            ("Paso 1: lee el caso.\n\n%s\nBloque.\n%s\nLINEA EXTRA\n" % (INI, FIN)).encode("utf-8"))
        self.assertEqual([i["codigo"] for i in errores(va.verificar(ORIGINAL, modificado))],
                         ["adicion-fuera-de-bloque"])

    def test_presupuesto_en_el_limite_exacto(self):
        modificado = con_bloque(ORIGINAL, "Paso 1: lee el caso.\n", "x" * 50 + "\n")
        exacto = va.verificar(ORIGINAL, modificado)["bytes_en_bloques"]
        self.assertEqual(errores(va.verificar(ORIGINAL, modificado, max_bytes=exacto)), [])
        self.assertEqual([i["codigo"] for i in errores(va.verificar(ORIGINAL, modificado, max_bytes=exacto - 1))],
                         ["presupuesto-superado"])

    def test_fichero_largo_con_reemplazo_aprobado(self):
        # Más de 200 líneas con muchas repetidas: la alineación no debe tratar las líneas frecuentes
        # como «basura» (heurística autojunk de difflib), o el reemplazo aprobado deja de reconocerse.
        lineas = []
        for i in range(400):
            lineas.append("" if i % 2 else "- elemento")
        lineas[201] = "Línea única que se aprueba cambiar."
        original = ("\n".join(lineas) + "\n").encode("utf-8")
        modificado = original.replace("Línea única que se aprueba cambiar.".encode("utf-8"),
                                      "Línea única ya cambiada.".encode("utf-8"))
        aprobados = {202: {"linea": 202, "texto": "Línea única ya cambiada."}}
        self.assertEqual(errores(va.verificar(original, modificado, aprobados=aprobados)), [])

    def test_solo_salto_de_linea_separa_lineas(self):
        original = "uno\fsigue\ndos\u2028sigue\ntres\n".encode("utf-8")
        modificado = original.replace("tres".encode("utf-8"), "TRES".encode("utf-8"))
        aprobados = {3: {"linea": 3, "texto": "TRES"}}
        self.assertEqual(errores(va.verificar(original, modificado, aprobados=aprobados)), [])

    def test_bloque_con_blancos_en_medio_de_una_lista_se_senala(self):
        # Insertar blancos entre dos elementos de lista cambia la estructura del original: D27 pide
        # insertar donde ya haya una línea en blanco.
        original = b"- uno\n- dos\n"
        modificado = ("- uno\n\n%s\nx\n%s\n\n- dos\n" % (INI, FIN)).encode("utf-8")
        self.assertIn("adicion-fuera-de-bloque", [i["codigo"] for i in errores(va.verificar(original, modificado))])

    def test_utf8_invalido_es_error_de_uso(self):
        with self.assertRaises(va.ErrorUso):
            va.verificar(ORIGINAL, b"\xff\xfe")


class PruebasLineaDeOrdenes(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.script = os.path.join(SCRIPTS, "verificar_adiciones.py")

    def tearDown(self):
        shutil.rmtree(self.dir)

    def escribir(self, nombre, datos):
        ruta = os.path.join(self.dir, nombre)
        with open(ruta, "wb") as f:
            f.write(datos)
        return ruta

    def ejecutar(self, *args, cwd=None):
        return subprocess.run([sys.executable, "-B", self.script] + list(args), cwd=cwd,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_codigos_de_salida(self):
        orig = self.escribir("o.md", ORIGINAL)
        bien = self.escribir("b.md", con_bloque(ORIGINAL, "Paso 1: lee el caso.\n"))
        mal = self.escribir("m.md", ORIGINAL.replace(b"Demo.", b"Otra."))
        self.assertEqual(self.ejecutar(orig, bien).returncode, 0)
        self.assertEqual(self.ejecutar(orig, mal).returncode, 1)
        self.assertEqual(self.ejecutar(orig, os.path.join(self.dir, "no-existe.md")).returncode, 2)
        salida = self.ejecutar(orig, mal, "--json")
        self.assertEqual(json.loads(salida.stdout.decode("utf-8"))["incidencias"][0]["codigo"], "cambio-no-aprobado")

    def test_reemplazos_desde_fichero_y_fichero_invalido(self):
        orig = self.escribir("o.md", ORIGINAL)
        mod = self.escribir("m.md", ORIGINAL.replace(b"Paso 1: lee el caso.", b"Paso 1: lee todo."))
        reemp = self.escribir("r.json", json.dumps({"reemplazos": [{"linea": 8, "texto": "Paso 1: lee todo."}]}).encode())
        self.assertEqual(self.ejecutar(orig, mod, "--reemplazos", reemp).returncode, 0)
        roto = self.escribir("roto.json", b'{"reemplazos": [{"linea": 8}]}')
        self.assertEqual(self.ejecutar(orig, mod, "--reemplazos", roto).returncode, 2)

    @unittest.skipIf(shutil.which("git") is None, "git no está disponible")
    def test_original_desde_git(self):
        repo = os.path.join(self.dir, "repo")
        os.mkdir(repo)
        ruta = os.path.join(repo, "SKILL.md")
        with open(ruta, "wb") as f:
            f.write(ORIGINAL)
        entorno = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
                       GIT_COMMITTER_EMAIL="t@t", GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
        for orden in (["git", "init", "-q"], ["git", "add", "SKILL.md"], ["git", "commit", "-q", "-m", "base"]):
            subprocess.run(orden, cwd=repo, check=True, env=entorno, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with open(ruta, "wb") as f:
            f.write(con_bloque(ORIGINAL, "Paso 2: responde.\n"))
        self.assertEqual(self.ejecutar("--git", "HEAD", ruta).returncode, 0)
        with open(ruta, "ab") as f:
            f.write(b"suelta\n")
        self.assertEqual(self.ejecutar("--git", "HEAD", ruta).returncode, 1)
        self.assertEqual(self.ejecutar("--git", "no-existe", ruta).returncode, 2)


if __name__ == "__main__":
    unittest.main()

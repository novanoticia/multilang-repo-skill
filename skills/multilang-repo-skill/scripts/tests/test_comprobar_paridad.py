"""Pruebas de comprobar_paridad.py. Ejecutar desde la raíz de la skill:
    python3 -B -m unittest discover -s scripts/tests -v
"""
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPTS)
import comprobar_paridad as cp  # noqa: E402

SCRIPT = os.path.join(SCRIPTS, "comprobar_paridad.py")

ES = (
    "# Título\n"
    "\n"
    "Regla R1 y D4 en [instrucciones] con [enlace](references/a.md#sección) y [web](https://x.org/a).\n"
    "\n"
    "## Sección\n"
    "\n"
    "| a | b |\n"
    "|---|---|\n"
    "| 1 | 2 |\n"
    "\n"
    "```bash\n"
    "# comentario en español\n"
    "python3 x.py --opcion\n"
    "```\n"
    "\n"
    "```\n"
    "Fase 0  Entorno\n"
    "```\n"
    "\n"
    "Fin R1.\n"
).encode("utf-8")


def cabecera(datos, estado="borrador-ia", extra=""):
    return "<!-- i18n fuente-sha256=%s estado=%s%s -->\n\n" % (cp.hash_fuente(datos), estado, extra)


EN_CUERPO = (
    "# Title\n"
    "\n"
    "Rule R1 and D4 in [instrucciones] with [link](references/a.md#section) and [web](https://x.org/a).\n"
    "\n"
    "## Section\n"
    "\n"
    "| a | b |\n"
    "|---|---|\n"
    "| 1 | 2 |\n"
    "\n"
    "```bash\n"
    "# comment in English\n"
    "python3 x.py --opcion\n"
    "```\n"
    "\n"
    "```\n"
    "Phase 0  Environment\n"
    "```\n"
    "\n"
    "End R1.\n"
)


def en(cuerpo=EN_CUERPO, es=ES, **kw):
    return (cabecera(es, **kw) + cuerpo).encode("utf-8")


def codigos(incidencias, severidad=None):
    return sorted(i["codigo"] for i in incidencias if severidad is None or i["severidad"] == severidad)


def errores(incidencias):
    return codigos(incidencias, "error")


class PruebasComparar(unittest.TestCase):
    def test_paridad_correcta(self):
        self.assertEqual(errores(cp.comparar(ES, en())), [])

    def test_falta_un_identificador(self):
        self.assertEqual(errores(cp.comparar(ES, en(EN_CUERPO.replace(" and D4", "")))), ["ids_difieren"])

    def test_identificador_cambiado(self):
        self.assertEqual(errores(cp.comparar(ES, en(EN_CUERPO.replace("End R1", "End R2")))), ["ids_difieren"])

    def test_identificador_repetido_de_menos(self):
        # El recuento importa: una mención menos es una regla citada menos veces.
        self.assertEqual(errores(cp.comparar(ES, en(EN_CUERPO.replace("End R1.", "End.")))), ["ids_difieren"])

    def test_ids_en_bloques_de_codigo_se_ignoran(self):
        es = ES + b"\n```bash\n# R9\n```\n"
        trad = en(EN_CUERPO + "\n```bash\n# R7\n```\n", es=es)
        self.assertEqual(errores(cp.comparar(es, trad)), [])

    def test_marca_de_modulo_traducida(self):
        incs = cp.comparar(ES, en(EN_CUERPO.replace("[instrucciones]", "[instructions]")))
        self.assertEqual(errores(incs), ["marcas_difieren"])

    def test_enlace_con_texto_igual_a_marca_no_cuenta_como_marca(self):
        es = ES + b"\nVer [seguridad](references/seguridad.md).\n"
        trad = en(EN_CUERPO + "\nSee [security](references/seguridad.md).\n", es=es)
        self.assertEqual(errores(cp.comparar(es, trad)), [])

    def test_encabezado_extra(self):
        incs = cp.comparar(ES, en(EN_CUERPO + "\n## Extra\n"))
        self.assertEqual(errores(incs), ["estructura_difiere"])

    def test_nivel_de_encabezado_cambiado(self):
        incs = cp.comparar(ES, en(EN_CUERPO.replace("## Section", "### Section")))
        self.assertEqual(errores(incs), ["estructura_difiere"])

    def test_encabezado_dentro_de_bloque_no_cuenta(self):
        es = ES + b"\n```bash\n# no soy un encabezado\n```\n"
        trad = en(EN_CUERPO + "\n```bash\n# not a heading\n## tampoco\n```\n", es=es)
        self.assertEqual(errores(cp.comparar(es, trad)), [])

    def test_tabla_con_una_fila_menos(self):
        incs = cp.comparar(ES, en(EN_CUERPO.replace("| 1 | 2 |\n", "")))
        self.assertEqual(errores(incs), ["tablas_difieren"])

    def test_bloque_de_codigo_con_otro_comando(self):
        incs = cp.comparar(ES, en(EN_CUERPO.replace("--opcion", "--option")))
        self.assertEqual(errores(incs), ["bloques_difieren"])

    def test_comentarios_del_bloque_pueden_traducirse(self):
        self.assertEqual(errores(cp.comparar(ES, en())), [])

    def test_comentario_al_final_de_linea_en_bash_puede_traducirse(self):
        es = b"# T\n\n```bash\nclaude plugin validate .   # manifiesto y skill\n```\n"
        trad = en("# T\n\n```bash\nclaude plugin validate .   # manifest and skill\n```\n", es=es)
        self.assertEqual(errores(cp.comparar(es, trad)), [])

    def test_el_comando_antes_del_comentario_se_compara(self):
        es = b"# T\n\n```bash\nclaude plugin validate .   # manifiesto\n```\n"
        trad = en("# T\n\n```bash\nclaude plugin validate --strict .   # manifest\n```\n", es=es)
        self.assertEqual(errores(cp.comparar(es, trad)), ["bloques_difieren"])

    def test_almohadilla_entre_comillas_no_es_comentario(self):
        es = b"# T\n\n```bash\necho \"a # b\"\n```\n"
        trad = en("# T\n\n```bash\necho \"a # c\"\n```\n", es=es)
        self.assertEqual(errores(cp.comparar(es, trad)), ["bloques_difieren"])

    def test_almohadilla_pegada_no_es_comentario(self):
        es = b"# T\n\n```bash\ngit log origin/x#1\n```\n"
        trad = en("# T\n\n```bash\ngit log origin/x#2\n```\n", es=es)
        self.assertEqual(errores(cp.comparar(es, trad)), ["bloques_difieren"])

    def test_comentario_al_final_solo_se_ignora_en_shell(self):
        es = b"# T\n\n```json\n{\"a\": 1} # uno\n```\n"
        trad = en("# T\n\n```json\n{\"a\": 1} # one\n```\n", es=es)
        self.assertEqual(errores(cp.comparar(es, trad)), ["bloques_difieren"])

    def test_bloque_de_codigo_eliminado(self):
        incs = cp.comparar(ES, en(EN_CUERPO.replace("```\nPhase 0  Environment\n```\n\n", "")))
        self.assertEqual(errores(incs), ["bloques_difieren"])

    def test_bloque_sin_lenguaje_solo_cuenta(self):
        self.assertEqual(errores(cp.comparar(ES, en())), [])  # su texto se tradujo y no es error

    def test_enlace_con_otro_destino(self):
        incs = cp.comparar(ES, en(EN_CUERPO.replace("references/a.md", "references/b.md")))
        self.assertEqual(errores(incs), ["enlaces_difieren"])

    def test_enlace_externo_distinto(self):
        incs = cp.comparar(ES, en(EN_CUERPO.replace("x.org/a", "y.org/a")))
        self.assertEqual(errores(incs), ["enlaces_difieren"])

    def test_fragmento_traducido_es_equivalente(self):
        self.assertEqual(errores(cp.comparar(ES, en())), [])  # #sección vs #section

    def test_enlace_relativo_con_otra_profundidad_es_equivalente(self):
        es = b"Ver [script](../scripts/x.py).\n"
        trad = en("See [script](../../../scripts/x.py).\n", es=es)
        incs = cp.comparar(es, trad, dir_es="/r/references", dir_trad="/r/i18n/en/references")
        self.assertEqual(errores(incs), [])

    def test_enlace_relativo_que_apunta_a_otro_fichero(self):
        es = b"Ver [script](../scripts/x.py).\n"
        trad = en("See [script](../../../scripts/y.py).\n", es=es)
        incs = cp.comparar(es, trad, dir_es="/r/references", dir_trad="/r/i18n/en/references")
        self.assertEqual(errores(incs), ["enlaces_difieren"])

    def test_enlace_solo_ancla_cuenta(self):
        es = b"Ver [arriba](#seccion-uno).\n"
        self.assertEqual(errores(cp.comparar(es, en("See [up](#section-one).\n", es=es))), [])
        self.assertEqual(errores(cp.comparar(es, en("See up.\n", es=es))), ["enlaces_difieren"])


class PruebasExencion(unittest.TestCase):
    ES_BASE = "# T\n\nVer R1.\n\nTambién en [inglés](README.en.md).{marca}\n"
    EN_BASE = "# T\n\nSee R1.\n\nAlso in [Spanish](README.md).{marca}\n"

    def par(self, marca_es, marca_en):
        es = self.ES_BASE.format(marca=marca_es).encode("utf-8")
        return cp.comparar(es, en(self.EN_BASE.format(marca=marca_en), es=es))

    def test_sin_marca_el_enlace_distinto_es_error(self):
        self.assertEqual(errores(self.par("", "")), ["enlaces_difieren"])

    def test_linea_exenta_en_ambos_no_cuenta(self):
        marca = " <!-- i18n:exento -->"
        self.assertEqual(errores(self.par(marca, marca)), [])

    def test_exencion_en_un_solo_lado_sigue_siendo_error(self):
        marca = " <!-- i18n:exento -->"
        self.assertEqual(errores(self.par(marca, "")), ["enlaces_difieren"])
        self.assertEqual(errores(self.par("", marca)), ["enlaces_difieren"])

    def test_la_exencion_no_oculta_el_resto_del_fichero(self):
        marca = " <!-- i18n:exento -->"
        es = self.ES_BASE.format(marca=marca).encode("utf-8")
        trad = en(self.EN_BASE.format(marca=marca).replace("See R1", "See R2"), es=es)
        self.assertEqual(errores(cp.comparar(es, trad)), ["ids_difieren"])


class PruebasCabecera(unittest.TestCase):
    def test_sin_cabecera(self):
        incs = cp.comparar(ES, EN_CUERPO.encode("utf-8"))
        self.assertEqual(errores(incs), ["cabecera_ausente"])

    def test_cabecera_mal_formada(self):
        malo = ("<!-- i18n fuente-sha256=XYZ estado=borrador-ia -->\n\n" + EN_CUERPO).encode("utf-8")
        self.assertEqual(errores(cp.comparar(ES, malo)), ["cabecera_mal_formada"])

    def test_estado_desconocido(self):
        malo = en().replace(b"borrador-ia", b"revisado")
        self.assertEqual(errores(cp.comparar(ES, malo)), ["cabecera_mal_formada"])

    def test_fuente_desfasada(self):
        otro = ES + b"\nUna regla nueva.\n"
        self.assertEqual(errores(cp.comparar(otro, en())), ["fuente_desfasada"])

    def test_revisado_humano_sin_revisor(self):
        self.assertEqual(errores(cp.comparar(ES, en(estado="revisado-humano"))), ["estado_sin_revisor"])

    def test_revisado_humano_con_revisor(self):
        self.assertEqual(errores(cp.comparar(ES, en(estado="revisado-humano", extra=" revisor=Ana"))), [])

    def test_hash_es_determinista_y_de_12_hex(self):
        h = cp.hash_fuente(ES)
        self.assertEqual(h, cp.hash_fuente(ES))
        self.assertRegex(h, r"^[0-9a-f]{12}$")
        self.assertNotEqual(h, cp.hash_fuente(ES + b" "))


class PruebasNotaYTextoSinTraducir(unittest.TestCase):
    NOTA = "AI-assisted; requires human review."

    def test_nota_ausente(self):
        incs = cp.comparar(ES, en(), nota_ia=self.NOTA)
        self.assertEqual(errores(incs), ["nota_ia_ausente"])

    def test_nota_presente_al_final(self):
        incs = cp.comparar(ES, en(EN_CUERPO + "\n---\n\n" + self.NOTA + "\n"), nota_ia=self.NOTA)
        self.assertNotIn("nota_ia_ausente", codigos(incs))

    def test_sin_nota_pedida_no_se_comprueba(self):
        self.assertNotIn("nota_ia_ausente", codigos(cp.comparar(ES, en())))

    def test_parrafo_sin_traducir_es_aviso_no_error(self):
        incs = cp.comparar(ES, en(EN_CUERPO + "\nEste párrafo sigue en español.\n"))
        self.assertIn("texto_sin_traducir", codigos(incs, "aviso"))
        self.assertNotIn("texto_sin_traducir", errores(incs))

    def test_marcas_de_modulo_con_tilde_no_son_texto_sin_traducir(self):
        es = ES + b"\nUsa [h\xc3\xadbrido] y [publicaci\xc3\xb3n].\n"
        trad = en(EN_CUERPO + "\nUse [h\xedbrido] and [publicaci\xf3n].\n", es=es)
        self.assertNotIn("texto_sin_traducir", codigos(cp.comparar(es, trad)))

    def test_texto_en_codigo_con_tilde_no_cuenta(self):
        trad = en(EN_CUERPO + "\nUse `ñandú` here.\n")
        self.assertNotIn("texto_sin_traducir", codigos(cp.comparar(ES, trad)))

    def test_letras_toleradas_no_cuentan_como_texto_sin_traducir(self):
        # En francés «é» es normal; sin tolerarla, el aviso saltaría en cada línea.
        trad = en(EN_CUERPO + "\nUne règle écrite en français.\n")
        self.assertIn("texto_sin_traducir", codigos(cp.comparar(ES, trad)))
        self.assertNotIn("texto_sin_traducir", codigos(cp.comparar(ES, trad, tolera="éÉ")))

    def test_letras_toleradas_no_apagan_el_resto_del_aviso(self):
        # Tolerar «é» no exime «ñ» ni «á»: siguen delatando español sin traducir.
        for resto in ("Il y a mañana.", "Il dit está."):
            trad = en(EN_CUERPO + "\n" + resto + "\n")
            self.assertIn("texto_sin_traducir", codigos(cp.comparar(ES, trad, tolera="éÉ")), resto)

    def test_letras_toleradas_con_caracteres_de_regex_no_rompen(self):
        trad = en(EN_CUERPO + "\nIl dit mañana.\n")
        incs = cp.comparar(ES, trad, tolera="]^-\\")
        self.assertIn("texto_sin_traducir", codigos(incs))

    def test_tolerar_todas_las_letras_no_rompe_la_regex(self):
        trad = en(EN_CUERPO + "\nIl dit mañana.\n")
        incs = cp.comparar(ES, trad, tolera="ñÑ¿¡áéíóúÁÉÍÓÚü")
        self.assertNotIn("texto_sin_traducir", codigos(incs))


class PruebasArbol(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.es = os.path.join(self.tmp, "skill")
        self.trad = os.path.join(self.es, "i18n", "en")
        for sub in ("references", "assets"):
            os.makedirs(os.path.join(self.es, sub))
        self.escribir(os.path.join(self.es, "SKILL.md"), ES)
        self.escribir(os.path.join(self.es, "references", "a.md"), b"# A\n\nTexto R1.\n")

    def escribir(self, ruta, datos):
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "wb") as f:
            f.write(datos)

    def traducir_a(self, rel, es_datos, cuerpo):
        self.escribir(os.path.join(self.trad, rel), en(cuerpo, es=es_datos))

    def test_traduccion_completa_sin_errores(self):
        self.traducir_a("SKILL.md", ES, EN_CUERPO)
        self.traducir_a("references/a.md", b"# A\n\nTexto R1.\n", "# A\n\nText R1.\n")
        r = cp.comprobar_arbol(self.es, self.trad, completo=True)
        self.assertEqual(r["errores"], 0, r)

    def test_arbol_tolera_letras_por_linea_de_ordenes(self):
        self.traducir_a("SKILL.md", ES, EN_CUERPO + "\nUne règle écrite en français.\n")
        self.traducir_a("references/a.md", b"# A\n\nTexto R1.\n", "# A\n\nText R1.\n")
        os.makedirs(os.path.join(self.trad, "references"), exist_ok=True)
        base = [sys.executable, "-B", "-I", SCRIPT, "--arbol", self.es, self.trad, "--json"]
        sin = subprocess.run(base, capture_output=True, text=True)
        self.assertIn("texto_sin_traducir", sin.stdout)
        con = subprocess.run(base + ["--tolera-letras", "éÉ"], capture_output=True, text=True)
        self.assertNotIn("texto_sin_traducir", con.stdout, con.stdout + con.stderr)

    def test_enlace_roto_en_la_traduccion(self):
        self.traducir_a("SKILL.md", ES, EN_CUERPO)  # apunta a references/a.md dentro de i18n/en, que no existe
        r = cp.comprobar_arbol(self.es, self.trad)
        cods = [i["codigo"] for f in r["ficheros"] for i in f["incidencias"]]
        self.assertIn("enlace_roto", cods)

    def test_traduccion_ausente_es_aviso_y_con_completo_es_error(self):
        self.traducir_a("SKILL.md", ES, EN_CUERPO)
        r = cp.comprobar_arbol(self.es, self.trad)
        ausentes = [i for f in r["ficheros"] for i in f["incidencias"] if i["codigo"] == "traduccion_ausente"]
        self.assertEqual([i["severidad"] for i in ausentes], ["aviso"])
        r = cp.comprobar_arbol(self.es, self.trad, completo=True)
        ausentes = [i for f in r["ficheros"] for i in f["incidencias"] if i["codigo"] == "traduccion_ausente"]
        self.assertEqual([i["severidad"] for i in ausentes], ["error"])

    def test_traduccion_sin_original(self):
        self.escribir(os.path.join(self.trad, "references", "huerfano.md"), b"x\n")
        r = cp.comprobar_arbol(self.es, self.trad)
        cods = [i["codigo"] for f in r["ficheros"] for i in f["incidencias"]]
        self.assertIn("traduccion_sin_original", cods)

    def test_no_compara_scripts_ni_la_propia_carpeta_i18n(self):
        self.escribir(os.path.join(self.es, "scripts", "x.py"), b"print(1)\n")
        self.traducir_a("SKILL.md", ES, EN_CUERPO)
        r = cp.comprobar_arbol(self.es, self.trad)
        rutas = [f["ruta"] for f in r["ficheros"]]
        self.assertFalse(any(x.startswith("scripts") or x.startswith("i18n") for x in rutas))


class PruebasCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.es = os.path.join(self.tmp, "es.md")
        self.en = os.path.join(self.tmp, "en.md")
        with open(self.es, "wb") as f:
            f.write(ES)

    def ejecutar(self, *args):
        return subprocess.run([sys.executable, "-B", "-I", SCRIPT] + list(args), capture_output=True, text=True)

    def test_par_correcto_sale_0(self):
        with open(self.en, "wb") as f:
            f.write(en())
        r = self.ejecutar("--par", self.es, self.en)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_par_con_discrepancia_sale_1_y_json_valido(self):
        with open(self.en, "wb") as f:
            f.write(en(EN_CUERPO.replace("End R1", "End R2")))
        r = self.ejecutar("--par", self.es, self.en, "--json")
        self.assertEqual(r.returncode, 1)
        self.assertIn("ids_difieren", json.dumps(json.loads(r.stdout)))

    def test_estricto_convierte_avisos_en_fallo(self):
        with open(self.en, "wb") as f:
            f.write(en(EN_CUERPO + "\nEste párrafo sigue en español.\n"))
        self.assertEqual(self.ejecutar("--par", self.es, self.en).returncode, 0)
        self.assertEqual(self.ejecutar("--par", self.es, self.en, "--estricto").returncode, 1)

    def test_tolera_letras_por_linea_de_ordenes(self):
        with open(self.en, "wb") as f:
            f.write(en(EN_CUERPO + "\nUne règle écrite en français.\n"))
        sin = self.ejecutar("--par", self.es, self.en, "--json")
        self.assertIn("texto_sin_traducir", sin.stdout)
        con = self.ejecutar("--par", self.es, self.en, "--json", "--tolera-letras", "éÉ")
        self.assertEqual(con.returncode, 0, con.stdout + con.stderr)
        self.assertNotIn("texto_sin_traducir", con.stdout)

    def test_hash(self):
        r = self.ejecutar("--hash", self.es)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), cp.hash_fuente(ES))

    def test_fichero_inexistente_sale_2(self):
        self.assertEqual(self.ejecutar("--par", self.es, os.path.join(self.tmp, "no.md")).returncode, 2)

    def test_no_utf8_sale_2_sin_traza(self):
        with open(self.en, "wb") as f:
            f.write(b"\xff\xfe\x00 roto")
        r = self.ejecutar("--par", self.es, self.en)
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("Traceback", r.stderr)

    def test_sin_argumentos_sale_2(self):
        self.assertEqual(self.ejecutar().returncode, 2)

    def test_par_en_subcarpeta_necesita_las_raices(self):
        raiz = os.path.join(self.tmp, "skill")
        trad = os.path.join(raiz, "i18n", "en")
        es_datos = b"# A\n\nVer [b](../assets/b.md).\n"
        for ruta, datos in (("references/a.md", es_datos), ("assets/b.md", b"# B\n")):
            os.makedirs(os.path.dirname(os.path.join(raiz, ruta)), exist_ok=True)
            with open(os.path.join(raiz, ruta), "wb") as f:
                f.write(datos)
        os.makedirs(os.path.join(trad, "references"), exist_ok=True)
        with open(os.path.join(trad, "references", "a.md"), "wb") as f:
            f.write(en("# A\n\nSee [b](../assets/b.md).\n", es=es_datos))
        par = ("--par", os.path.join(raiz, "references", "a.md"), os.path.join(trad, "references", "a.md"))
        self.assertEqual(self.ejecutar(*par).returncode, 1)  # sin raíces, el enlace parece distinto
        con_raices = par + ("--raiz-es", raiz, "--raiz-trad", trad)
        self.assertEqual(self.ejecutar(*con_raices).returncode, 0)

    def test_raices_solo_con_par(self):
        self.assertEqual(self.ejecutar("--hash", self.es, "--raiz-es", self.tmp).returncode, 2)

    def test_no_escribe_ficheros(self):
        with open(self.en, "wb") as f:
            f.write(en())
        antes = sorted(os.listdir(self.tmp))
        self.ejecutar("--par", self.es, self.en)
        self.ejecutar("--hash", self.es)
        self.assertEqual(sorted(os.listdir(self.tmp)), antes)


class PruebasTotalidad(unittest.TestCase):
    def test_entradas_aleatorias_no_hacen_fallar(self):
        azar = random.Random(20261011)
        trozos = ["# ", "## ", "```", "```bash\n", "|", "R1", "D4", "[instrucciones]", "](", "ñ", "\n", " ",
                  "<!-- i18n fuente-sha256=", "[x](", "../", "#", "Doc9", "\r\n", "\x00", "é"]
        for _ in range(300):
            a = "".join(azar.choice(trozos) for _ in range(azar.randint(0, 40))).encode("utf-8")
            b = "".join(azar.choice(trozos) for _ in range(azar.randint(0, 40))).encode("utf-8")
            incs = cp.comparar(a, b)
            self.assertIsInstance(incs, list)

    def test_bytes_no_utf8_son_una_incidencia(self):
        self.assertEqual(errores(cp.comparar(b"\xff", b"x")), ["no_utf8"])
        self.assertEqual(errores(cp.comparar(b"x", b"\xff")), ["no_utf8"])


if __name__ == "__main__":
    unittest.main()

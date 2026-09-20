#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mantiene el aparato de referencias numeradas de un ensayo en Markdown.

Invariante que sostiene:
  - ninguna referencia citada en el cuerpo sin entrada en la bibliografía
  - ninguna entrada de bibliografía sin uso en el cuerpo
  - numeración en orden de primera aparición

Uso:
    referencias.py verificar  ensayo.md
    referencias.py renumerar  ensayo.md [--nuevas nuevas.json] [--seccion "## Bibliografía"]

Para agregar citas a un ensayo ya numerado: insertar en el cuerpo un token alfabético
(por ejemplo [MILLER]), poner su entrada en un JSON {"MILLER": "Miller, Chris. ..."} y
correr `renumerar`. El script reasigna todos los números y reconstruye la bibliografía.
"""

import argparse
import io
import json
import re
import sys

SECCION_POR_DEFECTO = "## Bibliografía"

# Un marcador es [12] o [TOKEN], donde TOKEN empieza con letra mayúscula y puede
# contener dígitos. El dígito interior importa: [W3TECHS] debe calzar.
MARCADOR = r"\[([A-Z][A-Z0-9_-]*|\d+)\]"


def partir(texto, seccion):
    if seccion not in texto:
        sys.exit("No encontré la sección '%s' en el archivo." % seccion)
    cuerpo, biblio = texto.split(seccion, 1)
    return cuerpo, biblio


def leer_biblio(biblio):
    """Devuelve {numero_como_str: entrada} preservando entradas multilínea."""
    entradas = {}
    for m in re.finditer(r"^\[(\d+)\] (.*?)(?=\n\n\[\d+\] |\Z)", biblio.strip(), re.S | re.M):
        entradas[m.group(1)] = m.group(2).strip()
    return entradas


def tokens_en_orden(cuerpo):
    vistos = []
    for tk in re.findall(MARCADOR, cuerpo):
        if tk not in vistos:
            vistos.append(tk)
    return vistos


def informe(cuerpo, entradas_por_numero):
    citados = sorted({int(x) for x in re.findall(r"\[(\d+)\]", cuerpo)})
    definidos = sorted(int(x) for x in entradas_por_numero)
    aparicion = []
    for x in re.findall(r"\[(\d+)\]", cuerpo):
        n = int(x)
        if n not in aparicion:
            aparicion.append(n)

    sueltos = sorted(set(re.findall(r"\[[A-Z][A-Z0-9_-]*\]", cuerpo)))
    huerfanas = [n for n in citados if n not in definidos]
    sin_usar = [n for n in definidos if n not in citados]
    ascendente = aparicion == sorted(aparicion)
    esperado = list(range(1, len(definidos) + 1))

    print("referencias definidas : %d" % len(definidos))
    print("numeración 1..N       : %s" % ("sí" if definidos == esperado else "NO — %s" % definidos))
    print("huérfanas             : %s" % (huerfanas or "ninguna"))
    print("definidas sin usar    : %s" % (sin_usar or "ninguna"))
    print("orden de aparición    : %s" % ("ascendente" if ascendente else "NO ascendente"))
    print("tokens sin numerar    : %s" % (", ".join(sueltos) if sueltos else "ninguno"))

    ok = (not huerfanas) and (not sin_usar) and ascendente and (definidos == esperado) and (not sueltos)
    print("\n%s" % ("OK" if ok else "REVISAR"))
    return 0 if ok else 1


def verificar(ruta, seccion):
    texto = io.open(ruta, encoding="utf-8").read()
    cuerpo, biblio = partir(texto, seccion)
    return informe(cuerpo, leer_biblio(biblio))


def renumerar(ruta, seccion, ruta_nuevas):
    texto = io.open(ruta, encoding="utf-8").read()
    cuerpo, biblio = partir(texto, seccion)

    entradas = leer_biblio(biblio)
    if ruta_nuevas:
        nuevas = json.load(io.open(ruta_nuevas, encoding="utf-8"))
        chocan = [k for k in nuevas if k in entradas]
        if chocan:
            sys.exit("Estos tokens ya existen en la bibliografía: %s" % ", ".join(chocan))
        entradas.update(nuevas)

    orden = tokens_en_orden(cuerpo)
    if not orden:
        sys.exit("No encontré marcadores de referencia en el cuerpo.")

    faltan = [tk for tk in orden if tk not in entradas]
    if faltan:
        sys.exit("Estos tokens se citan en el cuerpo pero no tienen entrada: %s" % ", ".join(faltan))

    sin_usar = [tk for tk in entradas if tk not in orden]
    if sin_usar:
        print("Aviso: entradas sin uso en el cuerpo, se descartan: %s" % ", ".join(sorted(sin_usar)),
              file=sys.stderr)

    mapa = {tk: i + 1 for i, tk in enumerate(orden)}
    cuerpo_nuevo = re.sub(MARCADOR, lambda m: "[%d]" % mapa[m.group(1)], cuerpo)
    lineas = "\n\n".join("[%d] %s" % (mapa[tk], entradas[tk]) for tk in orden)

    io.open(ruta, "w", encoding="utf-8").write(cuerpo_nuevo + seccion + "\n\n" + lineas + "\n")
    print("Renumeradas %d referencias.\n" % len(orden))
    return informe(cuerpo_nuevo, {str(mapa[tk]): entradas[tk] for tk in orden})


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("accion", choices=["verificar", "renumerar"])
    ap.add_argument("ensayo")
    ap.add_argument("--nuevas", help="JSON {token: entrada bibliográfica}")
    ap.add_argument("--seccion", default=SECCION_POR_DEFECTO,
                    help="Encabezado de la bibliografía (por defecto: %s)" % SECCION_POR_DEFECTO)
    a = ap.parse_args()

    if a.accion == "verificar":
        if a.nuevas:
            sys.exit("--nuevas solo aplica a 'renumerar'.")
        sys.exit(verificar(a.ensayo, a.seccion))
    sys.exit(renumerar(a.ensayo, a.seccion, a.nuevas))


if __name__ == "__main__":
    main()

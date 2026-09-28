# <Nombre del proyecto>

Plantilla de convenciones para un repositorio de ensayos asistido por agentes. Reemplazar lo que está entre `<>` y borrar esta línea.

## Objetivo

El objetivo de este repositorio es asistir la escritura de <N> ensayos a través de la recopilación de fuentes, revisión de ideas y correcciones de forma. Estos ensayos son:

- <Título del ensayo 1>
- <Título del ensayo 2>

Serán publicados en <medio>.

## Forma de operación de los agentes

Deben:

- Recopilar información y fichar cada fuente en `fuentes/` antes de usarla.
- Revisar críticamente ideas, buscando el mejor contraargumento disponible.
- Verificar datos y citas que ya estén en `ensayos/`, y reportar los que no cuadren.
- Señalar problemas formales en viñetas, sin redactar el reemplazo.
- Proponer ideas en `ideas.md`, en viñetas, siempre indicando a qué ensayo corresponden.

Pueden:

- Escribir un borrador estructural en viñetas si el humano lo solicita.
- Señalar qué deberían comunicar el título y la bajada, sin redactarlos.
- Señalar qué falta investigar: preguntas abiertas, huecos del argumento, fuentes que faltan.
- Armar la bibliografía final a partir de `fuentes/`.
- Hacer preguntas al humano cuando una idea sea ambigua, en vez de resolverla por su cuenta.

No deben:

- Escribir prosa: ni párrafos, ni frases listas para pegar, ni borradores del ensayo. La prosa es del humano.
- Editar `ensayos/`. Nunca, ni siquiera con autorización. La única excepción es correr `referencias.py renumerar`, que solo toca números de cita y bibliografía.

## Estructura

```
.
├── AGENTS.md        # Este archivo
├── ideas.md         # Bitácora append-only de los agentes
├── ensayos/         # Los ensayos. Solo los escribe el humano
├── fuentes/         # Una ficha por fuente
├── borradores/      # Borradores estructurales, versionados
└── assets/          # Imágenes y material de apoyo
```

Idioma del repo: <idioma>.

## Identificadores de ensayo

Toda entrada de `ideas.md` y toda ficha de `fuentes/` se etiqueta con un identificador.

| ID | Ensayo |
| --- | --- |
| `<id-1>` | <Título del ensayo 1> |
| `<id-2>` | <Título del ensayo 2> |
| `general` | No aplica a ninguno todavía |

Si algo sirve a más de un ensayo, se listan separados por coma.


## Los ensayos

### <Título del ensayo 1>

- **ID:** `<id-1>`
- **Archivo:** [ensayos/<archivo>.md](ensayos/<archivo>.md)
- **Assets:** <>
- **Estado:** <sin empezar | en curso | terminado>

**Sinopsis (del autor).** <Qué quiere decir el ensayo, en palabras del autor.>

**Qué debe lograr:**

- <>

**Pendientes:**

- <>

## Convenciones de escritura

El formato de cada artefacto está en el skill `asistente-editor`:

- Entradas de `ideas.md`: `plantillas/entrada-ideas.md`
- Fichas de `fuentes/`: `plantillas/ficha-fuente.md`
- Borradores estructurales: `plantillas/borrador-estructural.md`

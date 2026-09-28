# asistente-editor

Un skill para escribir ensayos de no ficción con asistencia de IA, sin que la IA escriba el ensayo.

Nació escribiendo ensayos que publicaba en mi Substack. El método que quedó acá es el que sobrevivió a ese proceso: fuentes fichadas antes de usarlas, auditoría adversarial en rondas, y un aparato de referencias que se verifica solo.

## La idea

Los LLMs realmente no escriben tan bien. Son correctos en uso de reglas y plausibilidad, pero pueden inventar cosas y escriben con poca "alma".

Este skill parte del siguiente principio: **el agente no escribe el ensayo**. Asiste en el trabajo de edición y recopilación:

- Busca y ficha fuentes, una por archivo, con extractos literales y localizador.
- Verifica cada afirmación contra fuente primaria, y dice cuando no pudo.
- Critica el texto como lo haría un lector hostil e informado.
- Mantiene las referencias numeradas sin huérfanas ni entradas muertas.

El autor escribe. El agente hace que lo escrito aguante una lectura adversarial.

## Qué hace distinto

**Territorios separados.** `ensayos/` es exclusivamente del humano. El agente escribe en `ideas.md`, `fuentes/` y `borradores/`, y no edita el ensayo nunca, ni siquiera con autorización. La única excepción es mecánica: renumerar las citas.

**La objeción es de primera clase.** Contradecir la tesis del autor es trabajo esperado, no una molestia. El skill pide buscar el mejor contraargumento disponible, no el más fácil de derribar. Las fuentes que contradicen el ensayo se fichan igual, y son las más valiosas.

**La objeción correcta se convierte en argumento.** Si un dato incómodo ilustra la tesis, va en el texto y se dice antes de que lo diga otro. Reconocer que la telemetría de una faena minera pertenece al proveedor extranjero fortalece un ensayo sobre soberanía de datos. Esconderlo lo hace vulnerable.

**Bitácora append-only.** `ideas.md` registra qué se cambió, qué no se cambió y por qué. Incluye lo que no se pudo verificar. Eso evita reabrir discusiones ya cerradas.

**La prosa es humana.** Todo lo que el agente propone (ideas, estructura, objeciones, correcciones) va en viñetas. Ni párrafos sugeridos ni frases listas para pegar: el autor convierte los puntos en texto con sus palabras. Una corrección dice dónde está el problema y qué tiene que lograr el arreglo, nunca cómo redactarlo.

## Instalación

Como skill de usuario, disponible en todos tus proyectos:

```bash
git clone https://github.com/goyanedelv/asistente-editor.git ~/.claude/skills/asistente-editor
```

O como skill de un proyecto, versionado junto al repo del ensayo:

```bash
git clone https://github.com/goyanedelv/asistente-editor.git .claude/skills/asistente-editor
```

Luego, en Claude Code:

```
/asistente-editor
```

## Estructura del repositorio de ensayos

```
.
├── AGENTS.md        # Convenciones del proyecto y ficha de cada ensayo
├── ideas.md         # Bitácora append-only. Único lugar donde el agente escribe ideas
├── ensayos/         # Los ensayos. Territorio del humano
├── fuentes/         # Una ficha por fuente
├── borradores/      # Borradores estructurales, versionados
└── assets/          # Imágenes y material de apoyo
```

`plantillas/` tiene el formato de cada artefacto, incluido un `AGENTS.md` para empezar un proyecto nuevo.

## El script de referencias

Mantiene el invariante de un ensayo con citas numeradas en texto: sin huérfanas, sin entradas sin usar, numeración en orden de primera aparición.

```bash
python3 scripts/referencias.py verificar ensayos/mi-ensayo.md
```

```
referencias definidas : 36
numeración 1..N       : sí
huérfanas             : ninguna
definidas sin usar    : ninguna
orden de aparición    : ascendente
tokens sin numerar    : ninguno

OK
```

`verificar` solo lee. `renumerar` es lo único que el agente escribe en un ensayo, y solo toca números y bibliografía. Para agregar citas a un ensayo ya numerado, se inserta en el cuerpo un token alfabético y su entrada en un JSON:

```bash
echo '{"MILLER": "Miller, Chris. *Chip War*. Scribner, 2022."}' > nuevas.json
python3 scripts/referencias.py renumerar ensayos/mi-ensayo.md --nuevas nuevas.json
```

El script reasigna todos los números por orden de aparición y reconstruye la bibliografía. Renumerar a mano es una fuente confiable de errores silenciosos: un token con un dígito adentro que no calza con la expresión regular, o una inserción temprana que desplaza treinta referencias.

## Qué aprendió este skill a la mala

Cada una de estas reglas está acá porque el error ocurrió.

- Una cifra repetida en toda la prensa puede ser falsa. La cuota de mercado más citada de una empresa resultó ser la composición interna de sus ingresos.
- Un ranking tiene subtablas. La posición que devuelve un buscador puede venir de una lista parcial de 27 países y no del ranking de 69.
- Las proyecciones oficiales se revisan. Una de hace dieciocho meses puede estar reemplazada por otra del mismo organismo.
- Dos fuentes que parecen medir lo mismo miden cosas distintas. Hablantes de un idioma y páginas web en ese idioma no son el mismo número ni la misma fuente.
- Un ejemplo que suena perfecto puede no existir. Vale la pena buscar el paper antes de que lo busque un lector.
- Una contradicción lógica interna es peor que un dato malo, porque no se arregla con una fuente.

## Licencia

MIT.

# Daypo Gen

Herramienta para generar tests de Daypo a partir de un JSON de preguntas y una plantilla XML exportada de Daypo. Cabe recalcar que es un script que funciona de aquella manera; lo creé solo para usarlo en mis estudios, así que no es algo completamente útil, por así decirlo.

## Cómo funciona

El script toma un JSON con las preguntas y las inyecta en una plantilla XML válida de Daypo, produciendo un archivo listo para importar.
La gran limitación es que el XML que toma Daypo necesita dos números específicos que sinceramente no sé cómo generar ni tampoco quiero investigar, así que hace falta descargar un XML de Daypo para usar como plantilla.
Para esto, solo tenemos que entrar en la página de creación de Daypo, crear un test con su título, descripción, etc., y al menos una pregunta con su respuesta. Cualquier pregunta vale, incluso letras aleatorias.
Luego le damos a publicar, nos metemos en nuestro perfil donde nos tiene que aparecer el test, le damos a editar y luego a guardar para que se nos descargue el XML que usamos como plantilla.
Una vez tengamos este XML y el JSON, los pasamos por el script, nos da el XML final, entramos en nuestro test de Daypo, le damos a cargar y, en vez del XML plantilla que nos descargó al principio, seleccionamos el que nos ha dado el script.

## Requisitos

- Python 3

## Uso

```bash
python daypo_gen.py
```

El script pedirá tres rutas (IMPORTANTE: todas las rutas deben tener su extensión para que el programa las detecte bien. Ejemplo: preguntas.json, plantilla.xml, test_final.xml):

1. **Archivo de preguntas** — JSON con las preguntas a generar.
2. **Plantilla** — XML exportado de Daypo que sirve de base (debe tener al menos una pregunta dummy).
3. **Archivo de salida** — Nombre del XML resultante listo para subir a Daypo.

## Formato del JSON de preguntas

```json
{
  "preguntas": [
    {
      "pregunta": "¿Enunciado de la pregunta?",
      "opciones": ["Opción A", "Opción B", "Opción C", "Opción D"],
      "correcta": 0
    }
  ]
}
```

- `correcta`: índice (0-3) de la opción correcta.
- Cada pregunta DEBE TENER EXACTAMENTE 4 opciones.

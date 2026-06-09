import json

def indice_a_patron(indice):
    if indice == 0:
        return "2111"
    elif indice == 1:
        return "1211"
    elif indice == 2:
        return "1121"
    elif indice == 3:
        return "1112"
    else:
        raise ValueError("Índice de respuesta correcta fuera de rango (0-3)")

def limpiar_texto(txt: str) -> str:
    # Limpieza mínima para evitar problemas con < y >
    return (txt
            .replace('<<include>>', 'include')
            .replace('<<extend>>', 'extend')
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            )

def generar_bloque_preguntas(preguntas):
    partes = []
    partes.append('<c>')  # contenedor de preguntas

    for q in preguntas:
        enunciado = limpiar_texto(q["pregunta"])
        opciones = [limpiar_texto(o) for o in q["opciones"]]
        correcta = q["correcta"]

        if len(opciones) != 4:
            raise ValueError(f"La pregunta '{enunciado}' no tiene exactamente 4 opciones")

        patron = indice_a_patron(correcta)

        partes.append('<c>')
        partes.append('<t>0</t>')
        partes.append(f'<p>{enunciado}</p>')
        partes.append(f'<c>{patron}</c>')
        partes.append('<r>')
        for o in opciones:
            partes.append(f'<o>{o}</o>')
        partes.append('</r></c>')

    partes.append('</c>')
    return ''.join(partes)

def reemplazar_preguntas_en_plantilla(xml_plantilla: str, bloque_preguntas: str) -> str:
    """
    xml_plantilla: contenido del XML exportado de Daypo (funcional)
    bloque_preguntas: string que empieza por <c><c><t>0</t>... y termina en </c>
    Sustituye desde el primer <c><t>0</t>... hasta la secuencia </c><i/></test>.
    """
    # Encontrar el inicio del bloque de preguntas:
    # buscamos el contenedor <c> que contiene preguntas; simplificación:
    # asumimos que la primera pregunta empieza en "<c><t>0</t>"
    idx_start_question = xml_plantilla.find('<c><t>0</t>')
    if idx_start_question == -1:
        raise ValueError("No se ha encontrado ninguna pregunta (<c><t>0</t>) en la plantilla.")

    # Antes de la primera pregunta siempre hay un <c> (contenedor); retrocedemos hasta ese <c>
    idx_start_container = xml_plantilla.rfind('<c>', 0, idx_start_question)
    if idx_start_container == -1:
        raise ValueError("No se ha encontrado el contenedor <c> de preguntas en la plantilla.")

    # Encontrar el final: queremos sustituir hasta justo antes de <i/>
    idx_i = xml_plantilla.rfind('<i/>')
    if idx_i == -1:
        raise ValueError("No se ha encontrado <i/> en la plantilla.")

    # Todo lo entre idx_start_container y idx_i se reemplaza por bloque_preguntas
    header = xml_plantilla[:idx_start_container]
    tail = xml_plantilla[idx_i:]  # incluye <i/></test>

    return header + bloque_preguntas + tail

if __name__ == "__main__":
    # 1) JSON con TODAS tus preguntas (200 o las que sean)

    preguntas_file = input("Introduce el nombre del archivo con las preguntas: ")
    plantilla_file = input("Introduce el nombre del sujeto de pruebas: ")
    resultado_file = input("Introduce el nombre de frankestein: ")

    with open(preguntas_file, "r", encoding="utf-8") as f:
        datos = json.load(f)
    preguntas = datos["preguntas"]

    # 2) XML de plantilla exportado de Daypo (uno que se publique bien)
    #    Debe incluir ya el encabezado correcto y al menos una pregunta dummy.
    with open(plantilla_file, "r", encoding="utf-8") as f:
        xml_plantilla = f.read().strip()

    # 3) Generar bloque de preguntas nuevo
    bloque_preguntas = generar_bloque_preguntas(preguntas)

    # 4) Reemplazar bloque en la plantilla
    xml_final = reemplazar_preguntas_en_plantilla(xml_plantilla, bloque_preguntas)

    # 5) Guardar resultado listo para subir
    with open(resultado_file, "w", encoding="utf-8") as f:
        f.write(xml_final)
    print(f"Generado {resultado_file}")

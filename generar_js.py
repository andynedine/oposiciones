import re

def procesar_respuestas_y_generar_js(archivo_respuestas):
    # Leer el archivo completo
    with open(archivo_respuestas, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    tema_actual = None
    preguntas_por_tema = {}
    pregunta_actual = {}
    opciones_actuales = []
    acumulador = ""

    for linea in lineas:
        linea = linea.strip()

        # Detectar inicio de un tema (Ejemplo: "Tema 1. Título del tema")
        if linea.startswith("Tema") and re.match(r"Tema\s+\d+\.", linea):
            # Guardar el tema anterior si hay preguntas acumuladas
            if tema_actual and pregunta_actual:
                pregunta_actual["opciones"] = opciones_actuales
                preguntas_por_tema[tema_actual].append(pregunta_actual)
            if tema_actual and opciones_actuales:
                opciones_actuales = []

            # Extraer número del tema
            tema_actual = re.match(r"Tema\s+(\d+)\.", linea).group(1)
            preguntas_por_tema[tema_actual] = []
            pregunta_actual = {}
            acumulador = ""  # Reiniciar acumulador

        # Detectar una pregunta (Ejemplo: "1.- Pregunta...")
        elif re.match(r"\d+\.\-", linea):
            # Guardar la pregunta anterior si existe
            if pregunta_actual:
                pregunta_actual["opciones"] = opciones_actuales
                preguntas_por_tema[tema_actual].append(pregunta_actual)
                opciones_actuales = []

            # Nueva pregunta: Extraer número y texto inicial
            numero_pregunta, texto_pregunta = linea.split(".-", 1)
            pregunta_actual = {"pregunta": texto_pregunta.strip()}
            acumulador = "pregunta"  # Indicar que estamos procesando una pregunta multilínea

        # Detectar opciones de respuesta (Ejemplo: "a) Respuesta...")
        elif re.match(r"[a-d]\)", linea):
            opciones_actuales.append(linea[3:].strip())  # Extraer texto de la opción sin "a) "
            acumulador = "opciones"  # Indicar que estamos procesando opciones multilínea

        # Detectar respuesta correcta (Ejemplo: "[A]")
        elif re.match(r"\[[A-D]\]", linea):
            respuesta_correcta = linea[1].strip()  # Extraer la letra de la respuesta correcta
            respuesta_index = ord(respuesta_correcta) - ord("A")  # Convertir A/B/C/D a índice
            pregunta_actual["respuesta"] = opciones_actuales[respuesta_index]

        # Continuar acumulando líneas multilínea
        elif linea:
            if acumulador == "pregunta":
                pregunta_actual["pregunta"] += " " + linea.strip()
            elif acumulador == "opciones" and opciones_actuales:
                opciones_actuales[-1] += " " + linea.strip()

    # Guardar la última pregunta del último tema
    if tema_actual and pregunta_actual:
        pregunta_actual["opciones"] = opciones_actuales
        preguntas_por_tema[tema_actual].append(pregunta_actual)

    # Generar archivos JS por tema
    for tema, preguntas in preguntas_por_tema.items():
        archivo_js = f"tema{tema}.js"
        with open(archivo_js, "w", encoding="utf-8") as f:
            f.write(f"const tema{tema} = [\n")
            for pregunta in preguntas:
                f.write("    {\n")
                f.write(f"        pregunta: \"{pregunta['pregunta']}\",\n")
                f.write(f"        opciones: {pregunta['opciones']},\n")
                f.write(f"        respuesta: \"{pregunta['respuesta']}\"\n")
                f.write("    },\n")
            f.write("];\n\n")
            f.write(f"export default tema{tema};\n")
        print(f"Archivo generado: {archivo_js}")


# Procesar el archivo respuestas.txt
procesar_respuestas_y_generar_js("respuestas.txt")

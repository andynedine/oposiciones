import re

def procesar_preguntas_y_respuestas(preguntas_file, respuestas_file, archivo_salida):
    # Leer preguntas
    with open(preguntas_file, "r", encoding="utf-8") as f:
        preguntas = f.readlines()

    # Leer respuestas (ignorando las dos primeras líneas)
    with open(respuestas_file, "r", encoding="utf-8") as f:
        respuestas_brutas = f.readlines()[2:]

    # Procesar respuestas en un diccionario
    respuestas_dict = {}
    for linea in respuestas_brutas:
        # Cada línea tiene pares de "<número> <letra>"
        elementos = linea.split()
        for i in range(0, len(elementos), 2):  # Procesar en pasos de 2 (número y letra)
            numero_pregunta = int(elementos[i])
            respuesta_correcta = elementos[i + 1].strip(".")  # Asegurar que no incluya un punto
            respuestas_dict[numero_pregunta] = respuesta_correcta

    # Procesar preguntas e insertar la respuesta correcta
    resultado = []
    acumulador_tema = []  # Para acumular líneas del bloque del tema
    acumulador_opciones = []  # Para acumular opciones de respuesta
    numero_pregunta = None
    texto_pregunta = ""  # Para acumular el texto completo de la pregunta
    en_opciones = False  # Para indicar si estamos procesando opciones de respuesta

    for i, linea in enumerate(preguntas):
        linea = linea.strip()
        siguiente_linea = preguntas[i + 1].strip() if i + 1 < len(preguntas) else ""

        # Detectar inicio de un nuevo tema
        if re.match(r"Tema\s+\d+\.", linea):
            # Guardar opciones y respuesta correcta de la pregunta previa si existen
            if acumulador_opciones and numero_pregunta in respuestas_dict:
                resultado.append(f"{texto_pregunta}\n")
                resultado.extend(acumulador_opciones)
                resultado.append(f"[{respuestas_dict[numero_pregunta]}]\n")
                acumulador_opciones = []

            # Guardar el bloque del tema actual
            if acumulador_tema:
                resultado.extend(acumulador_tema)
                acumulador_tema = []

            acumulador_tema.append(linea)  # Agregar el inicio del nuevo tema
            en_opciones = False  # Salir del bloque de opciones
            texto_pregunta = ""  # Reiniciar texto de la pregunta
            continue

        # Detectar el inicio de una nueva pregunta
        if re.match(r"\d+\.-", linea):  # Detecta "X.-" donde X es un número
            # Guardar opciones y respuesta correcta de la pregunta previa
            if acumulador_opciones and numero_pregunta in respuestas_dict:
                resultado.append(f"{texto_pregunta}\n")
                resultado.extend(acumulador_opciones)
                resultado.append(f"[{respuestas_dict[numero_pregunta]}]\n")
                acumulador_opciones = []

            # Agregar el bloque del tema actual
            if acumulador_tema:
                resultado.extend(acumulador_tema)
                acumulador_tema = []

            # Registrar la nueva pregunta y reiniciar acumuladores
            numero_pregunta = int(linea.split(".-")[0].strip())
            texto_pregunta = linea  # Inicializar el texto de la nueva pregunta
            en_opciones = True  # Entramos en el bloque de opciones
            continue

        # Acumular texto de la pregunta si estamos en la sección de preguntas
        if en_opciones and not linea.startswith(("a)", "b)", "c)", "d)")):
            texto_pregunta += f" {linea.strip()}"
            continue

        # Detectar opciones de respuesta (a), b), c), d))
        if en_opciones and linea.startswith(("a)", "b)", "c)", "d)")):
            acumulador_opciones.append(linea)  # Iniciar una nueva opción
            continue

        # Continuar acumulando líneas de una opción si no inicia un nuevo bloque
        if en_opciones:
            if re.match(r"Tema\s+\d+\.", siguiente_linea) or re.match(r"\d+\.-", siguiente_linea):
                # Guardar las opciones acumuladas y la respuesta correcta
                if acumulador_opciones and numero_pregunta in respuestas_dict:
                    resultado.append(f"{texto_pregunta}\n")
                    resultado.extend(acumulador_opciones)
                    resultado.append(f"[{respuestas_dict[numero_pregunta]}]\n")
                    acumulador_opciones = []
                en_opciones = False
            elif acumulador_opciones:
                # Añadir texto adicional a la última opción solo si existe
                acumulador_opciones[-1] += f" {linea.strip()}"
        else:
            # Agregar cualquier línea que no sea una pregunta ni opciones
            acumulador_tema.append(linea)

    # Agregar las últimas opciones y respuesta correcta al final del archivo
    if acumulador_opciones and numero_pregunta in respuestas_dict:
        resultado.append(f"{texto_pregunta}\n")
        resultado.extend(acumulador_opciones)
        resultado.append(f"[{respuestas_dict[numero_pregunta]}]\n")

    # Guardar el archivo final
    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.writelines(f"{line}\n" for line in resultado)

    print(f"Archivo generado: {archivo_salida}")


# Procesar los archivos correspondientes
procesar_preguntas_y_respuestas("preguntas1_filtrado.txt", "respuestas1.txt", "respuestas_final_1.txt")
procesar_preguntas_y_respuestas("preguntas2_filtrado.txt", "respuestas2.txt", "respuestas_final_2.txt")

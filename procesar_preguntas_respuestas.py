import re

def insertar_respuestas_correctas(archivo_preguntas, archivo_respuestas, archivo_salida):
    # Leer las preguntas tal como están
    with open(archivo_preguntas, "r", encoding="utf-8") as f:
        preguntas = f.readlines()

    # Leer las respuestas, ignorando las dos primeras líneas
    with open(archivo_respuestas, "r", encoding="utf-8") as f:
        respuestas_brutas = f.readlines()[2:]

    # Procesar las respuestas en un diccionario
    respuestas_dict = {}
    for linea in respuestas_brutas:
        elementos = linea.split()
        for i in range(0, len(elementos), 2):  # Procesar en pares de número-letra
            numero_pregunta = int(elementos[i])
            respuesta_correcta = elementos[i + 1].strip(".")  # Asegurar que no incluya un punto
            respuestas_dict[numero_pregunta] = respuesta_correcta

    # Procesar las preguntas e insertar las respuestas correctas
    resultado = []
    numero_pregunta = None

    for i, linea in enumerate(preguntas):
        linea = linea.strip()

        # Detectar inicio de un nuevo tema
        if re.match(r"Tema\s+\d+\.", linea):
            resultado.append(linea)  # Guardar el título del tema
            continue

        # Detectar inicio de una nueva pregunta
        if re.match(r"\d+\.-", linea):
            numero_pregunta = int(linea.split(".-")[0].strip())  # Extraer número de la pregunta

        # Agregar la línea al resultado
        resultado.append(linea)

        # Detectar el final de una pregunta y sus opciones
        siguiente_linea = preguntas[i + 1].strip() if i + 1 < len(preguntas) else ""
        if re.match(r"\d+\.-", siguiente_linea) or re.match(r"Tema\s+\d+\.", siguiente_linea) or not siguiente_linea:
            # Insertar la respuesta correcta si existe
            if numero_pregunta in respuestas_dict:
                resultado.append(f"[{respuestas_dict[numero_pregunta]}]\n")

    # Guardar el archivo final
    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.writelines(f"{line}\n" for line in resultado)

    print(f"Archivo generado: {archivo_salida}")


# Procesar los archivos de preguntas y respuestas
insertar_respuestas_correctas("preguntas1_filtrado.txt", "respuestas1.txt", "preguntas_salida1.txt")
insertar_respuestas_correctas("preguntas2_filtrado.txt", "respuestas2.txt", "preguntas_salida2.txt")

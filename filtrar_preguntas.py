import re

# Función para filtrar preguntas por tema
def filtrar_preguntas_por_tema(archivo_entrada, temas_requeridos, archivo_salida):
    with open(archivo_entrada, "r", encoding="utf-8") as file:
        lineas = file.readlines()

    # Inicializar variables
    texto_filtrado = ""
    tema_actual = None

    for linea in lineas:
        # Detectar inicio de un tema (Ejemplo: "Tema 5.")
        match_tema = re.match(r"Tema\s+(\d+)\.", linea)
        if match_tema:
            tema_actual = int(match_tema.group(1))  # Extraer número de tema
        # Si el tema actual está en los requeridos, guardar las líneas
        if tema_actual in temas_requeridos:
            texto_filtrado += linea

    # Escribir el archivo filtrado
    with open(archivo_salida, "w", encoding="utf-8") as file:
        file.write(texto_filtrado)
    print(f"Preguntas filtradas guardadas en {archivo_salida}")

# Temas requeridos
temas_pdf1 = [5, 8]  # Temas requeridos de preguntas1.txt
temas_pdf2 = [1, 2, 3, 4, 6, 7, 8]  # Temas requeridos de preguntas2.txt

# Filtrar preguntas de preguntas1.txt
filtrar_preguntas_por_tema("preguntas1.txt", temas_pdf1, "preguntas1_filtrado.txt")

# Filtrar preguntas de preguntas2.txt
filtrar_preguntas_por_tema("preguntas2.txt", temas_pdf2, "preguntas2_filtrado.txt")

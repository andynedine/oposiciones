from pdf2image import convert_from_path
from pytesseract import image_to_string
import pdfplumber

# Función para calcular rangos correctamente
def calcular_rango(total_paginas, inicio, fin):
    """Convierte rangos relativos (negativos o positivos) en índices absolutos."""
    inicio = inicio if inicio >= 0 else total_paginas + inicio
    #fin = fin if fin >= 0 else total_paginas + fin
    fin = total_paginas + fin
    print(f"Rango: {inicio}, {fin}")
    return range(inicio, fin)

# Función para limpiar líneas irrelevantes del texto extraído
def limpiar_lineas_irrelevantes(texto):
    # Frases a ignorar
    frases_irrelevantes = ["V.2", "Temario General. Grupo"]
    
    # Filtrar líneas que no contengan las frases irrelevantes
    lineas_limpias = [
        linea for linea in texto.split("\n")
        if not any(frase in linea for frase in frases_irrelevantes)
    ]
    
    # Reconstruir el texto con las líneas relevantes
    return "\n".join(lineas_limpias)

# Función para extraer texto de un rango de páginas con OCR como respaldo
def extraer_texto_con_respaldo(pdf_path, rango_pagina):
    texto = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_paginas = len(pdf.pages)
            for page_num in rango_pagina:
                if 0 <= page_num < total_paginas:  # Verificar que la página esté en el rango válido
                    page_text = pdf.pages[page_num].extract_text()
                    if page_text:  # Si se extrae texto con pdfplumber
                        #texto += f"--- Página {page_num + 1} ---\n"
                        page_text = limpiar_lineas_irrelevantes(page_text)
                        texto += page_text + "\n"
                    else:  # Si no hay texto, usar OCR
                        print(f"Usando OCR para la página {page_num + 1}")
                        images = convert_from_path(pdf_path, first_page=page_num + 1, last_page=page_num + 1)
                        for image in images:
                            #texto += f"--- Página {page_num + 1} ---\n"
                            texto += image_to_string(image, lang="spa") + "\n"
    except Exception as e:
        print(f"Error al procesar el PDF: {e}")
    return texto

# Función para extraer preguntas y respuestas
def extraer_texto_pdf(pdf_path, rango_preguntas, rango_respuestas, archivo_preguntas, archivo_respuestas):
    with pdfplumber.open(pdf_path) as pdf:
        total_paginas = len(pdf.pages)

        # Calcular rangos absolutos para preguntas y respuestas
        print(f"Preguntas: {total_paginas},{rango_preguntas.start}, {rango_preguntas.stop}")
        rango_preguntas = calcular_rango(total_paginas, rango_preguntas.start, rango_preguntas.stop)
        print(f"Respuestas: {total_paginas},{rango_respuestas.start}, {rango_respuestas.stop}")
        rango_respuestas = calcular_rango(total_paginas, rango_respuestas.start, rango_respuestas.stop)

    # Extraer preguntas
    texto_preguntas = extraer_texto_con_respaldo(pdf_path, rango_preguntas)
    with open(archivo_preguntas, "w", encoding="utf-8") as preguntas_file:
        preguntas_file.write(texto_preguntas)
    print(f"Preguntas guardadas en {archivo_preguntas}")

    # Extraer respuestas
    texto_respuestas = extraer_texto_con_respaldo(pdf_path, rango_respuestas)
    with open(archivo_respuestas, "w", encoding="utf-8") as respuestas_file:
        respuestas_file.write(texto_respuestas)
    print(f"Respuestas guardadas en {archivo_respuestas}")


# Especificaciones de los PDF
pdfs = [
    {
        "pdf_path": "temario-general-a1.pdf",
        "rango_preguntas": range(3, -3),  # Desde la página 4 hasta 3 páginas antes del final
        "rango_respuestas": range(-3, 0),  # Últimas 3 páginas
        "archivo_preguntas": "preguntas1.txt",
        "archivo_respuestas": "respuestas1.txt",
    },
    {
        "pdf_path": "temario-general-a2.pdf",
        "rango_preguntas": range(3, -2),  # Desde la página 4 hasta 2 páginas antes del final
        "rango_respuestas": range(-2, 0),  # Últimas 2 páginas
        "archivo_preguntas": "preguntas2.txt",
        "archivo_respuestas": "respuestas2.txt",
    },
]

# Procesar ambos PDFs
for pdf in pdfs:
    extraer_texto_pdf(
        pdf["pdf_path"],
        pdf["rango_preguntas"],  # Páginas de preguntas
        pdf["rango_respuestas"],  # Páginas de respuestas
        pdf["archivo_preguntas"],
        pdf["archivo_respuestas"],
    )

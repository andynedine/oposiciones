import pdfplumber
import re
from pdf2image import convert_from_path
from pytesseract import image_to_string

# Función para limpiar texto y eliminar espacios adicionales
def limpiar_texto(texto):
    return " ".join(texto.split())

# Función para extraer texto con OCR
def extraer_texto_ocr(pdf_path):
    texto = ""
    images = convert_from_path(pdf_path)
    for image in images:
        texto += image_to_string(image, lang="spa")
    return texto

# Función para extraer texto con pdfplumber
def extraer_texto_pdfplumber(pdf_path):
    texto = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texto_extraido = page.extract_text()
            if texto_extraido:
                texto += texto_extraido + "\n"
    return texto

# Función para extraer preguntas y respuestas del texto
def extraer_preguntas_y_respuestas(texto, temas_interes):
    preguntas_por_tema = {tema: [] for tema in temas_interes.keys()}
    respuestas_correctas = {}

    # Limpiar texto completo
    texto = limpiar_texto(texto)

    # Dividir el texto en líneas
    lineas = texto.split("\n")
    tema_actual = None

    for linea in lineas:
        # Detectar el inicio de un tema
        for tema, titulo in temas_interes.items():
            if titulo.lower() in linea.lower():  # Comparar en minúsculas para evitar errores
                tema_actual = tema
                break

        # Extraer preguntas y opciones si estamos dentro de un tema
        if tema_actual:
            match_pregunta = re.match(r"(\d+\..+)", linea)
            if match_pregunta:
                pregunta_text = match_pregunta.group(1)
                opciones = []
                for i in range(1, 5):  # Intentar capturar a), b), c), d)
                    if len(lineas) > i and re.match(r"[a-d]\)", lineas[i]):
                        opciones.append(lineas[i])
                if len(opciones) == 4:  # Solo considerar si hay 4 opciones
                    preguntas_por_tema[tema_actual].append({
                        "pregunta": pregunta_text,
                        "opciones": opciones
                    })

    return preguntas_por_tema

# Función para generar archivo JS
def generar_js(tema, preguntas):
    file_name = f"tema{tema}.js"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(f"const tema{tema} = [\n")
        for pregunta in preguntas:
            file.write("    {\n")
            file.write(f"        pregunta: \"{pregunta['pregunta']}\",\n")
            file.write(f"        opciones: {pregunta['opciones']},\n")
            file.write(f"        respuesta: \"{pregunta['respuesta']}\"\n")
            file.write("    },\n")
        file.write("];\n\n")
        file.write(f"export default tema{tema};\n")
    print(f"Archivo generado: {file_name}")

# Rutas de los PDFs y temas de interés
pdf_paths = {
    "temario-general-a2.pdf": {
        1: "Tema 1. La Constitución Española de 1978.",
        2: "Tema 2. Organización Territorial del Estado Español.",
        3: "Tema 3. Procedimiento Administrativo Común.",
        4: "Tema 6. Régimen local español.",
        6: "Tema 7. La potestad reglamentaria en la esfera local.",
        7: "Tema 8. Los órganos colegiados locales.",
        8: "Tema 9. Personal al servicio de las entidades locales."
    },
    "temario-general-a1.pdf": {
        5: "Tema 4. El municipio y la provincia en la Ley 5/2010.",
        8: "Tema 5. El presupuesto de las entidades locales."
    }
}

# Extraer texto y generar archivos JS para cada tema
for pdf_path, temas_interes in pdf_paths.items():
    print(f"Procesando {pdf_path}...")
    texto = extraer_texto_pdfplumber(pdf_path)
    if not texto.strip():  # Si no se extrajo texto, usar OCR
        print(f"No se pudo extraer texto con pdfplumber. Usando OCR para {pdf_path}...")
        texto = extraer_texto_ocr(pdf_path)

    preguntas_por_tema = extraer_preguntas_y_respuestas(texto, temas_interes)
    for tema, preguntas in preguntas_por_tema.items():
        generar_js(tema, preguntas)

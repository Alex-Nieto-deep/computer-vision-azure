# Azure Computer Vision Project

Este proyecto utiliza el servicio de Azure Computer Vision para analizar una imagen, obtener una descripción en lenguaje natural, traducirla a otro idioma utilizando la biblioteca `translate`, y devolver la imagen original con recuadros delimitadores alrededor de los objetos detectados.

## Características

- **Descripción de la Imagen**: Genera una descripción de la imagen proporcionada utilizando Azure Computer Vision.
- **Traducción de la Descripción**: La descripción generada se traduce automáticamente al idioma deseado utilizando la biblioteca `translate`.
- **Detección de Objetos**: Los objetos en la imagen son detectados y marcados con recuadros delimitadores (bounding boxes).
- **Interfaz Gradio**: Incluye una interfaz gráfica construida con Gradio para cargar imágenes, seleccionar el idioma de traducción y visualizar los resultados.

## Requisitos

- Python 3.7+
- Una cuenta de Azure con acceso al servicio de Computer Vision
- Las siguientes bibliotecas de Python:

```bash
pip install -r requirements.txt
```

## Uso

```bash
python -u app.py
```

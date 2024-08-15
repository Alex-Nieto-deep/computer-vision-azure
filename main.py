import io
from dotenv import load_dotenv
import os
# from array import array
from PIL import Image, ImageDraw
import sys
# import time
from matplotlib import pyplot as plt
# import numpy as np

import gradio as gr
from translate import Translator

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

def main(image_file):
    global cv_client
    global img_description

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Authenticate
        credential = CognitiveServicesCredentials(cog_key)
        cv_client = ComputerVisionClient(cog_endpoint, credential)

        # Analyze image
        img_description, outputfile = AnalyzeImage(image_file)

        # Generate thumbnail
        GetThumbnail(image_file)

        return img_description, outputfile

    except Exception as ex:
        print(ex)

def AnalyzeImage(image_file):
    print('Analyzing', image_file)

    # Specify features to be retrieved
    features = [
        VisualFeatureTypes.description,
        VisualFeatureTypes.tags,
        VisualFeatureTypes.categories,
        VisualFeatureTypes.brands,
        VisualFeatureTypes.objects,
        VisualFeatureTypes.adult
    ]

    with open(image_file, mode="rb") as image_data:
        analysis = cv_client.analyze_image_in_stream(image_data , features)

    for caption in analysis.description.captions:
        print("Description: '{}' (confidence: {:.2f}%)".format(caption.text, caption.confidence * 100))
        img_description = caption.text
        img_description = Translator(from_lang="en", to_lang="es").translate(img_description)

    if len(analysis.tags) > 0:
        print("Tags: ")
        for tag in analysis.tags:
            print(" -'{}' (confidence: {:.2f}%)".format(tag.name, tag.confidence * 100))

    if len(analysis.categories) > 0:
        print("Categories:")
        landmarks = []

        for category in analysis.categories:
            print(" -'{}' (confidence: {:.2f}%)".format(category.name, category.score * 100))

            if category.detail.landmarks:
                for landmark in category.detail.landmarks:
                    if landmark not in landmarks:
                        landmarks.append(landmark)

        if len(landmarks) > 0:
            print("Landmarks: ")
            for landmark in landmarks:
                print(" - '{}' (confidence: {:.2f})".format(landmark.name, landmark.confidence * 100))


    # Get objects in the image
    if len(analysis.objects) > 0:
        print("Objects in image:")

        # Prepare image for drawing
        fig = plt.figure(figsize=(8, 8))
        plt.axis('off')
        image = Image.open(image_file)
        draw = ImageDraw.Draw(image)
        color = 'cyan'
        for detected_object in analysis.objects:
            # Print object name
            print(" -{} (confidence: {:.2f}%)".format(detected_object.object_property, detected_object.confidence * 100))

            # Draw object bounding box
            r = detected_object.rectangle
            bounding_box = ((r.x, r.y), (r.x + r.w, r.y + r.h))
            draw.rectangle(bounding_box, outline=color, width=3)
            plt.annotate(detected_object.object_property,(r.x, r.y), backgroundcolor=color)

        # Save annotated image
        plt.imshow(image)
        outputfile = 'images/objects.jpg'
        fig.savefig(outputfile)
        print('Results saved in', outputfile)


        return img_description, outputfile


def GetThumbnail(image_file):
    print('Generating thumbnail')

    with open(image_file, 'rb') as image_data:
        thumbnail_stream = cv_client.generate_thumbnail_in_stream(100, 100, image_data, True)

    thumbnail_file_name = "images/thumbnail.png"
    with open(thumbnail_file_name, 'wb') as thumbnail_file:
        for chunk in thumbnail_stream:
            thumbnail_file.write(chunk)




app = gr.Interface(
    fn=main,
    inputs=gr.Image(type="filepath"),
    outputs=[
        gr.Textbox(label="Descripción"),
        gr.Image(type="filepath")
    ],
    title="Análisis de Imagen con Azure",
    description="Carga una imagen y obtén una descripción usando Azure Computer Vision."
)

app.launch()
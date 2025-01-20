from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from django.http import JsonResponse
from django.shortcuts import render
from .utils import get_class
from io import BytesIO
import matplotlib.pyplot as plt
import base64, urllib
import numpy as np
import tempfile
import io
import os

# Create your views here.

def main_page(request):
    return render(request, 'index.html')

def PredictImage(request):
    if request.method == 'POST':
        if 'image_file' in request.FILES:
            uploaded_image = request.FILES['image_file']
            uploaded_model_opt_cnn = request.FILES['model_file']
            if uploaded_model_opt_cnn.name != '':
                file_data = uploaded_model_opt_cnn.read()
                # Create a temporary file to save the uploaded data
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(file_data)
                    temp_file_path = temp_file.name

                model = load_model(temp_file_path)
                temp_file.close()
                os.unlink(temp_file_path)
                if model:
                    predicted_image = scale_aware_cnn(model, uploaded_image)
                    response_data = {
                    "message": "Model uploaded and processed successfully",
                    "prediction": predicted_image
                    }
                    return JsonResponse(response_data)
                    # return render(request, 'prediction.html', {'prediction': predicted_image})
                else:
                    return JsonResponse({'message': 'No Model provided'}, status=400)
            else:
                return JsonResponse({'message': 'No Model Uploaded'}, status=400)

        else:
            return JsonResponse({'message': 'No image provided'}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=400)

def scale_aware_cnn(model, uploaded_image):
    image_height = 128
    image_width = 128

    image_buffer = io.BytesIO(uploaded_image.read())
    image = load_img(image_buffer, target_size=(image_width, image_height))
    test_image = img_to_array(image) / 255.0
    test_image = np.expand_dims(test_image, axis=0)
    predictions = model.predict(test_image)
    predicted_class = int(np.argmax(predictions))
    class_labels = get_class();

    output = class_labels[predicted_class]
    return output


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    img_png = buffer.getvalue()
    graph = base64.b64encode(img_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

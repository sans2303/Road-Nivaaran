from flask import Flask, render_template, request
from ultralytics import YOLO
from PIL import Image
import requests
#from fpdf import FPDF
#import base64

app = Flask(__name__)

def predict_defect(image_path):
    # Load the YOLOv5 model
    model = YOLO('./weights/best.pt')
    
    

    # Read and resize the input image using Pillow (PIL)
    with Image.open(image_path) as img:
        img = img.resize((255, 255))
    
    # Convert image data to a list
    
    
    # Perform prediction on the image
    results = model(img, show=True)

    # Extract relevant information from the prediction
    names_dict = results[0].names
    probs = results[0].probs.data.tolist()
    prediction = names_dict[probs.index(max(probs))]

    return prediction



@app.route('/')
def home():
    return render_template('index.html', prediction=None)





    

@app.route('/predict', methods=['POST'])
def predict():
    # Get the image file from the request
    file = request.files['image']

    # Save the file temporarily (optional)
    image_path = 'temp_image.jpg'
    file.save(image_path)
    # Pass the image to the YOLOv8 model for prediction
    prediction = predict_defect(image_path)

    #Generating Pdf according to prediction 
    #pdf_content = base64.b64encode( generate_pdf(image_path," Adharvadi Jail Road", prediction)).decode('utf-8')


    # Render the template with the prediction result
    return render_template('index.html', prediction=prediction)


    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    

if __name__ == '__main__':
    app.run(debug=True)

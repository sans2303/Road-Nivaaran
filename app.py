# app_with_yolo.py
from flask import Flask, render_template, request, send_file, Response
from ultralytics import YOLO
from PIL import Image
import requests
import webbrowser
from flask_ngrok import run_with_ngrok
from fpdf import FPDF
import base64
import io

app = Flask(__name__)
#run_with_ngrok(app)
def predict_defect(image_path):
    # Load the YOLOv5 model
    model = YOLO(r'Myproject-main\Myproject-main\YoloModel-20240306T045132Z-001\YoloModel\runs\classify\train3\weights\best.pt')

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


def generate_pdf(image_path, location,complain):
 
  # Create a new FPDF object
  pdf = FPDF()

  # Add a page
  pdf.add_page()

  # Set the font and font size
  pdf.set_font("Arial", size=12)

  # Create the subject line (centered)
  if complain=="garbage":
    subject = "Subject: Complaint Regarding Roadside Garbage"
    body_text = f"""Dear [Recipient Name],

  I am writing to express my concern about the excessive amount of garbage accumulating on the roadside near {location}. This has become a serious issue, not only detracting from the aesthetics of the neighborhood but also posing potential health hazards.

  The overflowing garbage attracts pests and creates an unpleasant odor. It is also a safety concern, as it can obstruct pedestrians and cyclists.

  I kindly request you to take immediate action to address this problem. This could involve scheduling more frequent garbage collection or implementing stricter waste disposal regulations in the area.

  Thank you for your time and attention to this matter.

  Sincerely,

  [Your Name]"""
    
  elif complain=="pothole":
    subject = "Subject: Complaining about Potholes on Road"
    body_text = """Dear [Recipient Name],

I am writing to express my concern about the numerous potholes that have developed on the road near [Location description]. These potholes pose a significant danger to motorists, cyclists, and pedestrians.

Traveling on a road riddled with potholes can damage vehicles, cause accidents, and lead to injuries. The uneven surface can be particularly hazardous for two-wheeled vehicles and can also create difficulties for pedestrians, especially those with mobility limitations.

I urge you to take immediate action to address this issue. This could involve scheduling repairs to fill in the potholes as soon as possible.

Thank you for your time and attention to this matter.

Sincerely,

[Your Name]"""
 
  pdf.cell(pdf.w, 10, txt=subject, align="C")

  # Add a line break
  pdf.ln(10)

  pdf.multi_cell(pdf.w - 20, 5, txt=body_text)

  # Get the current Y position (where the cursor is) - for optional image
  y_pos = pdf.get_y()

  # Calculate the image size based on available space (optional)
  if image_path:
      image_width = pdf.w - 40  # Leave some margin on both sides
      image_height = pdf.h - y_pos - 20  # Calculate available height, leaving margin

  # Add the image (adjust path and potentially resize as needed)
  if image_path:
      pdf.image(image_path, x=20, y=y_pos, w=image_width, h=image_height)


 # Output the PDF as a byte stream
  pdf_output = pdf.output(dest='S')
  pdf_bytes = io.BytesIO(pdf_output.encode('latin-1')).read()
   

  return pdf_bytes


@app.route('/predict', methods=['POST'])
def predict():
    # Get the image file from the request
    file = request.files['image']

    # Save the file temporarily (optional)
    image_path = 'temp_image.jpg'
    file.save(image_path)
    # Pass the image to the YOLOv5 model for prediction
    prediction = predict_defect(image_path)
    
    
    #Generating Pdf according to prediction 
    
    pdf_content = base64.b64encode(generate_pdf(image_path, " Adharvadi Jail Road", prediction))

    # Render the template with the prediction result
    return render_template('index.html', prediction=prediction,pdf_content=pdf_content)

    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    


if __name__ == '__main__':
    app.run(debug=True)
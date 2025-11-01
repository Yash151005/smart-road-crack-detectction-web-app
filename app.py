from flask import Flask, render_template, request, send_file, session
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from PIL import Image
import io
from src.image_processing import detect_cracks, calculate_crack_percentage

app = Flask(__name__)
app.secret_key = 'crack_detection_secret_key'  # For session management

UPLOAD_FOLDER = "data/upload/"
RESULT_FOLDER = "static/results/"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("image")
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            result_filename = "processed_" + file.filename
            result_path = os.path.join(RESULT_FOLDER, result_filename)

            mask_path = detect_cracks(file_path, result_path)
            crack_percentage = calculate_crack_percentage(mask_path)

            # Store analysis data in session for PDF generation
            session['analysis_data'] = {
                'original_image': file_path,
                'result_image': result_path,
                'mask_image': mask_path,
                'crack_percentage': crack_percentage,
                'filename': file.filename,
                'timestamp': datetime.now().isoformat()
            }

            return render_template(
                "result.html",
                result_image="results/" + result_filename,
                mask_image="results/" + os.path.basename(mask_path),
                crack_percentage=crack_percentage
            )
    return render_template("index.html")

@app.route("/download_pdf")
def download_pdf():
    """Generate and download PDF report with analysis results"""
    if 'analysis_data' not in session:
        return "No analysis data found. Please run an analysis first.", 400
    
    data = session['analysis_data']
    
    # Create PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Title
    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, height - 50, "Road Crack Detection Report")
    
    # Analysis details
    p.setFont("Helvetica", 12)
    y_position = height - 100
    
    # Add timestamp and filename
    p.drawString(50, y_position, f"Analysis Date: {datetime.fromisoformat(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
    y_position -= 20
    p.drawString(50, y_position, f"Image File: {data['filename']}")
    y_position -= 20
    p.drawString(50, y_position, f"Crack Coverage: {data['crack_percentage']:.2f}%")
    y_position -= 40
    
    # Add images to PDF
    try:
        # Original image
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y_position, "Original Image:")
        y_position -= 20
        
        if os.path.exists(data['original_image']):
            img = Image.open(data['original_image'])
            img.thumbnail((400, 300), Image.Resampling.LANCZOS)
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            p.drawImage(ImageReader(img_buffer), 50, y_position - 300, width=400, height=300)
            y_position -= 320
        
        # Processed image
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y_position, "Processed Image (Crack Detection):")
        y_position -= 20
        
        if os.path.exists(data['result_image']):
            img = Image.open(data['result_image'])
            img.thumbnail((400, 300), Image.Resampling.LANCZOS)
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            p.drawImage(ImageReader(img_buffer), 50, y_position - 300, width=400, height=300)
        
    except Exception as e:
        p.drawString(50, y_position, f"Error loading images: {str(e)}")
    
    # Analysis summary
    p.showPage()  # New page
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, height - 50, "Analysis Summary")
    
    p.setFont("Helvetica", 12)
    y_position = height - 100
    
    summary_data = [
        f"• Crack Coverage Percentage: {data['crack_percentage']:.2f}%",
        f"• Risk Level: {'High' if data['crack_percentage'] > 15 else 'Medium' if data['crack_percentage'] > 5 else 'Low'}",
        f"• Recommendation: {'Immediate repair needed' if data['crack_percentage'] > 15 else 'Monitor and plan maintenance' if data['crack_percentage'] > 5 else 'Good condition'}",
        f"• Analysis Method: Computer Vision with Edge Detection",
        f"• Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ]
    
    for line in summary_data:
        p.drawString(50, y_position, line)
        y_position -= 25
    
    p.save()
    
    buffer.seek(0)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"crack_detection_report_{timestamp}.pdf"
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )

if __name__ == "__main__":
    app.run(debug=True)

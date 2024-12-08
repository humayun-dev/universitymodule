from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import csv

app = Flask(__name__)

# Load university data from CSV file
universities_data = []
with open('data/universities_data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        universities_data.append(row)

# Define a function to generate the PDF report
def generate_pdf_report(universities):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt="University Report", ln=True, align='C')
    pdf.ln(10)
    for university in universities:
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=university['University Name'], ln=True, align='L')
        pdf.cell(200, 10, txt=f"City: {university['City']}, State: {university['State']}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Career Path: {university['Career Path']}, Degree Level: {university['Degree Level']}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Courses Offered: {university['Courses Offered']}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Fees: {university['Fees']}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Ranking: {university['Ranking']}", ln=True, align='L')
        pdf.ln(10)
    return pdf

# Define the Flask route for the homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        career_path = request.form['career_path']
        degree_level = request.form['degree_level']
        universities = [university for university in universities_data if university['Career Path'] == career_path and university['Degree Level'] == degree_level]
        pdf_report = generate_pdf_report(universities)
        pdf_report.output("university_report.pdf")
        return send_file("university_report.pdf", as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
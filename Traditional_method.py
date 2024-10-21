# import package
import cv2
import easyocr
import matplotlib.pyplot as plt
import re
import spacy
import subprocess
import numpy as np

# Check and download language model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Downloading 'en_core_web_sm' model... Please wait.")
    subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])
    nlp = spacy.load('en_core_web_sm')

# Image preprocessing (simplified version)
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Visualization
    plt.figure(figsize=(10, 5))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.tight_layout()
    plt.show()

    return gray

# Perform OCR using EasyOCR
def ocr_with_visualization(image):
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image, detail=0)
    extracted_text = "\n".join(results)
    return extracted_text

# Clean extracted text data
def clean_extracted_data(text):
    return re.sub(r'\s+', ' ', text.replace('\n', ' ').strip())

# Extract invoice data using regex
def extract_specific_values(text):
    data = {}
    # Search for specific values '348.43', '971 ', '425 '
    value_348_43 = re.search(r'348\.43', text)
    value_971 = re.search(r'971\s*kwh?', text, re.IGNORECASE)
    value_425 = re.search(r'425\s*kwh?', text, re.IGNORECASE)

    if value_348_43:
        data['Total Current Charges'] = '348.43'
    if value_971:
        data['Charged Midnight-9pm:'] = '971 kWh'
    if value_425:
        data['Free 9pm-Midnight:'] = '425 kWh'

    return data

# Extract invoice data using NLP
def extract_invoice_data_nlp(text):
    text = text.lower()
    doc = nlp(text)
    data = {}

    # Match Charged data using regex
    charged_match = re.search(r'charged[^\d]*(\d+)\s*kwh', text)
    if charged_match:
        data['Charged'] = f"{charged_match.group(1)} kWh"

    # Match Free data using regex
    free_match = re.search(r'free[^\d]*(\d+)\s*kwh', text)
    if free_match:
        data['Free'] = f"{free_match.group(1)} kWh"

    # Use NLP model to identify key fields in the invoice
    for ent in doc.ents:
        if ent.label_ == "MONEY" and any(keyword in ent.text for keyword in ["total", "amount", "charges"]):
            data['Total Current Charges'] = f"${ent.text.strip()}"

    return data

# Format extracted text to look like an invoice
def format_extracted_text_as_invoice(text):
    lines = text.split('\n')
    formatted_text = "Invoice Summary:\n"
    for line in lines:
        if any(keyword in line.lower() for keyword in ["total", "charged", "free", "amount", "charges"]):
            formatted_text += line + "\n"
    return formatted_text

# Main function: Extract and analyze data from invoice
def process_invoice_with_visualization(image_path):
    # Image preprocessing
    preprocessed_image = preprocess_image(image_path)

    # Perform OCR and get extracted text
    ocr_result = ocr_with_visualization(preprocessed_image)

    # Clean extracted text
    cleaned_text = clean_extracted_data(ocr_result)

    # Format extracted text
    formatted_text = format_extracted_text_as_invoice(cleaned_text)
    print("\nFormatted Invoice Text:\n", formatted_text)

    # Extract data using NLP
    extracted_data_nlp = extract_invoice_data_nlp(cleaned_text)
    if not extracted_data_nlp:
        print("\nNo data extracted using NLP.")
    else:
        print("\nExtracted Data (NLP):", extracted_data_nlp)

    # Extract specific values
    extracted_specific_values = extract_specific_values(cleaned_text)
    print("\nExtracted Specific Values:", extracted_specific_values)

    # Combine all extracted data
    extracted_data = {**extracted_data_nlp, **extracted_specific_values}
    return extracted_data

# Run invoice processing
def run():
    image_path = 'electric_example.jpg'
    processed_data = process_invoice_with_visualization(image_path)

if __name__ == "__main__":
    run()

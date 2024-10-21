
# OCR Invoice Extraction Project

This project utilizes multiple Optical Character Recognition (OCR) techniques for extracting text and relevant information from invoice images. It includes different models and approaches to ensure robust text extraction, preprocessing, and post-processing for structured output.

## Files

### 1. Python Scripts

- **PaddleOCR.py**:  
  Implements OCR using the PaddleOCR library for English and Chinese text recognition. The script includes image preprocessing and visualizes the OCR results on the original image.
  
- **Traditional_method.py**:  
  Uses EasyOCR combined with Spacy for NLP-based extraction of key invoice data. The script preprocesses images, performs OCR, and uses regular expressions and NLP for refining the extracted text.
  
- **TrOCR.py**:  
  Leverages Microsoft TrOCR model to extract text from invoice images. This script utilizes transformer models for OCR, handling both printed and handwritten text.
  
- **Extract_data_PDF.py**:  
  Extracts tables and key data from PDF documents, such as emissions reports, and saves them as Excel files for further analysis.

### 2. Sample Images and Data

- **clear_invoice.png**:  
  An invoice image used as an example for OCR testing.

- **Process_picture.png**:  
  An image showing preprocessing techniques, including cropping and denoising, applied to invoice images.

- **electric_example.jpg**:  
  Another sample invoice used to evaluate different OCR models.

- **Measuring-Emissions-Guidance_EmissionFactors_Summary_2023_ME1781.pdf**:  
  A PDF file containing emission factor data. This file is used for testing the table extraction capabilities of the `Extract_data_PDF.py` script.

## How to Use

### Prerequisites

Make sure you have the following Python libraries installed:

```bash
pip install paddleocr easyocr opencv-python spacy transformers pillow pdfplumber pandas matplotlib
```

### Running the Scripts

To run the OCR extraction or PDF processing, use the following commands:

1. **PaddleOCR.py**:
   ```bash
   python PaddleOCR.py
   ```

2. **Traditional_method.py**:
   ```bash
   python Traditional_method.py
   ```

3. **TrOCR.py**:
   ```bash
   python TrOCR.py
   ```

4. **Extract_data_PDF.py**:
   ```bash
   python Extract_data_PDF.py
   ```

## Acknowledgments

The project makes use of the following libraries:

- PaddleOCR
- EasyOCR
- OpenCV
- Spacy
- Transformers (HuggingFace)
- PIL (Pillow)
- pdfplumber
- pandas
- matplotlib

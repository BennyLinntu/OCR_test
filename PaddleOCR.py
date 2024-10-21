from paddleocr import PaddleOCR, draw_ocr
import cv2
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm

# List all available font paths
def show_ttf():
    for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
        print(font)# show ttf

# Initialize the OCR model for English and Chinese recognition
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # 'en' for English, you can switch to other languages

# Read the image
img_path = 'clear_invoice.png'#'electric_example.jpg'

# Perform text recognition
result = ocr.ocr(img_path, cls=True)

# Print recognized text
for line in result:
    print(line)

# Load and display the image with recognized text
image = cv2.imread(img_path)
boxes = [res[0] for res in result[0]]  # Text regions
txts = [res[1][0] for res in result[0]]  # Recognized text
scores = [res[1][1] for res in result[0]]  # Confidence scores

# Visualize the results
image = draw_ocr(image, boxes, txts, scores, font_path = "C:/Windows/Fonts/arial.ttf"
)
plt.imshow(image)
plt.show()


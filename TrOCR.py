from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

# Load TrOCR processor and model
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

# Load local image
image_path = "electric_example.jpg"
image = Image.open(image_path).convert("RGB")

# Process image
pixel_values = processor(image, return_tensors="pt").pixel_values

# Generate text with max_length parameter to generate longer text
generated_ids = model.generate(pixel_values, max_length=100)

# Decode generated text
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

# Print generated text
print('==================')
print(generated_text)

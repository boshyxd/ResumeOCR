import os
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define input and output directories
input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ResumePng')
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ResumeDump')

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def preprocess_image(image):
    """Apply minimal preprocessing for clean documents"""
    # Convert to grayscale
    image = image.convert('L')
    
    # Slightly enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.2)
    
    return image

def process_resumes():
    try:
        # Get list of PNG files in input directory
        png_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.png')]
        
        if not png_files:
            print("No PNG files found in the input directory.")
            return

        # Process each PNG file
        for png_file in png_files:
            try:
                # Construct full file paths
                input_path = os.path.join(input_dir, png_file)
                output_path = os.path.join(output_dir, os.path.splitext(png_file)[0] + '.txt')
                
                # Load and preprocess image
                print(f"Processing: {png_file}")
                image = Image.open(input_path)
                processed_image = preprocess_image(image)
                
                # Perform OCR with settings optimized for clean documents
                custom_config = r'--oem 3 --psm 3 -l eng'
                text = pytesseract.image_to_string(processed_image, config=custom_config)
                
                # Basic post-processing of OCR text
                text = text.replace('|', 'I')  # Common OCR mistake
                text = text.replace('0', 'O')  # Common OCR mistake
                
                # Save result to text file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                    
                print(f"Saved: {output_path}")
                
            except Exception as e:
                print(f"Error processing {png_file}: {str(e)}")
                
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    process_resumes()

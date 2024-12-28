import os
import pytesseract
from PIL import Image

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define input and output directories
input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ResumePng')
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ResumeDump')

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

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
                
                # Perform OCR
                print(f"Processing: {png_file}")
                text = pytesseract.image_to_string(Image.open(input_path))
                
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
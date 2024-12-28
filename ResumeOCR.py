import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define input and output directories
input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ResumePng')
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ResumeDump')

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def process_resumes():
    try:
        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
        )

        # Get list of image files in input directory
        image_files = [f for f in os.listdir(input_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            print("No image files found in the input directory.")
            return

        # Initialize combined text
        combined_text = ""

        # Process each image file
        for image_file in image_files:
            try:
                # Construct full file paths
                input_path = os.path.join(input_dir, image_file)
                
                # Load image
                print(f"Processing: {image_file}")
                image = Image.open(input_path)
                
                # Resize image if too large
                max_size = (1024, 1024)
                if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                    image.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Create chat session
                chat_session = model.start_chat(history=[])
                
                # Send image for OCR
                try:
                    response = chat_session.send_message(
                        [image, "Extract all text from this resume image with perfect accuracy. Return only the extracted text:"]
                    )
                except Exception as e:
                    print(f"API Error: {str(e)}")
                    continue
                
                # Add to combined text
                combined_text += f"\n\n=== {image_file} ===\n{response.text}"
                
            except Exception as e:
                print(f"Error processing {png_file}: {str(e)}")
                
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Save combined results
    if combined_text:
        output_path = os.path.join(output_dir, 'combined_results.txt')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(combined_text.strip())
        print(f"\nSaved combined results to: {output_path}")

if __name__ == "__main__":
    process_resumes()

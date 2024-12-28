import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ResumePng")
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ResumeDump")

os.makedirs(output_dir, exist_ok=True)


def process_resumes():
    try:
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

        image_files = [
            f
            for f in os.listdir(input_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        if not image_files:
            print("No image files found in the input directory.")
            return

        combined_text = ""

        batch_size = 10
        for i in range(0, len(image_files), batch_size):
            batch = image_files[i : i + batch_size]
            print(
                f"Processing batch {i//batch_size + 1} of {len(image_files)//batch_size + 1}"
            )

            images = []
            for image_file in batch:
                try:
                    input_path = os.path.join(input_dir, image_file)
                    image = Image.open(input_path)

                    max_size = (1024, 1024)
                    if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                        image.thumbnail(max_size, Image.Resampling.LANCZOS)

                    images.append((image_file, image))
                except Exception as e:
                    print(f"Error loading {image_file}: {str(e)}")
                    continue

            chat_session = model.start_chat(history=[])

            try:
                response = chat_session.send_message(
                    [
                        *[img for _, img in images],
                        "Extract all text from these resume images with perfect accuracy. Return the extracted text for each image, clearly labeled with the filename:",
                    ]
                )

                for image_file, image in images:
                    try:
                        individual_chat = model.start_chat(history=[])
                        individual_response = individual_chat.send_message(
                            [
                                image,
                                f"Extract all text from this resume image with perfect accuracy. The filename is {image_file}:",
                            ]
                        )

                        combined_text += (
                            f"\n\n=== {image_file} ===\n{individual_response.text}"
                        )

                    except Exception as e:
                        print(f"Error processing {image_file}: {str(e)}")
                        continue

            except Exception as e:
                print(f"API Error: {str(e)}")
                continue

            except Exception as e:
                print(f"Error processing {png_file}: {str(e)}")

    except Exception as e:
        print(f"Error: {str(e)}")

    if combined_text:
        output_path = os.path.join(output_dir, "combined_results.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(combined_text.strip())
        print(f"\nSaved combined results to: {output_path}")


if __name__ == "__main__":
    process_resumes()

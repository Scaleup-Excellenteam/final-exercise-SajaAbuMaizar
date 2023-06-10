import argparse
import asyncio
import os
import glob
import time
from dotenv import load_dotenv
from presentation_processor import PresentationProcessor

# Load environment variables from .env file
load_dotenv()
var = os.environ

UPLOADS_FOLDER = "uploads"
OUTPUTS_FOLDER = "outputs"


async def process_file(file_path):
    # Make a debugging print
    print(f"Processing file: {file_path}")

    # Process the file using the existing code
    presentation_processor = PresentationProcessor()
    await presentation_processor.main(file_path)

    # Save the explanation JSON in the outputs folder
    # Replace the existing code that saves the explanation JSON with the appropriate logic
    # You can use the file_path or generate a new filename as per your requirement

    # Make another debugging print
    print(f"File processed: {file_path}")


async def explainer():
    # Create the 'outputs' folder if it doesn't exist
    os.makedirs(OUTPUTS_FOLDER, exist_ok=True)

    while True:
        # Scan the uploads folder for new files
        file_paths = glob.glob(os.path.join(UPLOADS_FOLDER, "*"))

        for file_path in file_paths:
            # Get the base filename without the extension
            base_filename = os.path.splitext(os.path.basename(file_path))[0]

            # Check if the file with the same base filename (with the ending '.json') already exists in the outputs
            # folder
            output_file_path = os.path.join(OUTPUTS_FOLDER, f"{base_filename}.json")
            if os.path.exists(output_file_path):
                continue  # Skip if the output file already exists

            # Process the file
            await process_file(file_path)

        # Sleep for a few seconds before the next iteration
        time.sleep(10)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GPT-Explainer')
    parser.add_argument('presentation', type=str, help='Path to the presentation file')
    asyncio.run(explainer())

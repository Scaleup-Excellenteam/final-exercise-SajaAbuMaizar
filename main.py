import argparse
from dotenv import load_dotenv
from presentation_processor import PresentationProcessor
import asyncio

# Load environment variables from .env file
load_dotenv()


# comment
async def run_program(presentation_path):
    presentation_processor = PresentationProcessor()
    await presentation_processor.main(presentation_path)


# Run the program
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GPT-Explainer')
    parser.add_argument('presentation', type=str, help='Path to the presentation file')
    args = parser.parse_args()

    presentation_path = args.presentation

    asyncio.run(run_program(presentation_path))

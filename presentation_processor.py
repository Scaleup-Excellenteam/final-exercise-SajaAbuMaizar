import json
import os
from pptx import Presentation
import asyncio
from slide_processor import SlideProcessor


class PresentationProcessor:
    def __init__(self):
        self.slide_processor = SlideProcessor()

    async def process_presentation(self, presentation_path):
        presentation = Presentation(presentation_path)
        explanations = []

        # Create a list to hold the slide processing tasks
        slide_tasks = []

        for slide in presentation.slides:
            slide_text = ""

            for shape in slide.shapes:
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            slide_text += run.text

            slide_text = slide_text.strip()

            if slide_text:
                # Process the slide asynchronously and append the task to the list
                slide_task = self.slide_processor.process_slide(slide_text)
                slide_tasks.append(slide_task)

        # Wait for all slide processing tasks to complete
        explanations = await asyncio.gather(*slide_tasks)

        return explanations

    async def main(self, presentation_path):
        # Process the presentation
        explanations = await self.process_presentation(presentation_path)

        # Save the explanations to a JSON file
        output_file = os.path.splitext(presentation_path)[0] + '.json'
        with open(output_file, 'w') as f:
            json.dump(explanations, f, indent=4)

        print(f"Explanations saved to {output_file}")

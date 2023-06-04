import os

import openai
import asyncio

TOKEN_COUNT = 0


class SlideProcessor:
    def __init__(self):
        self.RATE_LIMIT = 3
        self.WAIT_TIME = 60
        openai.api_key = os.environ.get('OPENAI_API_KEY')

    async def process_slide(self, slide_text):
        global TOKEN_COUNT

        # Create the GPT prompt
        prompt = f"Explain the following slide:\n\n{slide_text}"

        try:
            # Check rate limit
            if TOKEN_COUNT >= self.RATE_LIMIT:
                wait_time = self.WAIT_TIME  # Wait a minute to send another request
                print(f"Rate limit exceeded. Waiting for {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                TOKEN_COUNT = 0

            # Send the prompt to the OpenAI API in a separate thread and await its result
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Update token count
            TOKEN_COUNT += 1

            # Extract the AI's reply from the response
            explanation = response.choices[0].message.content

            return explanation
        except openai.error.APIError as e:
            if 'quota' in str(e):
                return "Error processing slide: Exceeded quota. Please check your plan and billing details."
            else:
                return f"Error processing slide: {str(e)}"
        except Exception as e:
            # Handle other exceptions gracefully
            return f"Error processing slide: {str(e)}"

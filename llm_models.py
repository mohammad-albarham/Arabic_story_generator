import json
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from image_generator import get_image

class StepByStepAIResponse(BaseModel):
    title: str
    story_segments: List[str]
    image_prompts: List[str]

class GetTranslation(BaseModel):
    translated_text: List[str]


client = OpenAI(api_key="key_here")


def generate_story(k, prompt):
        """ Generate a story with k segments and initial prompt"""

        response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
            "role": "system",
            "content": f"""
            Your expertise lies in weaving captivating narratives for children, complemented by images that vividly bring each tale to life. Embark on a creative endeavor to construct a story segmented into {k} distinct chapters, each a cornerstone of an enchanting journey for a young audience.
            The input prompt will be on Arabic, but the output must be in English.

            **Task Overview**:

            1. **Story Development**:
            - Craft a narrative divided into {k} parts, with a strict 50-word limit for each.
            - Start with an engaging introduction that lays the foundation for the adventure.
            - Ensure each part naturally progresses from the previous, crafting a fluid story that escalates to an exhilarating climax.
            - Wrap up the narrative with a gratifying conclusion that ties all story threads together.
            - Keep character continuity intact across the story, with consistent presence from beginning to end.
            - You must describe the characters in details in every image prompt.
            - Use language and themes that are child-friendly, imbued with wonder, and easy to visualize.
            - The story will talk about {prompt}

            2. **Image Generation Instructions for Image Models**:
            - For every story part, create a comprehensive prompt for generating an image that encapsulates the scene's essence. Each prompt should:
                - Offer a detailed description of the scene, characters, and critical elements, providing enough specificity for the image model to create a consistent and coherent visual.
                - Request the images be in an anime style to ensure visual consistency throughout.
                - Given the image model's isolated processing, reintroduce characters, settings, and pivotal details in each prompt to maintain narrative and visual continuity.
                - Focus on visual storytelling components that enhance the story segments, steering clear of direct text inclusion in the images.

            **Key Points**:
            - Due to the image model's lack of recall, stress the need for self-contained prompts that reintroduce crucial elements each time. This strategy guarantees that, although generated independently, each image mirrors a continuous and cohesive visual story.

            Through your skill in melding textual and visual storytelling, you will breathe life into this magical tale, offering young readers a journey to remember through both prose and illustration.

            """
            },
        ],
        functions=[
            {
                "name": "get_story_segments_and_image_prompts",
                "description": "Get user answer in series of segment and image prompts",
                "parameters": StepByStepAIResponse.model_json_schema(),
            }
        ],
        function_call={"name": "get_story_segments_and_image_prompts"},  # Corrected to match the defined function name
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        output = json.loads(response.choices[0].message.function_call.arguments)

        sbs = StepByStepAIResponse(**output)

        return sbs
    
def get_Arabic_translation(story_segments):
        
        response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
            "role": "system",
            "content": 
            
            f"""
            You are an expert translator of text from English to Arabic.

            On the following, you can find the input text that you need to translate to Arabic: 
            {story_segments}

            Translate it from English to Arabic.

            """
            },
        ],
        functions=[
            {
                "name": "translate_text_from_english_to_arabic",
                "description": "Translate the text from English to Arabic.",
                "parameters": GetTranslation.model_json_schema(),
            }
        ],
        function_call={"name": "translate_text_from_english_to_arabic"},  # Corrected to match the defined function name
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        output = json.loads(response.choices[0].message.function_call.arguments)

        sbs = GetTranslation(**output)

        return sbs

def get_text_image_pairs(k, prompt):

    description = generate_story(k, prompt)

    segements_translation = get_Arabic_translation(description.story_segments)

    images_names = [get_image(itm) for itm in description.image_prompts]

    return (segements_translation.translated_text, images_names)

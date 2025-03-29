from fastapi import APIRouter, UploadFile, File, HTTPException
from ..config import client
from ..utils import encode_image

router = APIRouter(prefix="/annotation", tags=["Annotation"])

# TODO: Customize the prompt text and define output format.
prompt = """
I have uploaded an image of a UI design. Your task is to analyze the design's structure, content, and visual hierarchy. Provide a detailed critique covering:

Layout & Alignment – Analyze spacing, alignment, and organization. Point out any misaligned elements or inconsistent spacing that disrupts the design flow.
Call-to-Action (CTA) & Navigation – Review the effectiveness of CTA buttons, links, and navigation. Suggest improvements if they are unclear or misplaced.
Content & Messaging – Evaluate the clarity and effectiveness of text content. Identify vague or overly generic messaging and suggest more precise alternatives.
Visual Consistency – Identify inconsistencies in design patterns, styles, or spacing. Highlight sections that lack a uniform visual language.
User Experience (UX) Issues – Point out elements that might confuse users, disrupt navigation, or cause friction in user interaction.
Provide your feedback in a structured format with specific annotations where necessary.
"""

@router.post("/")
async def annotation(file: UploadFile = File(...)):
    """
    Analyze an image for accessibility features and issues.

    Image Upload Constraints:
    - Maximum image size: 10MiB
    - Supported image formats: JPG, JPEG, PNG
    """

    try:
        # Validate file type
        # if not file.filename.lower().endswith(".jpg" or ".jpeg" or ".png"):
        #     raise HTTPException(
        #         status_code=400,
        #         detail=f"File '{file.filename}' has an unsupported type. Only JPG, JPEG, and PNG are allowed.",
        #     )

        # Read file content
        file_content = await file.read()

        # Check file size (10MiB limit)
        if len(file_content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"File '{file.filename}' exceeds the 10MiB limit.",
            )

        # Encode image to base64
        base64_image = encode_image(file_content)

        # Prepare messages for the Grok API
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high",
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            },
        ]

        # Call the Grok API
        completion = client.chat.completions.create(
            model="grok-2-vision-latest",
            messages=messages,
            stream=False,
            temperature=0.01,
        )

        # Ensure the API response contains the expected data
        if not completion or not completion.choices or not completion.choices[0].message:
            raise HTTPException(
                status_code=500,
                detail="Invalid response from Grok API."
            )

        response_text = completion.choices[0].message.content

        return response_text

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

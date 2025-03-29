from fastapi import APIRouter, UploadFile, File, HTTPException

from ..config import client
from ..utils import encode_image

router = APIRouter(prefix="/support_docs", tags=["Support Documentation"])

# TODO: Customize the prompt text and define output format.
prompt = """
I have a sequence of UI pages designed in Figma, representing a user interface flow. Your task is to analyze the designs, including layouts, text, buttons, input fields, and any visible interactions, and generate detailed support documentation. The documentation should provide a step by step guide for users to navigate and interact with the interface to achieve a specific goal. and provide the guide for each task a user can perform.
"""


@router.post("/")
async def support_docs(file: UploadFile = File(...)):
    """
    Analyze multiple images for accessibility features and issues.

    Reminder on image model general limitations:
    - Maximum image size: 10MiB per image
    - Maximum number of images: No strict limit (depends on server resources)
    - Supported image file types: jpg/jpeg or png
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
            
        with open("documentation.md", "w", encoding="utf-8") as md_file:
                md_file.write(completion.choices[0].message.content)

        response_text = completion.choices[0].message.content

        return response_text

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )
        
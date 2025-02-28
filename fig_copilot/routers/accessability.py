from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from ..config import client
from ..utils import encode_image

router = APIRouter(prefix="/accessability", tags=["Accessability"])

# TODO: Customize the prompt text and define output format.
prompt = """
You are an expert in web accessibility (WCAG 2.1/2.2) and UI/UX design. I will provide an image of a user interface or design (e.g., a website screenshot, app screen, or graphic). Please analyze the image for accessibility features and issues, focusing on:

1. Color contrast (is text readable against backgrounds for low-vision users? Use WCAG contrast ratios, e.g., 4.5:1 for normal text, 3:1 for large text).
2. Text readability (font size, style, and clarity for users with visual impairments).
4. Navigation and interactivity (are buttons, links, and forms accessible for clear communicaion with readers?).

Provide your response in a clear, easy-to-scan structured format, using the following sections:

### Accessibility Analysis
- **Color Contrast**: Pass or List failed contrast ratios for text/background pairs.
- **Text Readability**: Pass or List failed texts in relation to font size, style, and clarity, suggesting improvements if needed.
- **Navigation/Interactivity**: Evaluate accessibility of interactive elements (e.g., buttons, forms) for clear communicaion with users.

### Recommendations
- Provide 3–5 specific, actionable recommendations to improve accessibility, prioritizing high-impact changes.

Ensure the response is concise, uses bullet points or numbered lists for clarity, and avoids jargon unless necessary. If the image lacks certain elements (e.g., no text or interactive components), note that clearly.
"""


@router.post("/")
async def accessability(file: UploadFile = File(...)):
    """
    Reminder on image model general limitations \n

    Maximum image size: 10MiB \n
    Maximum number of images: No limit \n
    Supported image file types: jpg/jpeg or png
    """
    try:
        # Validate file type (only accept images like JPG, JPEG, PNG)
        content_type = file.content_type
        if content_type not in ["image/jpg", "image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=400,
                detail="Only JPG, JPEG and PNG images are supported."
            )

        # Read the file content
        file_content = await file.read()

        # Encode the image to base64
        base64_image = encode_image(file_content)

        # Prepare the messages for the Grok API
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

        completion = client.chat.completions.create(
            model="grok-2-vision-latest",
            messages=messages,
            stream=False,
            temperature=0.01,
        )

        return completion.choices[0].message.content

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

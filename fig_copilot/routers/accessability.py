from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from ..config import client
from ..utils import encode_image

router = APIRouter(prefix="/accessability", tags=["accessability"])


@router.post("/accessability")
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
                        # TODO: Customize the prompt text and define output format.
                        "text": "What's in this image?",
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
        
        return JSONResponse(
            content={"analysis": completion.choices[0].message.content}
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

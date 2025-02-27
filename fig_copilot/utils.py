import base64


# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
#     return encoded_string


def encode_image(file_content: bytes) -> str:
    """
    Encode the binary content of an image file to a base64 string.
    """
    encoded_string = base64.b64encode(file_content).decode("utf-8")
    return encoded_string

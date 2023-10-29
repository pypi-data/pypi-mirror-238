from PIL import Image, ImageSequence
from .encoders import *
from .utils import *
import time

class ImageHandler:
    """A class to handle images for cryptography

    Attributes
    ----------
    image : Image - The parsed image

    Methods
    -------
    write(file_path): Writes the image data to a file
    file_info(): Gets the file information of the image
    encode(method, **kwargs): Encodes data into the image
    decode(method, **kwargs): Decodes data from the image
    """

    def __init__(self, file_path):
        """Initialise the ImageHandler class

        :param file_path: string - The path to the image file

        :attribute image: Image - The parsed image

        :return: object - The ImageHandler object
        """

        self.image = Image.open(file_path)

    def write(self, file_path):
        """Write to the image data to a file

        :param file_path: string - The path to the file to write to
        :return: None
        """

        self.image.save(file_path)

    def file_info(self):
        """Get the file information of the image

        :return: dict - The file information
        """

        return {"mode": self.image.mode, "size": self.image.size, "format": self.image.format, "filename": self.image.filename}

    def encode(self, method, **kwargs):
        """Encode data into the image

        :param method: string - The method to use to encode the data
        :param kwargs: dict - The arguments to pass to the method

        :return: None

        :raises: NotImplementedError - If the method is not implemented

        The method allows selecting the method to use to encode the data, and
        it accepts keyword arguments to pass to the method. The keywords are:
        - data: The data to encode
        - key: The key to use to encode the data
        """
        match method:
            case "rail_fence_cipher":
                info = self.file_info()
                x = get_rail_fence_pixels(info["size"][0], info["size"][1], kwargs["key"])
                encoded_data = encode_rail_fence_cipher(kwargs["data"], kwargs["key"])
                for (idx, pixel) in enumerate(x):
                    new_pixel = encode_data_to_pixel(self.image.getpixel(pixel), encoded_data[idx])
                    self.image.putpixel(i, new_pixel)
                
            case "random_spacing":
                info = self.file_info()
                enumerator = get_random_spacing_pixels(info["size"][0], info["size"][1], kwargs["key"])
                data = kwargs["data"]
                for (idx, pixel) in enumerate(enumerator):
                    new_pixel = encode_data_to_pixel(self.image.getpixel(pixel), data[idx])
                    self.image.putpixel(pixel, new_pixel)
                


            case _:
                raise NotImplementedError(f"Method {method} not implemented")
                    

    def decode(self, method, **kwargs):
        """Decode data from the image

        :param method: string - The method to use to decode the data
        :param kwargs: dict - The arguments to pass to the method

        :return: string - The decoded data

        :raises: NotImplementedError - If the method is not implemented

        The method allows selecting the method to use to decode the data, and
        it accepts keyword arguments to pass to the method. The keywords are:
        - key: The key to use to decode the data
        """

        match method:
            case _:
                raise NotImplementedError(f"Method {method} not implemented")


image_handler = ImageHandler("img/d.png")
#image_handler.encode("lsb")
#image_handler.write("img/d.png")
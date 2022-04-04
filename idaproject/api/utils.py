import os, urllib, random, string, sys
import PIL.Image as PIL_Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile



def get_picture_name_from_url(url: str) -> str:
    """
    Downloads an image by given url using GET-method.
    """

    a = urllib.parse.urlparse(url)
    return os.path.basename(a.path)


def remove_from_tuple(my_tuple: tuple, *args) -> tuple:
    """
    Removes all given elements from tuple.
    """

    my_new_tuple = (x for x in my_tuple if x not in args)
    return my_new_tuple


def resize_image(filepath: str, size: tuple) -> tuple:
    """
    Resizes an image stored by given filepath to new size.
    """

    resized_image = PIL_Image.open(filepath).resize(size)
    resized_filepath = generate_unique_name(filepath, 5)
    bytesio_obj = BytesIO(resized_image.tobytes())
    resized_image.save(bytesio_obj, format="JPEG")

    image_file = InMemoryUploadedFile(
        bytesio_obj,
        None,
        os.path.basename(resized_filepath),
        "image/jpeg",
        sys.getsizeof(bytesio_obj),
        None,
    )
    return (
        image_file,
        resized_filepath,
    )


def generate_unique_name(init_name: str, length: int) -> str:
    """
    Generates the unique name by adding random ASCII characters to the end of picture name.
    """

    random_string = ""
    init_name_list = [init_name]

    for i in range(abs(int(length))):
        random_string += random.choice(string.ascii_letters)

    if "." in init_name:
        init_name_list = init_name.split(".")
        unique_name = (
            init_name_list[0] + "_" + random_string + "." + init_name_list[1]
        )
    else:
        unique_name = init_name_list[0] + "_" + random_string

    return unique_name

from PIL import Image


def processor_iamge(img_path, width_size: int = 300, height_size: int = 300):
    img = Image.open(img_path)
    max_size = (width_size, height_size)
    img.thumbnail(max_size, Image.LANCZOS)
    img.save(img_path)

import datetime
import requests
from PIL import Image
from django.core.files.base import ContentFile
from .models import Image as ImageModel
from io import BytesIO


class PillowImageFormatter:

    def __init__(self, image):
        self.image = Image.open(image)
        self.initial_width, self.initial_height = self.image.size[0], self.image.size[1]

    def get_image(self):
        return self.image

    def get_initial_size(self):
        return self.initial_width, self.initial_height

    def set_size_and_return(self, w: int, h: int):
        new_image = self.image.resize((w, h))
        return new_image


class ImageObjectsCreator:
    """Create records in db with image from request and new resized image"""

    def __init__(self, form):
        self.data = form.cleaned_data

    def __need_to_download_from_link(self):
        if self.data.get('url'):
            return True
        else:
            return False

    def __get_image_from_link(self):
        link = self.data.get('url')
        image = requests.get(link).content
        return image

    def __pillow_object(self):
        if self.__need_to_download_from_link():
            pillow_object = PillowImageFormatter(BytesIO(self.__get_image_from_link()))
        else:
            pillow_object = PillowImageFormatter(self.data.get('picture'))
        return pillow_object

    def __image_file(self):
        image_file = self.__pillow_object().get_image()
        return image_file

    def __save_image_from_request(self):
        image_from_form = ImageModel()
        if not self.__need_to_download_from_link():
            image_from_form.picture = self.data.get('picture')
            image_from_form.name = image_from_form.picture.name
        else:
            image_from_form.url = self.data.get('url')

            file_name = str(datetime.datetime.now()).replace(':', '-').replace(' ', '')+'.jpg'
            file = ContentFile(self.__get_image_from_link())
            image_from_form.picture.save(file_name, file, save=False)

            image_from_form.name = image_from_form.picture.name

        image_from_form.width, image_from_form.height = self.__pillow_object().get_initial_size()
        image_from_form.save()

    def __resize_and_save_new_image(self):
        new_image = ImageModel()
        parent = ImageModel.objects.latest('id')
        file_name = str(datetime.datetime.now()).replace(':', '-').replace(' ', '')+'.png'
        new_image.name = file_name
        new_image.url = parent.url
        new_image.parent_picture = parent.id
        new_image.width = self.data.get('width')
        new_image.height = self.data.get('height')

        pillow_obj = PillowImageFormatter(parent.picture)
        resized_img = pillow_obj.set_size_and_return(w=new_image.width, h=new_image.height)
        bytes = BytesIO()
        resized_img.save(bytes, format='PNG')
        file = ContentFile(bytes.getvalue())
        new_image.picture.save(file_name, file, save=True)
        new_image.save()

    def run(self):
        self.__save_image_from_request()
        self.__resize_and_save_new_image()


class ImageAPICreator:
    """Download image from link and create new object"""
    def __init__(self, url):
        self.url = url
        self.image = None

    def __download_image(self):
        if self.image is None:
            self.image = requests.get(self.url).content
        return self.image

    def __pillow_object(self):
        pillow_object = PillowImageFormatter(BytesIO(self.__download_image()))
        return pillow_object

    def run(self):
        new_image = ImageModel()
        new_image.url = self.url
        pillow_obj = self.__pillow_object()
        new_image.width, new_image.height = pillow_obj.get_initial_size()
        bytes = BytesIO()
        pillow_obj.get_image().save(bytes, format='PNG')
        file = ContentFile(bytes.getvalue())
        file_name = str(datetime.datetime.now()).replace(':', '-').replace(' ', '') + '.png'
        new_image.picture.save(file_name, file, save=True)
        new_image.name = new_image.picture.name
        new_image.save()


class ImageAPIResizer:
    """Create and save resized image"""
    def __init__(self, parent, size):
        self.parent = parent
        self.image = parent.picture
        self.size = size

    def __resized_image(self):
        image = PillowImageFormatter(self.image)
        resized_img = image.set_size_and_return(*self.size)
        return resized_img

    def run(self):
        new_image = ImageModel()
        new_image.url = self.parent.url
        new_image.parent_picture = self.parent.id
        resized_image = self.__resized_image()
        new_image.width, new_image.height = self.size
        file_name = str(datetime.datetime.now()).replace(':', '-').replace(' ', '') + '.png'
        bytes = BytesIO()
        resized_image.save(bytes, format='PNG')
        file = ContentFile(bytes.getvalue())
        new_image.picture.save(file_name, file, save=True)
        new_image.name = new_image.picture.name
        new_image.save()

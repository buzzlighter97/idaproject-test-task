from pprint import pprint
from rest_framework import viewsets, response, status
from rest_framework.decorators import action
from django.forms.models import model_to_dict
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
from django.conf import settings
from .models import Image
from .serializers import ImageSerializer, ImageSerializerNoFile
from io import StringIO
from PIL import Image as PIL_Image
import os, requests
from .utils import *

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def list(self, request):
        images_queryset = Image.objects.all()
        serializer = ImageSerializerNoFile(images_queryset, many=True)
        
        return response.Response(
                serializer.data, status=status.HTTP_200_OK
            )

    def create(self, request):
        serializer = ImageSerializer(data=request.data)
        if request.data.get("file") and request.data.get("url"):
            return response.Response(
                data={
                    "error_message": "Can't decide which image to download"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            image_instance = serializer.save()

            if image_instance.url:
                response_content = ContentFile(
                    requests.get(image_instance.url).content
                )
                image_instance.file.save(
                    os.path.basename(image_instance.url), response_content
                )
                image_instance.picture = (
                    settings.BASE_DOMAIN_NAME + image_instance.file.url
                )
            elif not (image_instance.url or image_instance.file):
                return response.Response(
                    data={
                        "error_message": "Missing image or url to download image"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            image_instance.save()

            image_instance.picture = (
                settings.BASE_DOMAIN_NAME + image_instance.file.url
            )
            image_instance.name = image_instance.file.name
            image_instance.width = image_instance.file.width
            image_instance.height = image_instance.file.height

            image_instance.save()

            serializer = ImageSerializerNoFile(image_instance)
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED
            )

        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request, pk):
        try:
            image_obj = Image.objects.get(pk=pk)
            serializer = ImageSerializerNoFile(image_obj)
                       
            return response.Response(
                serializer.data, status=status.HTTP_200_OK
            )
        except Image.DoesNotExist:
            return response.Response(
                data={'error_message:': 'Image with this id doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        try:
            image_obj = Image.objects.get(id=pk)
            image_obj.file.delete()
            return super().destroy(request, pk)
        except Image.DoesNotExist:
            return response.Response(
                data={'error_message:': 'Image with this id doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=["post"], detail=True, url_path="resize")
    def resize(self, request, pk):
        try:
            image_instance = Image.objects.get(id=pk)
            image_instance.pk = None
            image_instance._state.adding = True

            width = image_instance.width
            height = image_instance.height

            if not (request.POST.get("width") or request.POST.get("height")):
                return response.Response(
                    data={"error_message": "Missing size parameters"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if request.POST.get("width"):
                width = request.POST.get("width")
                image_instance.width = width
            if request.POST.get("height"):
                height = request.POST.get("height")
                image_instance.height = height

            image_instance.parent_picture = pk

            if image_instance.url:
                image_instance.url = None

            resized_image_tuple = resize_image(
                os.path.join(settings.MEDIA_ROOT, image_instance.file.name),
                (
                    int(width),
                    int(height),
                ),
            )
            image_instance.file.save(
                resized_image_tuple[1], resized_image_tuple[0]
            )
            image_instance.save()

            image_instance.name = image_instance.file.name
            image_instance.picture = (
                settings.BASE_DOMAIN_NAME + image_instance.file.url
            )

            image_instance.save()

            serializer = ImageSerializerNoFile(image_instance)

            return response.Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
        except Image.DoesNotExist:
            return response.Response(
                data={'error_message:': 'Image with this id doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST
            )
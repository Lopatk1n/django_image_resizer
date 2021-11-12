from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .serializers import ImageSerializer, ImageURLSerializer, ImageSizeSerializer
from .utils import *


def index(request):
    if request.method == 'POST':
        form = ImageLoadForm(request.POST, request.FILES)
        if form.is_valid():
            ImageObjectsCreator(form).run()
            return redirect('show_resized_image')
    else:
        form = ImageLoadForm()
    return render(request, 'index.html', {'form': form})


def show_resized_image(request):
    image = ImageModel.objects.latest('id')
    return render(request, 'show_resized_image.html', context={'image': image})


class ImageListView(APIView):
    # http://localhost:8000/api/images/ GET
    def get(self, request):
        images = ImageModel.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    # http://localhost:8000/api/images/ POST
    def post(self, request):
        serializer = ImageURLSerializer(request.data)
        url = serializer.data.get('url')
        ImageAPICreator(url).run()
        image = ImageModel.objects.latest('id')
        serializer = ImageSerializer(image)
        return Response(serializer.data, status=201)


class ImageDetailView(APIView):
    # http://localhost:8000/api/images/1/ GET
    def get(self, request, pk):
        image = ImageModel.objects.get(id=pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    # http://localhost:8000/api/images/1/ DEL
    def delete(self, request, pk):
        ImageModel.objects.filter(id=pk).delete()
        return Response(status=204)


class ImageDetailResizer(APIView):
    # http://localhost:8000/api/images/2/resize/ POST
    def post(self, request, pk):
        serializer = ImageSizeSerializer(request.data)
        size = (serializer.data.get('width'), serializer.data.get('height'))
        image = ImageModel.objects.get(id=pk)
        ImageAPIResizer(image, size).run()
        image = ImageModel.objects.latest('id')
        serializer = ImageSerializer(image)
        return Response(serializer.data, status=201)

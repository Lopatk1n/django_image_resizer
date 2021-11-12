# ImageResizer Django App

This application is needed to resize the image.
On the main page, you can upload an image from your computer or from the link and set the required size.
After that, the application returns a new page with a picture.

## API requests are supported.

 GET 'http://localhost:8000/api/images/'

 GET 'http://localhost:8000/api/images/1/'

 POST 'http://localhost:8000/api/images/' need to specify url of image

 POST 'http://localhost:8000/api/images/2/resize/' need to specify width and height

 DELETE 'http://localhost:8000/api/images/2/'
 
 ## How to deploy locally
 
 create virtual environment
 
 pip install requirements.txt
 
 @migrations already was been applied. Superuser login admin pass 123456
 
 python manage.py runserver
 
 open http://127.0.0.1:8000/
 
 

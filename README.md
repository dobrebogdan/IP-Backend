# IP-Backend
Backed for the IP project

#Prerequisites
Make sure Python, Pip and Django are installed. To install Django use the following command: pip3 install django

#Running the server
Open a terminal, navigate to the /IP-Backend/Server folder and run the following command: python3 manage.py runserver
You can also open the project in PyCharm Professional Edition and click run. 

The server is expected to run on http://127.0.0.1:8000/
Images in binary format can be retrieved with get requests and uploaded with put requests. 

Get requests for the images should be sent to http://127.0.0.1:8000/app/get/id  where id is the id of the image you want.

Get requests for interogating whether the image was retrieved so far or not should be sent to http://127.0.0.1:8000/app/poll/id
They will return 1 if it wasn't retrieved yet and 0 otherwise.

Put requests with the image in binary format should be sent to http://127.0.0.1:8000/app/put

All the images are stored locally in the /IP-Backend/Server/images folder.

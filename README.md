# IP-Backend
Backed for the IP project

#Prerequisites
Make sure Python, Pip and Django are installed. You will also need PyCharm Professional Edition.

#Running the server
Open the project in PyCharm Professional Edition and click run. The server is expected to run on http://127.0.0.1:8000/
Images in binary format can be retrieved with get requests and uploaded with put requests. 
Get requests for the images should be sent to http://127.0.0.1:8000/app/get/id  where id is the id of the image you want.
Get requests for interogating whether the image was retrieved so far or not should be sent to http://127.0.0.1:8000/app/poll/id
Put requests with the image in binary format should be sent to http://127.0.0.1:8000/app/put